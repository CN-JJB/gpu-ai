#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

#ifdef __HIPCC__
#include <hip/hip_runtime.h>
#define GPU_SUCCESS hipSuccess
#define GPU_GET_ERROR_STRING hipGetErrorString
#define GPU_GET_DEVICE hipGetDevice
#define GPU_GET_DEVICE_PROPERTIES hipGetDeviceProperties
#define GPU_MALLOC hipMalloc
#define GPU_FREE hipFree
#define GPU_MEMCPY hipMemcpy
#define GPU_MEMCPY_H2D hipMemcpyHostToDevice
#define GPU_MEMCPY_D2H hipMemcpyDeviceToHost
#define GPU_DEVICE_SYNCHRONIZE hipDeviceSynchronize
#define GPU_GET_LAST_ERROR hipGetLastError
#define GPU_EVENT_CREATE hipEventCreate
#define GPU_EVENT_RECORD hipEventRecord
#define GPU_EVENT_SYNCHRONIZE hipEventSynchronize
#define GPU_EVENT_ELAPSED_TIME hipEventElapsedTime
#define GPU_EVENT_DESTROY hipEventDestroy
#define GPU_OCCUPANCY_MAX_ACTIVE_BLOCKS hipOccupancyMaxActiveBlocksPerMultiprocessor
using GpuEvent = hipEvent_t;
#else
#include <cuda_runtime.h>
#define GPU_SUCCESS cudaSuccess
#define GPU_GET_ERROR_STRING cudaGetErrorString
#define GPU_GET_DEVICE cudaGetDevice
#define GPU_GET_DEVICE_PROPERTIES cudaGetDeviceProperties
#define GPU_MALLOC cudaMalloc
#define GPU_FREE cudaFree
#define GPU_MEMCPY cudaMemcpy
#define GPU_MEMCPY_H2D cudaMemcpyHostToDevice
#define GPU_MEMCPY_D2H cudaMemcpyDeviceToHost
#define GPU_DEVICE_SYNCHRONIZE cudaDeviceSynchronize
#define GPU_GET_LAST_ERROR cudaGetLastError
#define GPU_EVENT_CREATE cudaEventCreate
#define GPU_EVENT_RECORD cudaEventRecord
#define GPU_EVENT_SYNCHRONIZE cudaEventSynchronize
#define GPU_EVENT_ELAPSED_TIME cudaEventElapsedTime
#define GPU_EVENT_DESTROY cudaEventDestroy
#define GPU_OCCUPANCY_MAX_ACTIVE_BLOCKS cudaOccupancyMaxActiveBlocksPerMultiprocessor
using GpuEvent = cudaEvent_t;
#endif

#define GPU_CHECK(expr)                                                         \
  do {                                                                          \
    auto _err = (expr);                                                         \
    if (_err != GPU_SUCCESS) {                                                  \
      std::cerr << "GPU error at " << __FILE__ << ":" << __LINE__ << ": "       \
                << GPU_GET_ERROR_STRING(_err) << std::endl;                    \
      std::exit(1);                                                             \
    }                                                                           \
  } while (0)

__global__ void naive_gemm(const float* a,
                           const float* b,
                           float* c,
                           int n) {
  const int row = blockIdx.y * blockDim.y + threadIdx.y;
  const int col = blockIdx.x * blockDim.x + threadIdx.x;

  if (row >= n || col >= n) {
    return;
  }

  float sum = 0.0f;

  for (int k = 0; k < n; ++k) {
    sum += a[row * n + k] * b[k * n + col];
  }

  c[row * n + col] = sum;
}

template <int TILE>
__global__ void tiled_gemm(const float* a,
                           const float* b,
                           float* c,
                           int n) {
  __shared__ float a_tile[TILE][TILE];
  __shared__ float b_tile[TILE][TILE];

  const int row = blockIdx.y * TILE + threadIdx.y;
  const int col = blockIdx.x * TILE + threadIdx.x;

  float sum = 0.0f;

  for (int tile_start = 0; tile_start < n; tile_start += TILE) {
    const int a_col = tile_start + threadIdx.x;
    const int b_row = tile_start + threadIdx.y;

    a_tile[threadIdx.y][threadIdx.x] =
        (row < n && a_col < n) ? a[row * n + a_col] : 0.0f;

    b_tile[threadIdx.y][threadIdx.x] =
        (b_row < n && col < n) ? b[b_row * n + col] : 0.0f;

    __syncthreads();

#pragma unroll
    for (int k = 0; k < TILE; ++k) {
      sum += a_tile[threadIdx.y][k] * b_tile[k][threadIdx.x];
    }

    __syncthreads();
  }

  if (row < n && col < n) {
    c[row * n + col] = sum;
  }
}

struct Result {
  std::string name;
  int threads_per_block = 0;
  std::size_t shared_bytes = 0;
  int active_blocks = 0;
  double thread_occupancy = 0.0;
  double ms = 0.0;
  double gflops = 0.0;
  double max_abs_error = 0.0;
};

static double verify(const std::vector<float>& output, int n) {
  const double expected = static_cast<double>(n);
  double max_error = 0.0;

  for (float value : output) {
    max_error = std::max(max_error, std::abs(static_cast<double>(value) - expected));
  }

  return max_error;
}

template <typename LaunchFn>
static double time_kernel(LaunchFn&& launch, int repeats) {
  launch();
  GPU_CHECK(GPU_DEVICE_SYNCHRONIZE());

  GpuEvent start{};
  GpuEvent stop{};
  GPU_CHECK(GPU_EVENT_CREATE(&start));
  GPU_CHECK(GPU_EVENT_CREATE(&stop));

  GPU_CHECK(GPU_EVENT_RECORD(start, 0));

  for (int i = 0; i < repeats; ++i) {
    launch();
  }

  GPU_CHECK(GPU_EVENT_RECORD(stop, 0));
  GPU_CHECK(GPU_EVENT_SYNCHRONIZE(stop));

  float total_ms = 0.0f;
  GPU_CHECK(GPU_EVENT_ELAPSED_TIME(&total_ms, start, stop));

  GPU_CHECK(GPU_EVENT_DESTROY(start));
  GPU_CHECK(GPU_EVENT_DESTROY(stop));

  return static_cast<double>(total_ms) / repeats;
}

template <typename Prop>
static Result run_naive(const float* d_a,
                        const float* d_b,
                        float* d_c,
                        std::vector<float>& h_c,
                        int n,
                        int repeats,
                        const Prop& prop) {
  constexpr int BX = 16;
  constexpr int BY = 16;
  constexpr int THREADS = BX * BY;

  dim3 block(BX, BY);
  dim3 grid((n + BX - 1) / BX, (n + BY - 1) / BY);

  auto launch = [&]() {
#ifdef __HIPCC__
    hipLaunchKernelGGL(
        naive_gemm, grid, block, 0, 0, d_a, d_b, d_c, n);
#else
    naive_gemm<<<grid, block>>>(d_a, d_b, d_c, n);
#endif
    GPU_CHECK(GPU_GET_LAST_ERROR());
  };

  int active_blocks = 0;
  GPU_CHECK(GPU_OCCUPANCY_MAX_ACTIVE_BLOCKS(
      &active_blocks, naive_gemm, THREADS, 0));

  const double ms = time_kernel(launch, repeats);

  GPU_CHECK(GPU_MEMCPY(
      h_c.data(),
      d_c,
      h_c.size() * sizeof(float),
      GPU_MEMCPY_D2H));

  const double flops =
      2.0 * static_cast<double>(n) * n * n;

  Result result;
  result.name = "naive-16";
  result.threads_per_block = THREADS;
  result.shared_bytes = 0;
  result.active_blocks = active_blocks;
  result.thread_occupancy =
      std::min(
          1.0,
          static_cast<double>(active_blocks * THREADS) /
              static_cast<double>(prop.maxThreadsPerMultiProcessor));
  result.ms = ms;
  result.gflops = flops / (ms * 1.0e6);
  result.max_abs_error = verify(h_c, n);
  return result;
}

template <int TILE, typename Prop>
static Result run_tiled(const float* d_a,
                        const float* d_b,
                        float* d_c,
                        std::vector<float>& h_c,
                        int n,
                        int repeats,
                        const Prop& prop) {
  constexpr int THREADS = TILE * TILE;
  constexpr std::size_t SHARED_BYTES =
      2 * TILE * TILE * sizeof(float);

  dim3 block(TILE, TILE);
  dim3 grid((n + TILE - 1) / TILE, (n + TILE - 1) / TILE);

  auto launch = [&]() {
#ifdef __HIPCC__
    hipLaunchKernelGGL(
        (tiled_gemm<TILE>), grid, block, 0, 0, d_a, d_b, d_c, n);
#else
    tiled_gemm<TILE><<<grid, block>>>(d_a, d_b, d_c, n);
#endif
    GPU_CHECK(GPU_GET_LAST_ERROR());
  };

  int active_blocks = 0;
  GPU_CHECK(GPU_OCCUPANCY_MAX_ACTIVE_BLOCKS(
      &active_blocks, tiled_gemm<TILE>, THREADS, 0));

  const double ms = time_kernel(launch, repeats);

  GPU_CHECK(GPU_MEMCPY(
      h_c.data(),
      d_c,
      h_c.size() * sizeof(float),
      GPU_MEMCPY_D2H));

  const double flops =
      2.0 * static_cast<double>(n) * n * n;

  Result result;
  result.name = "tile-" + std::to_string(TILE);
  result.threads_per_block = THREADS;
  result.shared_bytes = SHARED_BYTES;
  result.active_blocks = active_blocks;
  result.thread_occupancy =
      std::min(
          1.0,
          static_cast<double>(active_blocks * THREADS) /
              static_cast<double>(prop.maxThreadsPerMultiProcessor));
  result.ms = ms;
  result.gflops = flops / (ms * 1.0e6);
  result.max_abs_error = verify(h_c, n);
  return result;
}

static void print_result(const Result& r) {
  std::cout
      << std::left << std::setw(12) << r.name
      << std::right << std::setw(10) << r.threads_per_block
      << std::setw(13) << r.shared_bytes
      << std::setw(15) << r.active_blocks
      << std::setw(12) << std::fixed << std::setprecision(1)
      << (r.thread_occupancy * 100.0)
      << std::setw(13) << std::setprecision(3) << r.ms
      << std::setw(14) << std::setprecision(1) << r.gflops
      << std::setw(14) << std::setprecision(4) << r.max_abs_error
      << "\n";
}

int main(int argc, char** argv) {
  int n = 2048;

  if (argc >= 2) {
    n = std::stoi(argv[1]);
  }

  if (n < 256 || n > 4096) {
    std::cerr << "N must be between 256 and 4096" << std::endl;
    return 2;
  }

  int device = 0;
  GPU_CHECK(GPU_GET_DEVICE(&device));

#ifdef __HIPCC__
  hipDeviceProp_t prop{};
#else
  cudaDeviceProp prop{};
#endif

  GPU_CHECK(GPU_GET_DEVICE_PROPERTIES(&prop, device));

  const std::size_t elements =
      static_cast<std::size_t>(n) * static_cast<std::size_t>(n);
  const std::size_t bytes = elements * sizeof(float);

  std::vector<float> h_a(elements, 1.0f);
  std::vector<float> h_b(elements, 1.0f);
  std::vector<float> h_c(elements, 0.0f);

  float* d_a = nullptr;
  float* d_b = nullptr;
  float* d_c = nullptr;

  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_a), bytes));
  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_b), bytes));
  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_c), bytes));

  GPU_CHECK(GPU_MEMCPY(d_a, h_a.data(), bytes, GPU_MEMCPY_H2D));
  GPU_CHECK(GPU_MEMCPY(d_b, h_b.data(), bytes, GPU_MEMCPY_H2D));

  constexpr int repeats = 5;

  std::cout << "device: " << prop.name << "\n";
  std::cout << "SM/CU count: " << prop.multiProcessorCount << "\n";
  std::cout << "warpSize: " << prop.warpSize << "\n";
  std::cout << "maxThreadsPerBlock: " << prop.maxThreadsPerBlock << "\n";
  std::cout << "maxThreadsPerMultiProcessor: "
            << prop.maxThreadsPerMultiProcessor << "\n";
  std::cout << "sharedMemPerBlock: "
            << static_cast<unsigned long long>(prop.sharedMemPerBlock)
            << " bytes\n";
  std::cout << "N: " << n
            << ", FP32, matrix bytes each: "
            << std::fixed << std::setprecision(1)
            << (bytes / 1024.0 / 1024.0) << " MiB\n";
  std::cout << "timed repeats per kernel: " << repeats << "\n\n";

  std::cout
      << std::left << std::setw(12) << "kernel"
      << std::right << std::setw(10) << "threads"
      << std::setw(13) << "shared B"
      << std::setw(15) << "active blocks"
      << std::setw(12) << "occ %"
      << std::setw(13) << "time ms"
      << std::setw(14) << "GFLOP/s"
      << std::setw(14) << "max error"
      << "\n";
  std::cout << std::string(103, '-') << "\n";

  print_result(run_naive(
      d_a, d_b, d_c, h_c, n, repeats, prop));

  if (8 * 8 <= prop.maxThreadsPerBlock) {
    print_result(run_tiled<8>(
        d_a, d_b, d_c, h_c, n, repeats, prop));
  }

  if (16 * 16 <= prop.maxThreadsPerBlock) {
    print_result(run_tiled<16>(
        d_a, d_b, d_c, h_c, n, repeats, prop));
  }

  if (32 * 32 <= prop.maxThreadsPerBlock &&
      2 * 32 * 32 * sizeof(float) <= prop.sharedMemPerBlock) {
    print_result(run_tiled<32>(
        d_a, d_b, d_c, h_c, n, repeats, prop));
  }

  GPU_CHECK(GPU_FREE(d_c));
  GPU_CHECK(GPU_FREE(d_b));
  GPU_CHECK(GPU_FREE(d_a));

  return 0;
}

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#ifdef __HIPCC__
#include <hip/hip_runtime.h>
#define GPU_SUCCESS hipSuccess
#define GPU_GET_ERROR_STRING hipGetErrorString
#define GPU_GET_DEVICE hipGetDevice
#define GPU_GET_DEVICE_PROPERTIES hipGetDeviceProperties
#define GPU_MEM_GET_INFO hipMemGetInfo
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
using GpuEvent = hipEvent_t;
#else
#include <cuda_runtime.h>
#define GPU_SUCCESS cudaSuccess
#define GPU_GET_ERROR_STRING cudaGetErrorString
#define GPU_GET_DEVICE cudaGetDevice
#define GPU_GET_DEVICE_PROPERTIES cudaGetDeviceProperties
#define GPU_MEM_GET_INFO cudaMemGetInfo
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

__global__ void triad_kernel(const float* x,
                             const float* y,
                             float* out,
                             std::size_t n) {
  const std::size_t i =
      static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;

  if (i < n) {
    out[i] = x[i] + y[i];
  }
}

template <int REPEATS>
__global__ void mixed_kernel(const float* x,
                             const float* y,
                             float* out,
                             std::size_t n) {
  const std::size_t i =
      static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;

  if (i >= n) {
    return;
  }

  const float xv = x[i];
  const float yv = y[i];

  float a0 = xv + 0.125f;
  float a1 = xv + 0.250f;
  float a2 = xv + 0.500f;
  float a3 = xv + 1.000f;

#pragma unroll
  for (int r = 0; r < REPEATS; ++r) {
    a0 = a0 * 1.0000001f + yv;
    a1 = a1 * 0.9999999f + yv;
    a2 = a2 * 1.0000002f + yv;
    a3 = a3 * 0.9999998f + yv;
  }

  out[i] = (a0 + a1) + (a2 + a3);
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

static double sample_checksum(const std::vector<float>& output) {
  const std::size_t step = std::max<std::size_t>(1, output.size() / 1024);
  double sum = 0.0;

  for (std::size_t i = 0; i < output.size(); i += step) {
    sum += output[i];
  }

  return sum;
}

struct Point {
  std::string name;
  double nominal_ai = 0.0;
  double ms = 0.0;
  double effective_gbs = 0.0;
  double gflops = 0.0;
  double checksum = 0.0;
};

static Point run_triad(const float* d_x,
                       const float* d_y,
                       float* d_out,
                       std::vector<float>& h_out,
                       std::size_t n,
                       int block_size,
                       int repeats) {
  const int grid_size =
      static_cast<int>((n + block_size - 1) / block_size);

  auto launch = [&]() {
#ifdef __HIPCC__
    hipLaunchKernelGGL(
        triad_kernel,
        dim3(grid_size),
        dim3(block_size),
        0,
        0,
        d_x,
        d_y,
        d_out,
        n);
#else
    triad_kernel<<<grid_size, block_size>>>(d_x, d_y, d_out, n);
#endif
    GPU_CHECK(GPU_GET_LAST_ERROR());
  };

  const double ms = time_kernel(launch, repeats);
  const double useful_bytes = static_cast<double>(n) * 12.0;
  const double flops = static_cast<double>(n);

  GPU_CHECK(GPU_MEMCPY(
      h_out.data(),
      d_out,
      h_out.size() * sizeof(float),
      GPU_MEMCPY_D2H));

  Point p;
  p.name = "triad";
  p.nominal_ai = 1.0 / 12.0;
  p.ms = ms;
  p.effective_gbs = useful_bytes / (ms * 1.0e6);
  p.gflops = flops / (ms * 1.0e6);
  p.checksum = sample_checksum(h_out);
  return p;
}

template <int REPEATS>
static Point run_mixed(const float* d_x,
                       const float* d_y,
                       float* d_out,
                       std::vector<float>& h_out,
                       std::size_t n,
                       int block_size,
                       int timed_repeats) {
  const int grid_size =
      static_cast<int>((n + block_size - 1) / block_size);

  auto launch = [&]() {
#ifdef __HIPCC__
    hipLaunchKernelGGL(
        (mixed_kernel<REPEATS>),
        dim3(grid_size),
        dim3(block_size),
        0,
        0,
        d_x,
        d_y,
        d_out,
        n);
#else
    mixed_kernel<REPEATS><<<grid_size, block_size>>>(
        d_x, d_y, d_out, n);
#endif
    GPU_CHECK(GPU_GET_LAST_ERROR());
  };

  const double ms = time_kernel(launch, timed_repeats);
  const double useful_bytes = static_cast<double>(n) * 12.0;
  const double flops =
      static_cast<double>(n) * static_cast<double>(REPEATS) * 8.0;

  GPU_CHECK(GPU_MEMCPY(
      h_out.data(),
      d_out,
      h_out.size() * sizeof(float),
      GPU_MEMCPY_D2H));

  Point p;
  p.name = "mix-" + std::to_string(REPEATS);
  p.nominal_ai = static_cast<double>(REPEATS) * 8.0 / 12.0;
  p.ms = ms;
  p.effective_gbs = useful_bytes / (ms * 1.0e6);
  p.gflops = flops / (ms * 1.0e6);
  p.checksum = sample_checksum(h_out);
  return p;
}

static void print_point(const Point& p) {
  std::cout
      << std::left << std::setw(12) << p.name
      << std::right << std::setw(12) << std::fixed << std::setprecision(3)
      << p.nominal_ai
      << std::setw(13) << std::setprecision(3) << p.ms
      << std::setw(16) << std::setprecision(1) << p.effective_gbs
      << std::setw(16) << std::setprecision(1) << p.gflops
      << std::setw(16) << std::setprecision(3) << p.checksum
      << "\n";
}

int main(int argc, char** argv) {
  int device = 0;
  GPU_CHECK(GPU_GET_DEVICE(&device));

#ifdef __HIPCC__
  hipDeviceProp_t prop{};
#else
  cudaDeviceProp prop{};
#endif

  GPU_CHECK(GPU_GET_DEVICE_PROPERTIES(&prop, device));

  std::size_t free_bytes = 0;
  std::size_t total_bytes = 0;
  GPU_CHECK(GPU_MEM_GET_INFO(&free_bytes, &total_bytes));

  const std::size_t min_elements = std::size_t{1} << 22;
  const std::size_t max_elements = std::size_t{1} << 26;

  std::size_t elements =
      std::min(max_elements, free_bytes / (3 * sizeof(float) * 4));

  elements = std::max(min_elements, elements);

  if (argc >= 2) {
    elements = static_cast<std::size_t>(std::stoull(argv[1]));
  }

  const std::size_t bytes = elements * sizeof(float);

  if (3 * bytes > free_bytes / 2) {
    std::cerr
        << "Requested workload is too large for the currently free GPU memory. "
        << "Choose fewer elements."
        << std::endl;
    return 2;
  }

  std::vector<float> h_x(elements, 1.0f);
  std::vector<float> h_y(elements, 0.5f);
  std::vector<float> h_out(elements, 0.0f);

  float* d_x = nullptr;
  float* d_y = nullptr;
  float* d_out = nullptr;

  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_x), bytes));
  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_y), bytes));
  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_out), bytes));

  GPU_CHECK(GPU_MEMCPY(d_x, h_x.data(), bytes, GPU_MEMCPY_H2D));
  GPU_CHECK(GPU_MEMCPY(d_y, h_y.data(), bytes, GPU_MEMCPY_H2D));

  constexpr int block_size = 256;
  constexpr int timed_repeats = 5;

  std::cout << "device: " << prop.name << "\n";
  std::cout << "SM/CU count: " << prop.multiProcessorCount << "\n";
  std::cout << "warpSize: " << prop.warpSize << "\n";
  std::cout << "elements: " << elements << "\n";
  std::cout << "array size each: "
            << std::fixed << std::setprecision(1)
            << (bytes / 1024.0 / 1024.0) << " MiB\n";
  std::cout << "three arrays total: "
            << (3.0 * bytes / 1024.0 / 1024.0) << " MiB\n";
  std::cout << "timed repeats: " << timed_repeats << "\n\n";

  std::cout
      << std::left << std::setw(12) << "kernel"
      << std::right << std::setw(12) << "AI F/B"
      << std::setw(13) << "time ms"
      << std::setw(16) << "useful GB/s"
      << std::setw(16) << "GFLOP/s"
      << std::setw(16) << "checksum"
      << "\n";
  std::cout << std::string(85, '-') << "\n";

  print_point(run_triad(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  print_point(run_mixed<1>(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  print_point(run_mixed<4>(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  print_point(run_mixed<16>(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  print_point(run_mixed<64>(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  print_point(run_mixed<256>(
      d_x, d_y, d_out, h_out, elements, block_size, timed_repeats));

  GPU_CHECK(GPU_FREE(d_out));
  GPU_CHECK(GPU_FREE(d_y));
  GPU_CHECK(GPU_FREE(d_x));

  return 0;
}

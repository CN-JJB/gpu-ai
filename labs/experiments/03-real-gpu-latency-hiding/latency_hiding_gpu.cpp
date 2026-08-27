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
#define GPU_MALLOC hipMalloc
#define GPU_FREE hipFree
#define GPU_MEMCPY hipMemcpy
#define GPU_MEMCPY_H2D hipMemcpyHostToDevice
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

__global__ void memory_stall_kernel(const std::uint32_t* next,
                                    std::uint32_t* out,
                                    std::uint32_t mask,
                                    int steps,
                                    std::size_t dynamic_smem_bytes) {
  extern __shared__ unsigned char scratch[];

  if (dynamic_smem_bytes > 0 && threadIdx.x == 0) {
    scratch[0] = 1;
  }
  __syncthreads();

  const std::size_t gid =
      static_cast<std::size_t>(blockIdx.x) * blockDim.x + threadIdx.x;

  std::uint32_t idx = static_cast<std::uint32_t>(gid) & mask;

#pragma unroll 1
  for (int i = 0; i < steps; ++i) {
    idx = next[idx];
  }

  if (dynamic_smem_bytes > 0 && threadIdx.x == 0) {
    scratch[0] ^= static_cast<unsigned char>(idx);
  }

  out[gid] = idx;
}

static void launch_kernel(int grid,
                          int block,
                          std::size_t smem_bytes,
                          const std::uint32_t* d_next,
                          std::uint32_t* d_out,
                          std::uint32_t mask,
                          int steps) {
#ifdef __HIPCC__
  hipLaunchKernelGGL(memory_stall_kernel,
                     dim3(grid),
                     dim3(block),
                     smem_bytes,
                     0,
                     d_next,
                     d_out,
                     mask,
                     steps,
                     smem_bytes);
#else
  memory_stall_kernel<<<grid, block, smem_bytes>>>(
      d_next, d_out, mask, steps, smem_bytes);
#endif
  GPU_CHECK(GPU_GET_LAST_ERROR());
}

int main(int argc, char** argv) {
  int pow2 = 24;
  int steps = 128;

  if (argc >= 2) {
    pow2 = std::stoi(argv[1]);
  }
  if (argc >= 3) {
    steps = std::stoi(argv[2]);
  }

  if (pow2 < 20 || pow2 > 28) {
    std::cerr << "pow2 must be between 20 and 28" << std::endl;
    return 2;
  }
  if (steps < 1) {
    std::cerr << "steps must be positive" << std::endl;
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

  const std::size_t entries = std::size_t{1} << pow2;
  const std::uint32_t mask = static_cast<std::uint32_t>(entries - 1);
  const std::size_t bytes = entries * sizeof(std::uint32_t);
  const std::uint32_t stride = 131071u;

  std::vector<std::uint32_t> next(entries);
  for (std::size_t i = 0; i < entries; ++i) {
    next[i] = static_cast<std::uint32_t>((i + stride) & mask);
  }

  constexpr int block_size = 256;
  const int grid_size = prop.multiProcessorCount * 16;
  const std::size_t output_items =
      static_cast<std::size_t>(grid_size) * block_size;

  std::uint32_t* d_next = nullptr;
  std::uint32_t* d_out = nullptr;

  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_next), bytes));
  GPU_CHECK(GPU_MALLOC(reinterpret_cast<void**>(&d_out),
                       output_items * sizeof(std::uint32_t)));
  GPU_CHECK(GPU_MEMCPY(d_next, next.data(), bytes, GPU_MEMCPY_H2D));

  std::cout << "device: " << prop.name << "\n";
  std::cout << "SM/CU count: " << prop.multiProcessorCount << "\n";
  std::cout << "warpSize: " << prop.warpSize << "\n";
  std::cout << "maxThreadsPerMultiProcessor: "
            << prop.maxThreadsPerMultiProcessor << "\n";
  std::cout << "sharedMemPerBlock: "
            << static_cast<unsigned long long>(prop.sharedMemPerBlock)
            << " bytes\n";
  std::cout << "array: 2^" << pow2 << " uint32_t = "
            << std::fixed << std::setprecision(1)
            << (bytes / 1024.0 / 1024.0) << " MiB\n";
  std::cout << "block size: " << block_size
            << ", grid size: " << grid_size
            << ", dependent-load steps/thread: " << steps << "\n\n";

  std::cout << std::setw(10) << "smem KiB"
            << std::setw(16) << "active blocks"
            << std::setw(16) << "thread occ"
            << std::setw(14) << "time ms"
            << std::setw(16) << "Gload/s" << "\n";
  std::cout << std::string(72, '-') << "\n";

  const std::vector<std::size_t> smem_values = {
      0,
      8 * 1024,
      16 * 1024,
      24 * 1024,
      32 * 1024,
  };

  constexpr int repeats = 5;

  for (std::size_t smem_bytes : smem_values) {
    if (smem_bytes > prop.sharedMemPerBlock) {
      continue;
    }

    int active_blocks = 0;
    GPU_CHECK(GPU_OCCUPANCY_MAX_ACTIVE_BLOCKS(
        &active_blocks, memory_stall_kernel, block_size, smem_bytes));

    const double thread_occupancy =
        static_cast<double>(active_blocks * block_size) /
        static_cast<double>(prop.maxThreadsPerMultiProcessor);

    launch_kernel(grid_size,
                  block_size,
                  smem_bytes,
                  d_next,
                  d_out,
                  mask,
                  steps);
    GPU_CHECK(GPU_DEVICE_SYNCHRONIZE());

    GpuEvent start{};
    GpuEvent stop{};
    GPU_CHECK(GPU_EVENT_CREATE(&start));
    GPU_CHECK(GPU_EVENT_CREATE(&stop));

    GPU_CHECK(GPU_EVENT_RECORD(start, 0));
    for (int r = 0; r < repeats; ++r) {
      launch_kernel(grid_size,
                    block_size,
                    smem_bytes,
                    d_next,
                    d_out,
                    mask,
                    steps);
    }
    GPU_CHECK(GPU_EVENT_RECORD(stop, 0));
    GPU_CHECK(GPU_EVENT_SYNCHRONIZE(stop));

    float total_ms = 0.0f;
    GPU_CHECK(GPU_EVENT_ELAPSED_TIME(&total_ms, start, stop));

    GPU_CHECK(GPU_EVENT_DESTROY(start));
    GPU_CHECK(GPU_EVENT_DESTROY(stop));

    const double avg_ms = total_ms / repeats;
    const double loads =
        static_cast<double>(output_items) * static_cast<double>(steps);
    const double gloads_per_s = loads / (avg_ms * 1.0e6);

    std::cout << std::setw(10) << (smem_bytes / 1024)
              << std::setw(16) << active_blocks
              << std::setw(15) << std::setprecision(1)
              << (thread_occupancy * 100.0) << "%"
              << std::setw(14) << std::setprecision(3) << avg_ms
              << std::setw(16) << std::setprecision(3) << gloads_per_s
              << "\n";
  }

  GPU_CHECK(GPU_FREE(d_out));
  GPU_CHECK(GPU_FREE(d_next));
  return 0;
}

# Research Note 0003 — Registers、Shared Memory/LDS、Tiling 与 Data Reuse

日期：2026-08-26

## Research question

在 GPU kernel 中，为什么高性能实现常常把 global-memory 数据先搬到 shared memory / LDS，再放到 registers 中重复使用？tile size、register pressure、shared-memory/LDS footprint、occupancy、coalescing 和 bank conflicts 之间是什么关系？这些 trade-off 如何迁移到 GEMM 与后续 LLM kernel？

## Scope

本笔记建立稳定的跨 NVIDIA / AMD 心智模型，不把某一代 GPU 的 cache 容量、bank 数、register file 大小或峰值带宽写成通用常数。

本切片重点：
- registers / VGPR-SGPR
- shared memory / LDS
- global memory
- local memory / scratch spill
- coalescing
- bank conflicts
- tiling / reuse
- occupancy trade-off

cache、VRAM/HBM 带宽、PCIe/NVLink/Infinity Fabric 的定量分析留给下一切片。

## Primary sources

1. NVIDIA CUDA Programming Guide — Memory hierarchy / Registers / Local memory  
   https://docs.nvidia.com/cuda/cuda-programming-guide/  
   支撑：
   - registers 在 SM 上、thread-local；
   - shared memory 为 block 内共享片上存储；
   - global memory 为 device-wide 大容量存储；
   - CUDA local memory 名称描述作用域，不描述物理位置；它位于 device/global memory 空间；
   - register spilling 可把值放进 local memory。

2. NVIDIA CUDA C++ Best Practices Guide — Device memory spaces / coalescing / shared memory  
   https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/  
   支撑：
   - global-memory accesses 应尽量 coalesced；
   - shared memory 片上、低延迟高带宽，但 bank conflicts 会降低有效吞吐；
   - shared memory 可作为 user-managed cache；
   - matrix multiplication 中，tile 数据可从 global memory 只加载一次后被多个 threads 重用。

3. NVIDIA CUDA C++ Best Practices Guide — Shared Memory in Matrix Multiplication  
   https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#shared-memory-in-matrix-multiplication-c-ab  
   支撑：
   - matrix tile 放进 shared memory 能减少重复 global-memory reads；
   - shared memory 还能用于把 global-memory accesses 组织成 coalesced pattern。

4. NVIDIA Deep Learning Performance — Matrix Multiplication Background  
   https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html  
   支撑：
   - GEMM 以 output tiles 分配给 thread blocks；
   - larger tiles 通常提高 data reuse、降低 bandwidth demand；
   - larger tiles 同时会减少可并行 tiles 数，形成 tile efficiency ↔ tile parallelism trade-off。

5. NVIDIA CUTLASS — Efficient GEMM in CUDA  
   https://docs.nvidia.com/cutlass/latest/media/docs/cpp/efficient_gemm.html  
   支撑：
   - 高性能 GEMM 采用 global → shared memory → registers 的层级 tiling；
   - threadblock / warp / thread 级 tile 对应 memory hierarchy；
   - accumulator 大量占用 registers，优化 GEMM 往往不是高 occupancy kernel；
   - software pipelining / double buffering 可在低 occupancy 下继续隐藏 latency。

6. NVIDIA CUDA Programming Guide — NVCC resource reporting  
   https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/nvcc.html  
   支撑：
   - `-res-usage` 可报告 registers/shared/local 等 kernel resource usage；
   - `-Xptxas=-warn-spills` / `-warn-lmem-usage` 可辅助识别 spilling。

7. AMD ROCm HIP — Programming model / Memory model  
   https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html  
   支撑：
   - per-thread registers 位于 CU register file；
   - shared memory 对应 LDS，是 work-group 内共享的 programmer-managed on-chip storage；
   - HBM/global memory 是 device-wide 大容量层；
   - register pressure 可导致 spill 到 global/scratch，并影响 occupancy；
   - LDS 用量直接影响一个 CU 可驻留 work-groups 数量。

8. AMD ROCm HIP — Performance guidelines  
   https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html  
   支撑：
   - consecutive threads 访问 consecutive addresses 可形成 coalesced transactions；
   - shared memory/LDS 适用于 data reuse 与 tiled matrix multiplication；
   - bank conflicts 会序列化 LDS requests；
   - `hipcc --resource-usage` 可检查 kernel register/resource usage。

9. AMD ROCm — Understanding GPU performance  
   https://rocm.docs.amd.com/projects/HIP/en/latest/understand/performance_optimization.html  
   支撑：
   - LDS bank conflict 的机制与架构相关；
   - bank 组织不是跨代固定常数，应针对目标 CDNA/RDNA 查询。

10. AMD ROCm HIP — Device memory / shared memory  
    https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/hip_runtime_api/memory_management/device_memory.html  
    支撑：
    - HIP shared memory / LDS 是 CU 本地的 on-chip storage；
    - 可静态或动态按 work-group 分配。

11. AMD ROCm Profiler SDK — scratch memory trace  
    https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html  
    支撑：
    - AMD scratch roughly corresponds to CUDA local memory；
    - scratch 可用于 spills / stack-like private storage，可被 profiler trace。

## Findings

### F1 — “快慢层级”不是完整模型，真正关键是 scope + capacity + reuse

稳定的跨厂商近似：

- registers：thread-private，片上，最靠近执行单元，容量最紧张；
- shared memory / LDS：block/work-group shared，片上，由程序显式管理；
- global memory / VRAM/HBM：device-wide，大容量、高带宽，但相对片上存储延迟高得多；
- cache：硬件管理，用来减少到更远层级的访问；
- CUDA local / AMD scratch：逻辑上 thread-private，但物理代价更接近 global-memory path，常见来源之一是 spilling。

因此“把数据放更快的 memory”只是表面。更重要的问题是：

**同一份远端数据能不能加载一次，然后在更近层级被重复使用很多次？**

### F2 — Registers 的价值是 thread-local reuse，但 register pressure 会反过来限制 residency

GEMM 的 accumulator、循环中间值、向量 fragment 等常驻 registers，可以避免反复访问 shared/global memory。

代价：
- 每 thread registers 增加；
- 一个 SM/CU 的 register file 被更少 threads/warps 分完；
- resident blocks/warps 可能下降；
- occupancy / latency-hiding headroom 下降。

因此上一切片的 occupancy trade-off 在这里有了实体来源。

### F3 — “限制 registers 以提高 occupancy”可能制造 spill

NVIDIA 文档明确指出，压低 register usage 可能允许更多 blocks 同时驻留，但也可能导致 register spilling。

CUDA local memory 名字非常容易误导：它是 thread-local 的地址空间，但物理上位于 device/global memory 空间。

AMD 对应的 private/scratch spill 同样会把本来应该留在 registers 的值放到高代价存储路径。

稳定判断：

**不要用 occupancy 目标反向强迫编译器少用 registers，除非 profiler/benchmark 证明值得。**

### F4 — Shared memory / LDS 的核心价值是跨 threads 的显式 data reuse

如果一个 block/work-group 内很多 threads 都要用同一 tile 数据：

global memory
→ cooperative coalesced load
→ shared memory / LDS
→ block 内重复使用

可以把“每个 thread 自己反复从 global 读”变成“整个 block 只搬一次，然后共享”。

这就是 tiled GEMM 的第一层价值。

### F5 — Tiling 本质上是在购买 arithmetic intensity

对于简化的方阵 GEMM C=A×B：

naive 概念模型中，每个 output element 都独立读取 K 个 A 和 K 个 B 元素。

若 tile width = T，并假设每个 A/B tile 从 global 只加载一次供 T×T outputs 使用，则算法级 input-load requests 近似减少 T 倍。

因此 tile size 增大时：

global bytes / FLOP ↓
→ arithmetic intensity ↑
→ 更有机会从 memory-bound 向 compute-bound 移动。

注意：这只是算法级 request/reuse 模型，真实 DRAM traffic 还受 cache、broadcast、coalescing、prefetch 和编译器影响。

### F6 — Larger tile 不是无限更好

tile 增大通常带来：
- 更高 reuse；
- 更少 global-memory traffic；
- 更高 arithmetic intensity。

同时也带来：
- 更多 threads per block，或更多 work per thread；
- 更大的 shared memory/LDS footprint；
- 更多 register accumulators；
- 更少 resident blocks；
- 更少独立 tiles 可并行；
- 边界浪费 / tile quantization；
- 可能更高 bank-conflict 风险。

NVIDIA 的 GEMM performance guide 明确把它描述成 tile efficiency ↔ tile parallelism trade-off。

### F7 — Coalescing 解决“怎么搬”，tiling/reuse 解决“搬多少次”

这是两个不同问题：

**Coalescing**
- 同一 warp/wavefront 的 threads 访问地址是否能被硬件合并成少量宽 transactions；
- 目标是提高每次 global-memory transaction 的有效利用率。

**Tiling / reuse**
- 同一份数据是否被反复从 global memory 取回；
- 目标是减少 transaction 总需求。

高性能 kernel 通常两者都要。

### F8 — Shared memory/LDS 也不是“免费高速缓存”

programmer-managed scratchpad 需要：
- 显式 load；
- synchronization；
- 正确 lifetime；
- 合适 layout；
- 避免或减少 bank conflicts。

如果没有 reuse，或者同步/搬运成本超过收益，把数据绕一趟 shared memory/LDS 可能反而更慢。

### F9 — Bank conflicts 是片上 memory 的访问模式问题

shared memory/LDS 被分成多个 banks，以并行服务不同地址。

如果同一执行组内多个 requests 映射到同一 bank 且不是可广播情况，就可能序列化。

因此：
global coalescing 做好了
≠ shared/LDS access 一定高效。

具体 bank 数、映射和例外随架构变化，不应在稳定 Lesson 中写死为跨厂商常数。

### F10 — 高性能 GEMM 是执行模型与 memory hierarchy 的合流点

CUTLASS 给出的稳定层级非常适合课程后续：

global memory tile
→ threadblock shared-memory tile
→ warp-level fragments
→ thread registers / accumulators
→ matrix/SIMT instructions

这解释了为什么：
- register pressure 会高；
- occupancy 未必高；
- 仍然可以靠 reuse、ILP、software pipelining 得到高性能。

## LLM connection

后续本地 LLM kernel 会不断遇到同一个问题：

**能不能把高代价的 HBM/VRAM 流量，换成片上重复使用？**

典型场景包括：
- GEMM / linear layers；
- Attention 中 Q/K/V 或中间 tile；
- quantization/dequantization 中的 scale、packed values 与 accumulators；
- fused kernels 把中间结果留在 registers/shared memory，而不是写回 global memory 再重新读。

本切片不声称所有 LLM kernels 都遵循同一个 tile 形状；只建立资源 trade-off 的通用判断法。

## Stable cross-vendor mental model

far / large / expensive per access
global VRAM/HBM
    ↓ cooperative + coalesced loads
shared memory / LDS
    ↓ repeated block/work-group reuse
register fragments / accumulators
    ↓ math
execution pipelines / matrix units

优化目标不是“永远往上搬”，而是：

**用有限片上容量换足够大的 reuse，且别让 occupancy、parallelism、bank conflicts、spills 和 synchronization 成本吃掉收益。**

## Claims to avoid

- “shared memory 一定比 cache 快，所以必须手动搬。”
- “tile 越大一定越快。”
- “occupancy 越高越快。”
- “限制 registers 一定能提高性能。”
- “CUDA local memory 在芯片本地。”
- “global coalescing 做好以后就不会 memory-bound。”
- “shared memory/LDS 没有访问冲突。”
- “NVIDIA shared memory bank 规则可直接套到所有 AMD 架构。”

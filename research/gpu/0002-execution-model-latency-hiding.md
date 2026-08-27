# Research Note 0002 — GPU 执行模型：thread → warp/wavefront → SM/CU → scheduler → latency hiding

日期：2026-08-26

## Research question

当一个 GPU kernel 启动成大量逻辑线程后，这些线程如何被组织到 warp / wavefront、映射到 SM / CU，并由 scheduler 在长延迟操作之间切换？occupancy、寄存器和 shared memory / LDS 又如何改变这种 latency hiding 能力？

## Scope

本笔记只抽取对后续本地 LLM 判断最稳定的执行模型，不试图把某一代 NVIDIA 或 AMD 的具体 scheduler 数量、issue 宽度、pipeline 数量推广成所有 GPU 的规则。

术语以 CUDA/HIP 编程模型为入口。NVIDIA 为主线，AMD 做系统性迁移对照。

## Primary sources

1. NVIDIA CUDA Programming Guide — Programming Model  
   https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html  
   支撑：grid / thread block / thread 层级；thread block 在一个 SM 上执行；warp 为 32 threads；SM 的寄存器与 shared memory 是有限的驻留资源。

2. NVIDIA CUDA Programming Guide — Advanced Kernel Programming / Hardware Multithreading  
   https://docs.nvidia.com/cuda/cuda-programming-guide/03-advanced/advanced-kernel-programming.html  
   支撑：SM 将 block 划分为 warp；warp scheduler 从 ready warp 中选择并发射；warp 执行上下文常驻片上，普通 warp 切换不需要像 CPU OS thread 那样保存/恢复上下文；resident blocks/warps 受到 registers、shared memory 和硬件上限约束。

3. NVIDIA CUDA C++ Best Practices Guide — Execution Configuration / Occupancy  
   https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html  
   支撑：低 occupancy 会妨碍隐藏 memory latency，但更高 occupancy 不总等于更高性能；register usage 与 shared memory 会限制 occupancy；可以通过实验改变 dynamic shared memory 观察性能对 occupancy 的敏感性。

4. NVIDIA Deep Learning Performance — GPU Execution Model  
   https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html  
   支撑：深度学习 workload 中需要远多于执行 pipeline 数量的 threads；当一些 threads 等待依赖/内存时切换到其他 threads 是 GPU 利用率的关键。

5. AMD ROCm HIP — Introduction to the HIP programming model  
   https://rocm.docs.amd.com/projects/HIP/en/latest/understand/programming_model.html  
   支撑：work-item/thread、work-group/block、warp/wavefront 与 CU 的层级；warp 因 HBM 等长延迟操作 stall 后，scheduler 选择其他 ready warp；同一 work-group 的 warps 在同一 CU 上执行并共享 LDS。

6. AMD ROCm HIP — Hardware implementation  
   https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html  
   支撑：CU、sequencer/scheduling、VGPR/SGPR/LDS/warp slots 对并发驻留的限制；AMD 通过大量硬件多线程隐藏 memory/instruction latency；RDNA 与 CDNA 的组织并不相同。

7. AMD ROCm HIP — Performance guidelines  
   https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html  
   支撑：register pressure 与 shared memory/LDS 使用会限制 occupancy；降低资源使用可以增加并发 warps，但仍应通过 profile 验证性能。

8. AMD ROCm HIP — Hardware features  
   https://rocm.docs.amd.com/projects/HIP/en/latest/reference/hardware_features.html  
   支撑：wavefront/warp size 与目标架构相关。便携 HIP 代码不应把 AMD wavefront 永久硬编码成 64。

## Findings

### F1 — “thread”首先是编程模型里的逻辑工作单位

CUDA thread / HIP work-item 让程序员以标量线程写代码，但 GPU 不会把每个逻辑 thread 当成一个完全独立、每周期单独调度的 CPU core。

真正进入硬件调度时，threads 会被组织成 warp / wavefront 这样的执行组。

### F2 — NVIDIA warp 固定 32；AMD wavefront 必须按目标架构看

CUDA 编程模型把一个 warp 定义为 32 threads。

AMD 文档同时覆盖 CDNA 和 RDNA：常见 Instinct/CDNA 路径是 Wave64，现代 Radeon/RDNA 的 HIP 路径通常是 Wave32；HIP 还提供 warpSize 查询。稳定结论不是“AMD 永远 64”，而是：**不要在可移植代码和判断中把执行组宽度写死。**

### F3 — block/work-group 是资源与协作边界

NVIDIA thread block 的全部 threads 在一个 SM 上执行，因此可以使用该 SM 的 shared memory 并进行 block 内同步。

AMD work-group 的 wavefronts 同样被放在同一 CU 上，以访问同一 LDS 并同步。

因此从 kernel 代码到硬件的稳定映射可以写成：

thread → warp/wavefront → block/work-group residency → SM/CU

这不是说 block 先“变成”warp 再分配；更准确地说，block 被分配到 SM/CU 后，其 threads 以多个 warp/wavefront 被执行。

### F4 — latency hiding 的核心是“还有别的 ready group”

一个 warp/wavefront 发出长延迟内存操作后，后续依赖该结果的指令暂时不能继续。

GPU 的关键策略不是让这次内存访问本身变快，而是让 scheduler 选择另一个 ready 的 resident warp/wavefront 发射指令。只要还有足够多 ready groups，执行 pipeline 就能继续有活干。

所以 latency hiding 是**吞吐层面的掩盖**，不是“内存延迟消失”。

### F5 — warp/wavefront 切换和 CPU OS thread context switch 不是一回事

NVIDIA 明确描述 resident warp 的程序计数器、寄存器等执行上下文在生命周期内保留在片上；AMD 也描述 resident warp context 保存在 CU 上。

因此普通 scheduler 在 resident groups 之间换一个 ready group 发射，并不需要像 CPU 操作系统线程那样把整个上下文换入换出内存。

### F6 — occupancy 是“可同时驻留多少”，不是“GPU 有多忙”

NVIDIA 将 occupancy 定义为 active warps 相对硬件最大 active warps 的比例；AMD 对 CU/wavefront 给出同类定义。

它描述的是隐藏延迟所需的可用并发度上限之一，但不直接等于：
- issue efficiency；
- ALU utilization；
- memory bandwidth utilization；
- kernel performance。

官方 NVIDIA Best Practices 明确指出，更高 occupancy 不总能带来更高 performance。

### F7 — registers 与 shared memory/LDS 形成真实的 trade-off

每个 resident block/work-group 会占用有限的片上资源。

NVIDIA：per-thread registers + per-block shared memory 会限制一个 SM 同时能驻留多少 blocks/warps。

AMD：VGPR、SGPR、LDS 与 warp slots 共同限制一个 CU 上的 resident work-groups/warps。

因此：
更多寄存器/更大的 tile/更多 shared memory 或 LDS
→ 可能提高单个 group 的数据复用与 ILP
→ 也可能减少 resident groups
→ 降低 occupancy 和 latency-hiding headroom。

这正是后续 GEMM / Attention kernel 调优的核心张力之一。

### F8 — 高性能 LLM kernel 不应以“100% occupancy”为目标函数

矩阵乘、Attention、量化反量化等 kernel 经常主动用更多寄存器或 shared memory/LDS 保存 tile、累加器和中间结果。

如果这些资源换来了更少的 global-memory traffic、更好的数据复用、更强 ILP 或矩阵流水线利用，即使 occupancy 下降，最终也可能更快。

正确问题是：**当前 bottleneck 是不是因为没有足够 ready warps/wavefronts？**

## Stable cross-vendor mental model

kernel
→ many logical threads
→ block / work-group
→ resident on an SM / CU
→ threads execute as warp / wavefront groups
→ scheduler chooses a ready group
→ a group stalls on dependency or memory
→ scheduler issues another ready resident group
→ enough ready groups can hide latency

## Architecture-specific cautions

- NVIDIA Volta+ 有 Independent Thread Scheduling；不要把“warp 永远逐指令严格 lockstep”的旧式直觉用于正确性推理。
- AMD RDNA 引入 WGP 并改变 Wave32/Wave64 组织；CU 与 NVIDIA SM 只能做作用层映射，不能假设内部结构相同。
- scheduler 数量、每周期 issue 能力、pipeline 数量、最大 resident warps 都随具体架构变化，应查目标架构资料或 profiler。
- occupancy 公式需要目标 GPU 的实际 register/shared-memory/LDS 分配粒度与硬件限制，不能只用一个通用数字。

## Claims to avoid

- “一个 CUDA Core 对应一个 CUDA thread。”
- “warp/wavefront 就是一颗硬件 core。”
- “AMD wavefront 永远是 64。”
- “SM 和 CU 微架构完全等价。”
- “warp 切换就是 CPU thread context switch。”
- “occupancy 越高越快，100% 最优。”
- “latency hiding 把内存访问延迟变没了。”

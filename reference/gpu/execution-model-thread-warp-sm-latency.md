# GPU 执行模型速查：Thread → Warp/Wavefront → SM/CU → Scheduler → Latency Hiding

## 一句话模型

**GPU 不靠让每一次等待都很短，而是靠保留很多可运行的执行组；一个组在等，scheduler 就发射另一个 ready 组。**

## 层级

| 程序员看到的层 | NVIDIA CUDA | AMD HIP / ROCm | 稳定含义 |
|---|---|---|---|
| 单个逻辑工作 | thread | work-item / thread | 每个元素/任务的标量程序实例 |
| 协作组 | thread block | work-group / block | 同组可同步并共享片上 scratchpad |
| 硬件执行组 | warp = 32 threads | wavefront / warp；宽度依目标架构 | scheduler 实际选择和发射的线程组 |
| 主要执行资源 | SM | CU；RDNA 还存在 WGP 组织 | 驻留 blocks/groups、寄存器、片上共享内存和执行 pipeline 的局部资源域 |
| 片上共享 scratchpad | shared memory | LDS | block/work-group 内协作和数据复用 |
| 线程状态 | registers | VGPR/SGPR 等 | 快，但有限；会影响可驻留并发度 |

## 从 launch 到执行

kernel launch
→ grid
→ blocks / work-groups
→ block 被分配到一个 SM / CU
→ block 的 threads 以多个 warp / wavefront 执行
→ scheduler 每次选择 ready group 发射
→ 某 group 因 memory/dependency stall
→ scheduler 改发射其他 ready resident groups

## Latency hiding

- 目标：让执行 pipeline 在某些 groups 等待时仍有别的工作。
- 需要：足够的 resident 且 ready 的 warp/wavefront。
- 不代表：单次 HBM/VRAM 访问的真实 latency 被降低。
- 如果所有 resident groups 都在等，pipeline 仍会出现 idle cycles。

## Occupancy

概念定义：

occupancy = active warps/wavefronts ÷ hardware maximum active warps/wavefronts

它是“并发驻留能力”的指标，不是性能分数。

### 常见限制

- threads per block/work-group
- registers per thread / VGPR、SGPR pressure
- shared memory / LDS per block
- resident block / warp slots
- 具体架构资源分配粒度

### 重要纠偏

更高 occupancy 不一定更快。

一个 kernel 可能用更多 registers/shared memory/LDS：
→ occupancy 下降
→ 但数据复用、ILP、global-memory traffic 或矩阵 pipeline 利用改善
→ 总性能反而上升。

## NVIDIA ↔ AMD 迁移

| 先问什么 | NVIDIA | AMD |
|---|---|---|
| 执行组多宽？ | warp 32 | 查询目标 warpSize；CDNA/Instinct 常见 64，RDNA/HIP 常见 32 |
| block 放在哪里？ | 一个 SM | 一个 CU |
| block 内 scratchpad？ | shared memory | LDS |
| 什么限制驻留？ | registers + shared memory + block/warp limits | VGPR/SGPR + LDS + warp slots/work-group limits |
| 谁隐藏等待？ | warp scheduler 选择 ready warp | wavefront/warp scheduler 选择 ready wavefront |
| occupancy 是否越高越好？ | 否 | 否 |

SM 与 CU 是作用层类比，不是内部微架构等号。

## 读 LLM kernel 时的检查顺序

1. 一个 block/work-group 有多少 threads？
2. 等于多少 warp/wavefront？
3. 每 thread 用多少 registers？
4. 每 block 用多少 shared memory/LDS？
5. 这些资源允许多少 blocks/groups 同时 resident？
6. stall 主要来自 memory、dependency、divergence 还是别的 pipeline？
7. 增加 occupancy 后，真实 throughput/latency 有没有改善？
8. 如果 occupancy 降了，是否换来了更好的 tile reuse、ILP 或更少的 global-memory traffic？

## 不要背错的口诀

- thread ≠ CUDA Core
- warp/wavefront ≠ 一颗 core
- AMD wavefront ≠ 永远 64
- occupancy ≠ utilization
- occupancy ≠ performance
- latency hiding ≠ latency elimination

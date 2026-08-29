# Experiment 05 — 真实 GPU：Naive GEMM vs Shared-Memory/LDS Tiled GEMM

Hardware level: L2  
Risk: safe  
Cost: 已有独显时为 0  
平台：Linux 优先  
支持：NVIDIA CUDA / AMD HIP  
替代路径：没有可用独显时完成 Experiment 04 L0，不影响课程继续。

## 问题

同一个 FP32 GEMM：

~~~text
C = A × B
~~~

如果：

1. naive kernel 每个 thread 直接从 global memory 完成整个 dot product；
2. tiled kernel 让 block/work-group 合作把 A/B tiles 放到 shared memory/LDS，再重复使用；

真实 GPU 上：

- kernel time 会怎么变？
- tile 8 / 16 / 32 是否一直越大越快？
- static shared/LDS footprint 和 active blocks/SM-CU 怎么变？
- compiler 报告的 registers / VGPR / SGPR 是否变化？
- profiler 能否看到 global-memory traffic / cache / occupancy / bank-conflict 线索？

## 为什么这个实验有价值

它把前两节连起来：

~~~text
tile reuse
→ shared/LDS footprint
→ register/resource pressure
→ residency / occupancy
→ memory traffic
→ measured throughput
~~~

我们不预设“tiled 一定快多少”，只要求产生可解释 Evidence。

## Source

`naive_vs_tiled_gemm.cpp` 同时支持：

- `nvcc`
- `hipcc`

默认 N=2048，输入矩阵全为 1，因此正确结果每个 C 元素都应接近 N。这样可以做廉价 correctness check，而不用再写一个巨大的 CPU GEMM。

## 编译

### NVIDIA

~~~bash
nvcc -O3 -std=c++17 -x cu -res-usage \
  naive_vs_tiled_gemm.cpp -o gemm-cuda
~~~

可选检查 spill：

~~~bash
nvcc -O3 -std=c++17 -x cu -res-usage \
  -Xptxas=-warn-spills -Xptxas=-warn-lmem-usage \
  naive_vs_tiled_gemm.cpp -o gemm-cuda
~~~

### AMD ROCm/HIP

~~~bash
hipcc -O3 -std=c++17 --resource-usage \
  naive_vs_tiled_gemm.cpp -o gemm-hip
~~~

## 运行

~~~bash
./gemm-cuda
# 或
./gemm-hip
~~~

可传矩阵大小：

~~~bash
./gemm-cuda 1024
./gemm-cuda 2048
./gemm-cuda 4096
~~~

建议先 1024 验证，再使用 2048 获得更稳定 timing。

## 程序输出

每个 kernel 会报告：

- tile / block size
- static shared/LDS bytes per block
- occupancy API 推导的 active blocks per SM/CU
- 近似 thread occupancy
- average kernel time
- GFLOP/s
- correctness max absolute error

测试：
- naive 16×16 block
- tiled 8
- tiled 16
- tiled 32（如果设备 thread/block 与 shared-memory 限制允许）

## 预期形状，不预期固定速度比

你应该寻找的是 trade-off，不是答案表。

可能出现：

### tiled 比 naive 快

可能原因：
- A/B global loads 被 shared/LDS reuse；
- global traffic 降低；
- access pattern/coalescing 更好；
- arithmetic intensity 提升。

### tile 16 比 tile 8 快

可能原因：
- reuse 更高；
- 每个 tile 的固定同步/调度开销摊得更薄。

### tile 32 不如 tile 16

可能原因：
- 1024 threads/block 太重；
- resident blocks 降低；
- register/shared footprint 或其他资源限制；
- 当前 problem size 的 tile-level parallelism 降低；
- bank/layout/同步成本；
- 编译器代码生成差异。

### naive 意外接近 tiled

可能原因：
- cache/broadcast 已经帮 naive 减少实际 DRAM traffic；
- problem 太小；
- tiled 同步成本明显；
- 当前 GPU memory system 足够强；
- 编译器优化改变了实际访问；
- 实验进入其他 bottleneck。

不要先猜，去 profile。

## Profiler

### NVIDIA

推荐 Nsight Compute。

先看：
- achieved occupancy
- DRAM / L2 / L1 traffic
- global load efficiency / memory workload
- shared-memory throughput
- bank-conflict indicators
- scheduler stall reasons
- registers per thread / local-memory spill

metric 名会随 Nsight Compute 和 GPU 架构变化，因此课程不固定某个 raw metric 名。

### AMD

可先：

~~~bash
rocprofv3 --sys-trace -- ./gemm-hip 2048
~~~

再根据当前 ROCm Compute Profiler / rocprofv3 文档采集：
- VGPR / SGPR
- LDS
- scratch
- occupancy
- cache / memory counters
- wavefront activity

编译阶段的：

~~~bash
hipcc --resource-usage ...
~~~

也应保存进 Evidence。

## Benchmark 纪律

至少：

1. GPU 空闲、固定同一 power/clock policy（如果你知道如何安全设置；否则记录默认状态）。
2. 每种 kernel 先 warm-up。
3. 记录不少于 5 次 stable timing。
4. 相同 N、相同 datatype、相同输入。
5. 不把 host↔device memcpy 时间混进 kernel time。
6. 保存 compiler resource report。
7. 如果比较 NVIDIA vs AMD，不能只比一个 GFLOP/s；必须记录架构、工具链和 tile/config。

## Evidence

提交完整 Experiment Card：

- GPU 型号 / 架构
- VRAM
- driver
- CUDA/ROCm
- compiler version
- N
- tile size
- block size
- registers / VGPR / SGPR
- shared/LDS per block
- active blocks per SM/CU
- occupancy
- kernel time
- GFLOP/s
- correctness
- profiler evidence
- 对异常结果的解释

最后回答：

**如果 tile 32 global-memory traffic 更少，但 GFLOP/s 比 tile 16 低，你会优先检查哪几类资源，为什么？**


## Hypothesis

tiled GEMM 有机会通过 shared/LDS reuse 减少高成本数据移动，但 tile 越大并不保证越快，因为 threads/block、shared/LDS、register pressure、residency 与同步成本会一起变化。

## Fixed variables

同一 GPU/compiler/N/dtype/input 固定；比较 kernel/tile 时不把 H2D/D2H copy 混进 timing。

## What to observe

- correctness；
- kernel time/GFLOP/s；
- shared/LDS per block；
- active blocks/occupancy；
- compiler register/VGPR/SGPR；
- profiler memory/cache/bank/stall；
- tile 8/16/32 的 tradeoff。

## Troubleshooting

- problem 太小会被 cache/launch 影响。
- tile32 可能触及 thread/block 限制。
- naive 接近 tiled 时不要先判 kernel 错，先查 actual traffic/cache。
- 跨 NVIDIA/AMD 不只比单一 GFLOP/s。

## What this proves

你能把真实 tiling speedup 或 slowdown 解释为 data reuse 与片上资源之间的 tradeoff。

## What this does NOT prove

它不是厂商 GEMM library benchmark，也不能推广成所有矩阵 shape 的最佳 tile。

## No-hardware fallback

完成 Experiment 04。

## Transfer question

tile32 的 global traffic 更少但 GFLOP/s 更低时，为什么“流量更少”仍不足以判定它应该更快？

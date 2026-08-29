# Experiment 03 — 真实 GPU：改变片上资源占用，观察 latency-hiding sensitivity

Hardware level: L2  
Risk: safe  
Cost: 已有独显时为 0  
平台：Linux 优先  
支持路径：NVIDIA CUDA 或 AMD HIP/ROCm  
替代路径：没有可用独显/工具链时完成 Experiment 02 L0，不影响继续课程。

## 问题

如果保持同一个 memory-latency-heavy kernel 的核心逻辑不变，只增加每个 block 的 dynamic shared memory / LDS 预留量，使一个 SM/CU 能同时驻留的 blocks 变少：

- theoretical active blocks per SM/CU 会不会下降？
- throughput 会不会下降？
- 什么时候 occupancy 已经足够，继续增加 residency 不再明显改善结果？

NVIDIA Best Practices 明确建议可以通过增加 dynamic shared memory、在不改 kernel 算法的情况下压低 occupancy，再测性能敏感性。这个实验把该方法做成 CUDA/HIP 双路径。

## Kernel 设计

latency_hiding_gpu.cpp 中每个 thread 做一条 dependent pointer chain：

~~~text
idx = next[idx]
idx = next[idx]
idx = next[idx]
...
~~~

下一次 load 必须等待上一次 load 得到 idx，因此单个 thread 内没有足够 memory-level parallelism 可以把依赖链展开。

大量 warps/wavefronts 同时 resident 时，scheduler 才有机会在某个 group 等数据时运行另一个 ready group。

数组默认 2^24 个 uint32_t（64 MiB），并用奇数 stride 构造完整环，尽量让工作集大于许多 GPU 的低级 cache。它仍然不是纯 HBM-latency 测量；cache、coalescing 和架构都会影响结果。

## 编译

### NVIDIA CUDA

~~~bash
nvcc -O3 -std=c++17 -x cu latency_hiding_gpu.cpp -o latency-hiding-cuda
~~~

### AMD HIP / ROCm

~~~bash
hipcc -O3 -std=c++17 latency_hiding_gpu.cpp -o latency-hiding-hip
~~~

## 运行

默认工作集 64 MiB，每 thread 128 次 dependent loads：

~~~bash
./latency-hiding-cuda
# 或
./latency-hiding-hip
~~~

可选参数：

~~~bash
./latency-hiding-cuda 22 256
# 参数1：数组元素数 = 2^22
# 参数2：每 thread dependent-load steps = 256
~~~

显存很小的卡可把第一个参数降到 20–22。

## 程序会做什么

程序会打印：

- device name
- SM/CU 数
- warpSize
- max threads per SM/CU
- shared memory/LDS per block
- 对 0 / 8 / 16 / 24 / 32 KiB dynamic shared memory 的：
  - occupancy API 推导的 active blocks per SM/CU
  - 近似 thread occupancy
  - kernel time
  - dependent global-load throughput

如果某个 dynamic shared memory 值超过设备 per-block 上限，会自动跳过。

## 记录环境

### NVIDIA

~~~bash
nvidia-smi -L
nvcc --version
~~~

可选 profiler：用 Nsight Compute 的 Occupancy 与 scheduler/warp-stall 相关 section 验证 active residency 和 stall 原因。不同版本 metric 名可能变化，不在本课程把某个 metric 名写死。

### AMD

~~~bash
rocminfo
hipcc --version
~~~

可选 profiler：

~~~bash
rocprofv3 --occupancy ./latency-hiding-hip
~~~

如果你的 ROCm 版本参数不同，以当前官方文档为准。

## 预期形状，不预期固定数字

你不应该期待课程给出一组“正确 GB/s”。

更有价值的是曲线与解释：

1. dynamic shared memory/LDS 增加后，active blocks per SM/CU 可能在某些阈值下降。
2. 如果 kernel 依赖很多 resident groups 隐藏 memory latency，residency 大幅下降后 throughput 往往会受损。
3. 如果 occupancy 已经足够，继续提高 resident groups 可能几乎没有收益。
4. 如果结果与预期相反，先看 profiler：可能 cache、bandwidth、register limit、编译器或其他 pipeline 已成为主导因素。

## 重要限制

- 这是 occupancy sensitivity experiment，不是纯粹、隔离的“显存 latency 仪”。
- dynamic shared memory/LDS 不仅影响 occupancy；在某些架构上它还可能与其他片上资源配置发生耦合。
- pointer chain 访问仍受 cache 和 coalescing 影响。
- 不同架构的 scheduler、Wave32/Wave64、register allocation 和 shared-memory/LDS 容量不同，不能直接比较绝对数值。

## Evidence

提交完整 Experiment Card，至少记录：

- GPU 精确型号与架构
- driver + CUDA/ROCm 版本
- 编译器版本
- warpSize
- block size / grid size
- dynamic shared memory/LDS
- occupancy API 给出的 active blocks
- 每个配置的 5 次以上稳定 timing
- profiler 结果（如果可用）
- 对异常点的解释

最后回答：

**如果 32 KiB 配置 occupancy 更低却反而更快，你下一步会查什么，而不是直接宣布“occupancy 没用”？**


## Hypothesis

只增加 dynamic shared memory/LDS、让 active blocks 下降时，若 kernel 依赖多 resident groups 隐藏 dependent-load latency，吞吐应在 residency 低到不足时下降；但 occupancy 足够后继续增加不会线性增益。

## Fixed variables

同一 binary、GPU、array size、dependent-load steps、block/grid 与 power/thermal state固定；只改变 dynamic shared/LDS reservation。

## What to observe

- active blocks/SM-CU 与近似 occupancy；
- kernel time / dependent-load throughput；
- residency threshold 前后的性能敏感性；
- profiler stall/cache/register 线索；
- 低 occupancy 却更快的异常点。

## Troubleshooting

- dynamic shared memory 也可能耦合其他片上配置。
- pointer chain 仍受 cache/coalescing 影响。
- 不同架构绝对 occupancy 数不可直接横比。
- 异常结果先 profile，不要反推“occupancy 无用”。

## What this proves

你能在真实 GPU 上做 occupancy/residency sensitivity 实验，并把 latency hiding 当机制而非口号。

## What this does NOT prove

它不是纯 HBM latency 测量，也不能给出通用最佳 occupancy。

## No-hardware fallback

完成 Experiment 02。

## Transfer question

32KiB shared 配置 occupancy 更低却更快时，哪几类资源/缓存/代码生成证据最值得先查？

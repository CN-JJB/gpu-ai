# Experiment 07 — 真实 GPU：Memory → Compute Arithmetic-Intensity Sweep

Hardware level: L2  
Risk: safe  
Cost: 已有独显时为 0  
平台：Linux 优先  
支持：NVIDIA CUDA / AMD HIP  
替代路径：完成 Experiment 06 L0。

## 问题

能不能在同一张真实 GPU 上构造一组 kernel：

- 每个 element 都读相同数量 global bytes；
- 但逐步增加 register 内 FMA work；
- 从 memory-heavy 一路走到 compute-heavy；

然后观察：

~~~text
arithmetic intensity ↑
→ effective bandwidth / GFLOP/s 如何变化
→ 什么时候开始不再随 AI 线性增长
~~~

这就是一个最小 empirical Roofline probe。

## Kernel family

每个 mixed kernel：

1. 从 global memory 读取 x 和 y；
2. 在 registers 中保持 4 个 accumulator；
3. 重复执行 FMA；
4. 写一个结果回 global memory。

Useful bytes / element：

~~~text
read x: 4 B
read y: 4 B
write out: 4 B
total: 12 B
~~~

每个 repeat 有 4 个 FMA：

~~~text
4 FMA × 2 FLOP = 8 FLOP
~~~

所以概念 AI：

~~~text
AI = 8 × repeats / 12
~~~

测试：

| repeats | nominal AI |
|---:|---:|
| 1 | 0.667 FLOP/B |
| 4 | 2.667 |
| 16 | 10.667 |
| 64 | 42.667 |
| 256 | 170.667 |

另外程序会跑一个低-work triad 作为 memory-heavy baseline。

## 为什么不叫“峰值带宽/峰值算力测试”？

因为这个课程实验不是厂商认证 microbenchmark。

结果会受：
- compiler code generation；
- cache；
- clocks/power；
- instruction mix；
- FMA dependency/ILP；
- occupancy/register pressure；
- launch size；
- architecture。

所以我们只称：
- achieved effective bandwidth；
- achieved GFLOP/s；
- empirical crossover。

不要把结果替代官方 peak specs。

## 工作集大小

程序会查询 free GPU memory，并尝试选择一个较大的工作集，让 x/y/out 明显大于常见 cache，同时不吃掉太多显存。

默认目标：
- 最多约 64M FP32 elements；
- 总三数组约 768 MiB；
- 小显存卡会自动下降；
- 最少约 4M elements。

程序会打印实际 elements 与 MiB。

## 编译

### NVIDIA

~~~bash
nvcc -O3 -std=c++17 -x cu -res-usage \
  roofline_probe.cpp -o roofline-cuda
~~~

### AMD

~~~bash
hipcc -O3 -std=c++17 --resource-usage \
  roofline_probe.cpp -o roofline-hip
~~~

## 运行

~~~bash
./roofline-cuda
# 或
./roofline-hip
~~~

可选手动指定 elements：

~~~bash
./roofline-cuda 16777216
~~~

## 输出

每个 point 记录：

- repeats
- nominal AI
- kernel time
- useful effective bandwidth
- achieved GFLOP/s
- correctness checksum/sample

## 你应该找“形状”

低 AI：
- GFLOP/s 往往随着 AI 增加而明显上升；
- useful bandwidth 可能比较高。

AI 继续上升：
- GFLOP/s 增长开始变慢；
- effective GB/s 可能下降；
- kernel 更接近 compute-side limitation。

这就是 empirical crossover。

不要期待每张 GPU 的转折都在同一个 AI。

## NVIDIA profiler

Nsight Compute 可直接看 Roofline chart。

建议保存：
- Roofline chart；
- DRAM throughput；
- L2 traffic；
- achieved occupancy；
- registers；
- scheduler stall summary。

## AMD profiler

ROCm Compute Profiler 支持 per-kernel / hierarchical roofline。

当前版本可参考：

~~~bash
rocprof-compute profile --name roof-probe --roof-only -- ./roofline-hip
rocprof-compute analyze -p workloads/roof-probe/... -b 4
~~~

具体输出路径和参数以当前安装版本为准。

它可以分别分析 HBM/L2/L1/LDS roofs。

## Benchmark 纪律

- 记录 GPU exact model / architecture。
- 记录 driver、CUDA/ROCm、compiler。
- 记录 power/clock policy。
- warm-up。
- 每个 point 至少 5 次。
- 不把 H2D/D2H copy 算进 kernel timing。
- workload size 必须记录。
- 保存 compiler resource usage。
- 如果 profiler 的 actual DRAM bytes 和 12 B/element useful bytes 差很多，要解释 cache/transaction effects。

## Evidence

提交 Experiment Card，并画出：

~~~text
x = nominal AI
y = achieved GFLOP/s
~~~

至少标出：
- low-AI memory-heavy point；
- crossover；
- high-AI compute-heavy point。

最后回答：

**如果两张卡的 high-AI point 差很多，但 low-AI point 几乎一样，你会如何解释它们的 compute/bandwidth balance？**


## Hypothesis

在同一真实 GPU 上增加 register-local FMA work、保持 useful global bytes 近似固定，应让低 AI point 更像 memory-side limitation，高 AI point 更接近 compute-side limitation；empirical crossover 由真实实现决定。

## Fixed variables

同一 GPU/compiler/build/workset/power-clock policy 固定，只改变 repeats/nominal AI。手动改变 elements 时另开实验记录。

## What to observe

- low-AI achieved effective bandwidth；
- high-AI achieved GFLOP/s；
- crossover 形状；
- compiler resource usage/register pressure；
- profiler actual traffic 与 12B/element useful-byte proxy 的差异；
- 多次运行稳定性。

## Troubleshooting

- useful bytes 不是 actual DRAM transaction bytes。
- 工作集过小会更受 cache 影响。
- repeats 增大可能改变 register pressure/occupancy。
- profiler/driver 版本差异要记录。
- 不把结果替代官方 peak specs。

## Evidence to save

保存 binary/compiler command、resource usage、完整输出、GPU/runtime identity；有 profiler 时保存 roofline/traffic/stall evidence。

## What this proves

你能在真实 GPU 上观察 arithmetic-intensity sweep 的经验形状，并把它与理论 Roofline 联系起来。

## What this does NOT prove

它不是厂商峰值认证，也不直接预测 LLM TG。

## No-hardware fallback

完成 Experiment 06。

## Transfer question

两张卡 low-AI point 接近而 high-AI point 差很大，这更像说明它们哪一类资源差异更明显？

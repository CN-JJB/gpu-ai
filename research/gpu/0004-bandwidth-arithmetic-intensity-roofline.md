# Research Note 0004 — Bandwidth、Arithmetic Intensity 与 Roofline

日期：2026-08-26

## Research question

为什么“峰值 TFLOPS 更高”不保证某个 GPU workload 更快？显存/内存带宽、effective bandwidth、arithmetic intensity、cache/reuse 与 compute throughput 如何共同决定 kernel 的性能上限？这个模型如何用于解释本地 LLM 的 prefill、decode、量化与 KV/cache traffic？

## Scope

本笔记建立最小 Roofline 心智模型，并把上一切片的 tiling/data reuse 接到硬件选择。

稳定主线：

global memory traffic
→ achieved/effective bandwidth
→ arithmetic intensity
→ memory-bound / compute-bound
→ ridge point
→ hardware choice / kernel optimization

不在稳定 Lesson 中写死当前型号排名、价格、某后端 tokens/s 或特定 GPU 的营销峰值数字；这些属于后续 intelligence / benchmark。

## Primary sources

1. NVIDIA CUDA C++ Best Practices Guide — Bandwidth  
   https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/  
   支撑：
   - bandwidth 是关键性能门槛；
   - 区分 theoretical bandwidth 与 effective bandwidth；
   - effective bandwidth = 实际算法读写 bytes / elapsed time；
   - requested/effective traffic 与 actual DRAM transaction traffic 不一定相同；
   - coalescing 和 memory layout 会影响实际带宽利用。

2. NVIDIA Nsight Compute Profiling Guide — Roofline Charts  
   https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html  
   支撑：
   - Roofline 结合 peak compute、memory bandwidth 与 arithmetic intensity；
   - x 轴是 FLOP/byte；
   - memory roof 为斜线，compute roof 为水平线；
   - ridge point 划分 memory-bound 与 compute-bound 区域；
   - 若 kernel 已贴近 memory roof，要继续提高 FLOP/s 通常需要提高 arithmetic intensity。

3. NVIDIA GPU Performance Background  
   https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html  
   支撑：
   - math time ≈ operations / math bandwidth；
   - memory time ≈ bytes / memory bandwidth；
   - arithmetic intensity = operations / bytes；
   - processor compute-to-memory ratio 决定 workload 何时从 memory-limited 变为 math-limited。

4. NVIDIA Matrix Multiplication Background  
   https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html  
   支撑：
   - GEMM 通过 tiling 提高 data reuse；
   - larger tiles 通常降低 bandwidth demand；
   - arithmetic intensity 与 problem/tile shape 紧密相关。

5. AMD ROCm HIP — Understanding GPU performance  
   https://rocm.docs.amd.com/projects/HIP/en/latest/understand/performance_optimization.html  
   支撑：
   - arithmetic intensity = FLOPs / bytes transferred；
   - compute roof 与 memory roof；
   - ridge point；
   - memory-bound / compute-bound 判定；
   - Roofline deliberately ignores latency，强调 throughput ceilings；
   - occupancy、register/LDS 等仍会让 achieved performance 低于 roof。

6. AMD ROCm HIP — Performance guidelines  
   https://rocm.docs.amd.com/projects/HIP/en/latest/how-to/performance_guidelines.html  
   支撑：
   - global-memory throughput 对性能重要；
   - 应减少 host-device transfers；
   - on-chip memory、cache、coalescing 会改变 effective bandwidth。

7. AMD ROCm Compute Profiler — Roofline analysis  
   https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/how-to/analyze/cli.html  
   支撑：
   - per-kernel roofline；
   - memory chart；
   - hierarchical roofline 可分别看 HBM/L2/L1/LDS 等层级；
   - arithmetic intensity 可以相对不同 memory level 分析，不只一个“总 AI”。

8. NVIDIA Dynamo — Disaggregated Serving  
   https://docs.nvidia.com/dynamo/dev/knowledge-base/concepts/system-architecture/disaggregated-serving  
   支撑：
   - LLM prefill 与 decode 有不同计算特征；
   - prefill 通常偏 compute-bound；
   - decode 通常偏 memory-bound；
   - 因此不同阶段可采用不同硬件/并行策略。

9. AMD Infera Glossary — Prefill / Decode  
   https://rocm.docs.amd.com/projects/infera/en/latest/reference/glossary.html  
   支撑：
   - AMD 官方同样把 prefill 描述为 compute-bound、decode 描述为 memory-bandwidth-bound，且 decode 性能随 concurrency 改变。

## Findings

### F1 — Capacity、bandwidth、compute 是三个不同维度

垃圾佬常把“显存”当成一个指标，但至少要拆成：

**VRAM/HBM capacity**
- 能不能放下 model weights、KV cache、context、batch、中间 buffers；
- 单位：GB。

**Memory bandwidth**
- 每秒能在 GPU memory subsystem 与计算单元之间移动多少 bytes；
- 单位：GB/s 或 TB/s。

**Compute throughput**
- 每秒能执行多少目标 datatype 的算术操作；
- 单位：FLOP/s、OPS/s 等。

容量大不代表带宽高，带宽高也不等于算力高。

### F2 — Theoretical bandwidth 不是 achieved bandwidth

产品规格给的是理论上限。

真实 kernel 的 achieved/effective bandwidth 受到：
- access pattern；
- coalescing；
- cache hit/miss；
- transaction utilization；
- controller efficiency；
- contention；
- ECC/architecture details；
- workload size；
- profiler measurement method。

NVIDIA Best Practices 明确建议计算 effective bandwidth，并把它与 theoretical bandwidth 比较。

### F3 — Effective bandwidth 要先定义“你数的 bytes”

最简单的 copy kernel：

read N bytes
+ write N bytes
→ useful traffic = 2N bytes。

effective bandwidth：

useful bytes / kernel time。

但 profiler 看到的 actual DRAM bytes 可能更多或更少：
- transaction granularity 会搬没用到的 bytes；
- cache hit 会阻止请求下到 DRAM；
- writeback / protocol / ECC 等也会改变实际流量。

所以 benchmark 必须写清：
- requested/useful bytes；
- measured DRAM bytes（若有 profiler）；
- elapsed time。

### F4 — Arithmetic intensity 是“每搬一 byte 做多少工作”

定义：

AI = FLOPs / bytes transferred

低 AI：
- 每 byte 只做少量算术；
- 更容易 memory-bound。

高 AI：
- 同一数据被重复使用很多次；
- 更容易 compute-bound。

上一切片的 tiling 本质就是：

global bytes ↓
FLOPs 不变
→ AI ↑

### F5 — Roofline 只需要两个硬件上限和一个 workload 属性

最小模型：

memory-limited throughput = bandwidth × AI

compute-limited throughput = peak/achieved compute roof

所以：

achievable throughput ≤ min(compute roof, bandwidth × AI)

ridge point：

AI_ridge = compute throughput / memory bandwidth

当：
- AI < ridge → memory-side roof 更低；
- AI > ridge → compute roof 更低。

### F6 — “更多 TFLOPS”可能把 ridge 推得更右

假设抽象 GPU：

20 TFLOP/s + 500 GB/s
→ ridge = 40 FLOP/B。

如果只把 compute 翻倍：

40 TFLOP/s + 500 GB/s
→ ridge = 80 FLOP/B。

对一个 AI=4 FLOP/B 的 workload：
- 原来上限 = 2 TFLOP/s；
- 算力翻倍后仍 = 2 TFLOP/s。

因为 memory roof 没变。

这就是为什么单看 compute marketing number 会误判低-AI workload。

### F7 — “更多带宽”对低-AI workload 更直接

同样把：

20 TFLOP/s + 500 GB/s

改成：

20 TFLOP/s + 1000 GB/s

ridge 从 40 降到 20 FLOP/B。

AI=4 的 workload 上限从 2 TFLOP/s 变成 4 TFLOP/s。

但 AI=80 的 compute-bound workload 仍被 20 TFLOP/s compute roof 卡住。

### F8 — Cache 不是“额外带宽数字”，而是改变远端 traffic

同一个 kernel 可以有多个 Roofline 视角：

- relative to HBM/VRAM；
- relative to L2；
- relative to L1；
- relative to shared/LDS。

AMD ROCm Compute Profiler 甚至提供 hierarchical roofline。

如果某数据在 L2 命中：
- 对 HBM 来说 bytes 减少；
- HBM-level arithmetic intensity 上升；
- 但 L2 仍需要供给 bytes。

因此“cache 命中率高”最终要翻译成：
**减少了哪个更远 memory level 的 traffic？**

### F9 — Roofline 是 throughput model，不解释所有 latency

AMD 官方文档明确提醒：Roofline deliberately ignores latency。

一个 kernel 即使理论上处在 memory-bound 区，也可能因为：
- insufficient occupancy；
- dependency chain；
- scheduler stalls；
- divergence；
- launch overhead；
- poor coalescing；
- bank conflicts

远低于 memory roof。

所以：
execution-model slice 解释 latency hiding；
memory/tiling slice 解释 reuse；
Roofline slice 解释 throughput ceiling。

三者不能互相替代。

### F10 — Prefill 与 decode 是本地 LLM 中最重要的 workload split 之一

官方 NVIDIA Dynamo 与 AMD Infera 都给出稳定抽象：

**Prefill**
- 一次处理较多 input tokens；
- 大 GEMM/矩阵工作更容易形成高并行和高 reuse；
- 通常更偏 compute-bound。

**Decode**
- autoregressive token-by-token；
- 单步工作并行度与 reuse 条件不同；
- 需要反复访问 weights，并随 context/batch 访问 KV state；
- 通常更偏 memory-bandwidth-bound。

这是“通常”，不是绝对规则。
batch size、concurrency、model architecture、context length、quantization、backend、kernel fusion、cache strategy 都会移动实际 AI 和 bottleneck。

### F11 — Quantization 同时影响 capacity 与 bandwidth pressure

若把 weight representation 从更多 bits 降到更少 bits：

- capacity footprint ↓；
- 每次扫 weights 的 bytes ↓；
- memory-bound phase 的 effective arithmetic intensity 可能 ↑；
- 相同 raw bandwidth 可以服务更多 useful weights/s。

但代价可能包括：
- dequantization compute；
- scale/metadata traffic；
- packing/unpacking；
- kernel/backend 是否有高效低精度 path；
- quality trade-off。

所以“4-bit = 4× faster”不是稳定结论。

### F12 — KV cache 把“模型权重带宽”问题扩展成“状态带宽”问题

decode 不是只搬 weights。

随着：
- context length ↑；
- batch/concurrency ↑；

KV traffic 和 capacity 都可能变得重要。

后续 LLM slice 会单独推导 KV cache size 与 access pattern；本切片只建立：
**bytes/token 不只来自 weights。**

## Stable hardware-choice model

选卡时不要问：

> 哪张卡 TFLOPS 高？

改问：

1. workload 的 AI 大概在哪个区间？
2. 是 decode-heavy 还是 prefill-heavy？
3. model + KV 是否 fit？
4. 目标 datatype 的实际 compute roof 是多少？
5. memory bandwidth 是多少？
6. backend 能达到多少 achieved bandwidth / compute？
7. quantization 会减少多少 bytes，又增加多少额外 work？
8. 多 GPU 后还会不会被 PCIe/interconnect 卡住？

## Claims to avoid

- “显存越大一定越快。”
- “显存带宽越高所有 workload 都越快。”
- “TFLOPS 越高 LLM tokens/s 一定越高。”
- “decode 永远只受显存带宽限制。”
- “prefill 永远 compute-bound。”
- “4-bit 权重一定带来 4× tokens/s。”
- “theoretical bandwidth 就是 kernel 能用到的 bandwidth。”
- “Roofline 能解释所有 latency/stall。”

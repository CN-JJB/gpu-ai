# GPU Bandwidth / Roofline / LLM Bottleneck 速查

<figure>
  <img src="../../assets/diagrams/foundation-units-roof-estimation.svg" alt="GPU Bandwidth / Roofline / LLM Bottleneck 速查 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 GPU Bandwidth / Roofline / LLM Bottleneck 速查 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 三个先拆开的硬件指标

| 指标 | 回答什么 | 常见单位 |
|---|---|---|
| VRAM/HBM capacity | 能不能放下 weights、KV、context、buffers | GB |
| memory bandwidth | 每秒能搬多少数据 | GB/s、TB/s |
| compute throughput | 每秒能做多少目标 datatype 运算 | TFLOP/s、TOPS |

**容量 ≠ 带宽 ≠ 算力。**

## Effective bandwidth

概念公式：

effective bandwidth = useful bytes transferred / kernel time

例如 copy N bytes：

read N
+ write N
= 2N useful bytes

但 profiler 的 actual DRAM bytes 可能不同，因为：
- cache；
- transaction granularity；
- coalescing；
- writeback；
- ECC/protocol；
- access pattern。

所以 Experiment Card 要区分：
- useful/requested bytes；
- profiler actual traffic；
- elapsed time。

## Arithmetic Intensity

AI = FLOPs / bytes transferred

单位：

FLOP/B

低 AI：
→ memory roof 容易先撞到

高 AI：
→ compute roof 容易先撞到

## 最小 Roofline

memory roof:

performance = bandwidth × AI

compute roof:

performance = compute ceiling

所以：

performance ≤ min(compute ceiling, bandwidth × AI)

## Ridge point

AI_ridge = compute throughput / memory bandwidth

注意单位转换：

如果 compute 用 TFLOP/s，bandwidth 用 GB/s：

AI_ridge = TFLOP/s × 1000 / GB/s

例：

20 TFLOP/s / 500 GB/s
→ 40 FLOP/B

## L0 抽象比较

### GPU A

20 TFLOP/s  
500 GB/s  
ridge = 40 FLOP/B

### GPU B：只加算力

40 TFLOP/s  
500 GB/s  
ridge = 80 FLOP/B

### GPU C：只加带宽

20 TFLOP/s  
1000 GB/s  
ridge = 20 FLOP/B

| AI | GPU A | GPU B | GPU C |
|---:|---:|---:|---:|
| 0.25 | 0.125 TFLOP/s | 0.125 | 0.250 |
| 1 | 0.5 | 0.5 | 1.0 |
| 4 | 2.0 | 2.0 | 4.0 |
| 16 | 8.0 | 8.0 | 16.0 |
| 40 | 20.0 | 20.0 | 20.0 |
| 80 | 20.0 | 40.0 | 20.0 |

结论：

- 低 AI：加 bandwidth 有直接收益；只加 compute 可能没用。
- 高 AI：加 compute 才有机会继续涨；bandwidth 提升可能无效。

## Tiling 为什么重要

上一切片：

tile reuse ↑
→ global bytes ↓
→ AI ↑
→ workload 在 Roofline 图上往右移动

所以 tile 优化不只是“shared memory 更快”。

它可以改变 workload 属于 memory-bound 还是 compute-bound。

## Cache 怎么放进模型

不是只有一条 memory roof。

可以分别问：

- HBM/VRAM AI
- L2 AI
- L1 AI
- shared/LDS AI

cache hit 的价值：
→ 减少更远层级 traffic
→ 提高相对该远端层级的 AI

AMD ROCm Compute Profiler 支持 hierarchical roofline，就是这个思路。

## Roofline 不回答什么

它主要是 throughput ceiling model，不直接解释：

- dependency latency
- insufficient resident warps
- divergence
- scheduler issue stalls
- launch overhead
- bank conflicts

这些要和前两片 execution model / occupancy 一起看。

## LLM 映射

### Prefill

通常：
- 大量 input tokens 同时处理；
- 大 GEMM；
- parallelism/reuse 较高；
- 更偏 compute-bound。

### Decode

通常：
- token-by-token；
- 每步需访问 weights；
- context/batch 增大时还有 KV traffic；
- 更偏 memory-bandwidth-bound。

不是绝对规则。

### Quantization

可能同时：
- model capacity footprint ↓
- bytes per weight ↓
- memory pressure ↓
- AI ↑

但还要看：
- dequant compute
- scales/metadata
- low-bit kernel support
- matrix hardware support
- quality

## 垃圾佬选卡检查顺序

1. model + KV + buffers 能不能 fit？
2. 主要 workload 是 prefill 还是 decode？
3. 目标 precision/quantization 的 compute path 真能用吗？
4. raw memory bandwidth 多大？
5. achieved bandwidth 有多少？
6. workload AI 大概多高？
7. ridge point 在哪里？
8. bottleneck 是 memory roof、compute roof，还是根本没贴近任何 roof？
9. 多 GPU 时 interconnect 会不会变成新的 bandwidth roof？

## 常见误判

- 大显存 ≠ 高带宽
- 高带宽 ≠ 高算力
- 高 TFLOPS ≠ 高 decode tokens/s
- 高 theoretical bandwidth ≠ 高 achieved bandwidth
- memory-bound ≠ “GPU utilization 一定低”
- compute-bound ≠ “显存不重要”

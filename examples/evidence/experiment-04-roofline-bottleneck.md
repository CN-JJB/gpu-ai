---
experiment_id: example-roofline-bottleneck-model
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

当 GPU 只增加 compute throughput 或只增加 memory bandwidth 时，不同 arithmetic intensity 的 workload 哪些会得到加速？

## Hardware

无特殊硬件；Python 运行抽象 Roofline 模型。

## Software

Python 3。

## Configuration

GPU A：
- 20 TFLOP/s
- 500 GB/s

GPU B：
- 40 TFLOP/s
- 500 GB/s

GPU C：
- 20 TFLOP/s
- 1000 GB/s

AI：
- 0.25
- 1
- 4
- 16
- 40
- 80
- 160 FLOP/B

## Procedure

运行：

~~~bash
python labs/experiments/06-roofline-bottleneck-model/simulate.py
~~~

## Results

GPU A ridge = 40 FLOP/B。  
GPU B ridge = 80 FLOP/B。  
GPU C ridge = 20 FLOP/B。

关键对比：

### AI=4

- GPU A：2 TFLOP/s
- GPU B：2 TFLOP/s
- GPU C：4 TFLOP/s

### AI=80

- GPU A：20 TFLOP/s
- GPU B：40 TFLOP/s
- GPU C：20 TFLOP/s

## Observations

低-AI workload 被 bandwidth × AI 限制。

因此只增加 compute roof，memory roof 不动，性能上限也不动。

高-AI workload 已经跨过 ridge，则 compute roof 成为限制；此时只增加 memory bandwidth 不会继续提高上限。

## Conclusion

硬件选择必须匹配 workload arithmetic intensity。

**TFLOPS、bandwidth、capacity 不是能合成一个简单“显卡强度分数”的三个数字。**

上一切片的 tiling/data reuse 会减少 global bytes、提高 AI，相当于把 workload 在 Roofline 图上往右推；跨过 ridge 后，优化重点才从 memory system 转向 compute pipelines。

## Reproducibility

见：
- labs/experiments/06-roofline-bottleneck-model/simulate.py
- labs/experiments/06-roofline-bottleneck-model/EXPECTED.md

## LLM transfer

对于典型本地 LLM：
- prefill 通常更偏 compute-bound；
- decode 通常更偏 memory-bandwidth-bound。

但具体结论必须带 batch、context、quantization、model/backend 与 hardware 条件。

## Sources

- NVIDIA Nsight Compute — Roofline
- NVIDIA GPU Performance Background
- AMD ROCm — Understanding GPU performance
- NVIDIA Dynamo — Disaggregated Serving
- AMD Infera — Prefill / Decode

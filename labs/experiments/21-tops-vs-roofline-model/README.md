# Experiment 21 — Why TOPS Does Not Equal LLM Speed

硬件等级：L0

这是 synthetic Roofline teaching model，不使用任何真实 GPU 峰值。

## 目标

分清：

```
advertised compute peak
vs
workload utilization
vs
memory roof
vs
conversion/dequant overhead
```

## 默认 synthetic compute paths

- fp32
- fp16_matrix
- int8_matrix
- int4_native
- q4_weight_only

其中：

```
q4_weight_only
```

故意建模为：
- 4-bit 权重存储；
- 计算仍走 FP16-like matrix peak；
- 额外 dequant overhead。

它用来证明：

```
4-bit storage
!= native INT4 compute
```

## Workload profiles

### prefill-like

高 arithmetic intensity + 较好 matrix utilization。

### decode-like

低 arithmetic intensity + 很差的小-M matrix utilization。

## 公式

```
compute_roof = peak × utilization

memory_roof = bandwidth × arithmetic_intensity

achieved = min(compute_roof, memory_roof)

effective = achieved / (1 + overhead)
```

## 运行

```bash
python3 simulate.py
```

## 思考

1. 哪些 path 在 prefill-like profile 能吃到更高 compute peak？
2. 为什么 decode-like profile 里不同 TOPS 的差距突然缩小？
3. q4_weight_only 为什么可能比 fp16 快，但又远低于“native int4 peak”？
4. 如果 memory bandwidth 翻倍，decode-like 哪些 path 最先受益？


## Why this experiment

“TOPS 很高”最容易被误读成“LLM 一定更快”。这个模型把 compute peak、实际 utilization、memory roof 和 dequant overhead 分开，训练你先看 workload 是否真的能吃到对应硬件路径。

## Hypothesis

Prefill-like workload 因 arithmetic intensity 和 matrix utilization 更高，更容易看到不同 compute path 的峰值差异；decode-like workload 更容易被 memory roof 或低利用率压平。

## Fixed variables

同一 workload profile 下只比较 compute path；比较 prefill/decode 时保持 path 参数不变。

## What to observe

1. compute roof 与 memory roof 哪个更低。
2. q4_weight_only 为什么不是 native INT4 compute。
3. decode-like 下不同 TOPS 差距为何缩小。
4. bandwidth 翻倍后哪些 path 先获益。
5. overhead 如何让 theoretical achieved 与 effective 再分离。

## Troubleshooting

- 不要把 storage bits 与 arithmetic precision 画等号。
- advertised peak 必须绑定 dtype/条件。
- utilization 是 workload/implementation 变量，不是 GPU 固有常数。
- synthetic teaching units 不能当真实 GPU 性能。

## Evidence to save

保存默认输出，再修改一次 bandwidth、一次 utilization，记录 bottleneck roof 如何变化。

## What this proves

你能用 Roofline 思路解释为什么峰值 TOPS 不是 tok/s。

## What this does NOT prove

它不预测任何具体 GPU/backend 的真实利用率、带宽或 TG。

## No-hardware path

完整 L0。

## Transfer question

一张 GPU INT8 TOPS 翻倍，但 decode TG 几乎不变，你会优先怀疑 compute roof 还是 memory/utilization roof？为什么？

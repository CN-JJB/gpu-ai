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

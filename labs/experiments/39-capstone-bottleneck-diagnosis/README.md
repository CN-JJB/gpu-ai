# Experiment 39 — Bottleneck Diagnosis Cases

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/hardware-decision-gates.svg" alt="瓶颈诊断先排 Fit/Support，再结合计算、带宽、容量与软件 Evidence；不要看到慢就先换 GPU。">
  <figcaption>瓶颈诊断先排 Fit/Support，再结合计算、带宽、容量与软件 Evidence；不要看到慢就先换 GPU。</figcaption>
</figure>

## 目标

训练这条链：

```
observed evidence
→ bottleneck hypothesis
→ choose one next variable
```

不是看到任何性能问题都先“开 FlashAttention”。

## 运行

```bash
python3 check_diagnosis.py
```

## Cases

### A — decode near bandwidth roof

- model fully resident
- TG = 18 tok/s
- rough bandwidth roof = 20 tok/s
- PP already strong
- more GPU compute does not change TG

Expected:
```
TG_BANDWIDTH
```

Good next variable:
```
weight_bytes_or_backend
```

### B — prefill weak, TG healthy

- TG healthy
- PP much lower than expected
- large attention/prefill workload
- matrix backend path may be suboptimal

Expected:
```
PP_KERNEL
```

Good next variable:
```
flash_attention_or_backend
```

### C — long context hurts memory and speed

- 4k works well
- 32k nearly fills memory
- TG falls as context grows
- KV footprint matches model prediction

Expected:
```
KV_CONTEXT
```

Good next variable:
```
kv_type_or_context
```

### D — one user fine, concurrent TTFT explodes

Expected:
```
SERVING_QUEUE
```

Good next variable:
```
slots_or_batching
```

### E — two GPUs give 1.05x

- one GPU fits
- tensor split used
- low P2P bandwidth
- communication/sync visible

Expected:
```
INTERCONNECT
```

Good next variable:
```
split_mode_or_device_topology
```

### F — repeated long prefix

- warm repeated prompt has much lower TTFT
- decode phase unchanged

Expected:
```
PREFIX_REUSE
```

Good next variable:
```
prefix_cache
```

### G — low-QPS decode + cheap proposer

- decode-bound target
- free memory headroom
- draft acceptance expected high
- low/medium concurrency

Expected:
```
SPECULATIVE_OPPORTUNITY
```

Good next variable:
```
speculative_decoding
```

## 完成标准

7/7，并且你能解释为什么每个 case 不应该先改另外一个不相关变量。

## Why this experiment

优化最贵的错误是“看到慢就随便开一个热门 feature”。这个实验训练你先从证据形成瓶颈假设，再只选择一个最能区分假设的下一变量。

## Hypothesis

七个 case 的 symptom pattern 应分别支持不同瓶颈方向；正确答案不是记标签，而是能解释为什么其他优化在当前证据下优先级更低。

## Fixed variables

每个 case 的 evidence 原样保留；只选择一个 next variable。不要同时提出五项修改后声称找到了根因。

## What to observe

1. TG 接近 bandwidth roof 与 PP weak 的差异。
2. context/KV 增长与 serving queue 的不同时间模式。
3. multi-GPU 低 scaling 与 interconnect evidence。
4. prefix reuse 只改善 prompt phase 的特征。
5. speculative opportunity 需要哪些前提。

## Troubleshooting

- 任何标签都只是 hypothesis class，不是已证明根因。
- rough roof 接近不等于精确 bandwidth utilization。
- concurrent TTFT 爆炸要先看 queue/deferred，而不是默认 GPU 算力不足。
- 一次只改一个变量，修改后重新测相同指标。

## Evidence to save

保存 7/7 输出，并为每个 case 写：Evidence → Hypothesis → One next variable → Expected discriminating result。

## What this proves

你会把性能诊断转成可证伪的单变量实验。

## What this does NOT prove

synthetic cases 不代表任何真实 GPU/root cause。

## No-hardware path

完整 L0。

## Transfer question

如果 TG 低但模型权重有一部分 CPU offload，你为什么不应该立刻把问题归因于显存带宽？

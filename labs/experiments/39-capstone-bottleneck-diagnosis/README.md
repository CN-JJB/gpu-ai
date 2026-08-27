# Experiment 39 — Bottleneck Diagnosis Cases

硬件等级：L0

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
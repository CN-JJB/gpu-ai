# Expected — Experiment 39

```bash
python3 check_diagnosis.py
```

Expected:

```
score: 7/7
```

Mapping:

| Case | Bottleneck | Next variable |
|---|---|---|
| A | TG_BANDWIDTH | weight_bytes_or_backend |
| B | PP_KERNEL | flash_attention_or_backend |
| C | KV_CONTEXT | kv_type_or_context |
| D | SERVING_QUEUE | slots_or_batching |
| E | INTERCONNECT | split_mode_or_device_topology |
| F | PREFIX_REUSE | prefix_cache |
| G | SPECULATIVE_OPPORTUNITY | speculative_decoding |

## Key lesson

A valid optimization choice starts with:
```
evidence
```
not:
```
popular tweak
```

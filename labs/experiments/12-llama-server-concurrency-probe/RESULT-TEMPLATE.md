---
experiment_id: learner-llama-server-concurrency
date:
hardware_level:
risk_level: safe
status: template-not-result
---

# Question

在固定模型与 server 配置下，client concurrency 从 1→2→4→8 时，queue、TTFT、aggregate throughput 与 busy slots 如何变化？

## Runtime identity

- llama.cpp version/commit:
- llama-server command:
- OS:
- CPU:
- RAM:
- GPU/accelerator:
- driver/backend:

## Model identity

- repository:
- revision:
- filename:
- bytes:
- SHA256:
- architecture:
- parameters:
- GGUF quant:

## Server config

- slots / parallel:
- continuous batching:
- context:
- batch / ubatch:
- GPU layers/offload:
- KV K type:
- KV V type:
- Flash Attention:
- prompt cache:
- unified KV:
- other relevant flags:

## Workload

- total requests:
- concurrency sweep:
- prompt:
- max output tokens:
- seed:
- warm-up:
- monitor interval:

## Results

| concurrency | wall s | TTFT mean | TTFT p95 | E2E mean | stream-gap proxy | wall output t/s | server pred t/s | peak processing | peak deferred | busy slots/decode |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 8 | | | | | | | | | | |

## Queue evidence

## Batching evidence

## KV / capacity observations

## Unexpected results

## Interpretation

### Latency

### Throughput

### Queue saturation

### Connection to Roofline

### Connection to KV capacity

## Conclusion

## Reproducibility

Attach:

- server startup log
- props.json
- slots-before.json
- concurrency-1.json
- concurrency-2.json
- concurrency-4.json
- concurrency-8.json

## Sources

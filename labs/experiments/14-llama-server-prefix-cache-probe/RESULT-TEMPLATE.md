---
experiment_id: learner-prefix-cache-cold-warm
date:
hardware_level:
risk_level: safe
status: template-not-result
---

# Question

同一长 prefix 的 cold vs warm request，llama-server cache_n / prompt_n / prompt_ms / TTFT 如何变化？

## Runtime

- llama.cpp version/commit:
- server command:
- OS:
- CPU:
- RAM:
- GPU:
- backend/driver:

## Model

- repo/revision:
- filename:
- bytes:
- SHA256:
- quant:
- parameter count:

## Server config

- slots:
- context:
- prompt cache:
- cache reuse:
- cache RAM:
- unified KV:
- KV K/V dtype:
- offload:
- Flash Attention:

## Probe config

- prefix_repeat:
- cold prompt tokens:
- max output tokens:
- seed:
- run id:

## Timings

| case | cache_n | prompt_n | prompt_ms | prompt t/s | predicted_n | predicted_ms | client E2E |
|---|---:|---:|---:|---:|---:|---:|---:|
| cold exact | | | | | | | |
| warm exact | | | | | | | |
| near miss | | | | | | | |

## TTFT

| case | TTFT proxy | E2E | stream-gap proxy |
|---|---:|---:|---:|
| cold | | | |
| warm | | | |

## Observations

## Prefix reuse explanation

## Decode boundary

## Capacity / eviction notes

## Security / tenancy notes

## Unexpected results

## Conclusion

## Reproducibility

Attach:
- server log
- prefix-cache.json
- exact command
- model SHA256

## Sources

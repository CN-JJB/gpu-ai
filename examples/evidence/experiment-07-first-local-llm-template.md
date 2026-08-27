---
experiment_id: learner-first-local-llm
date:
hardware_level:
risk_level: safe
status: template-not-result
---

# Question

同一份本地量化 LLM artifact 在当前机器的 CPU 与可用 accelerator 路径上，能否正确运行？PP/TG 性能与资源配置如何变化？

## Hardware

- CPU:
- RAM:
- GPU / accelerator:
- VRAM / unified memory:
- motherboard / PCIe (if relevant):
- power/thermal notes:

## Software

- OS / kernel:
- driver:
- llama.cpp version / commit:
- build backend:
- compiler/build source:

## Model

- repository:
- revision:
- filename:
- bytes:
- SHA256:
- architecture:
- parameter count:
- GGUF / quant type:

## Configuration

- context:
- threads:
- GPU layers/offload:
- device:
- KV type:
- Flash Attention:
- pp tokens:
- tg tokens:
- repetitions:

## Procedure

## First-generation result

## Raw Results

### CPU

- pp t/s:
- tg t/s:
- stddev:
- raw JSON:

### GPU / hybrid

- pp t/s:
- tg t/s:
- stddev:
- raw JSON:

## Observations

## Unexpected Results / Failures

## Interpretation

- capacity:
- bandwidth/Roofline:
- offload:
- context/KV:
- CPU thread behavior:

## Conclusion

## Reproducibility

Attach:
- env.txt
- startup log
- benchmark JSON
- exact commands

## Sources

---
experiment_id: learner-speculative-decoding
date:
hardware_level:
risk_level: safe
status: template-not-result
---

# Question

Does speculative decoding improve real target decode throughput/latency for this exact model, proposer, workload and concurrency?

## Runtime / hardware

- llama.cpp commit/version:
- OS:
- CPU/RAM:
- GPU/VRAM or unified memory:
- driver/backend:
- power/thermal notes:

## Target

- repo/revision:
- filename:
- SHA256:
- quant:
- params:
- target offload:
- context/KV:

## Proposer

- type:
- draft model repo/revision:
- draft SHA256:
- draft quant:
- draft offload/device:
- draft length / n-gram config:
- extra resident memory:

## Workload

- prompt/category:
- output limit:
- sampling:
- concurrency:
- prompt cache:
- continuous batching:

## Results

| run | wall latency | server predicted t/s | wall t/s | decode calls | draft tokens | accepted tokens | acceptance | accepted/round |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | | | | | 0 | 0 | n/a | n/a |
| speculative | | | | | | | | |

## Speedup

- decode speedup:
- wall latency speedup:

## Memory

- baseline resident memory:
- speculative resident memory:
- target placement changed?:

## Interpretation

### Acceptance

### Proposer overhead

### Target verification

### Workload dependence

### Concurrency dependence

### Memory/offload

## Correctness note

Describe sampling/greedy settings and why exact text equality is or is not expected.

## Conclusion

## Reproducibility

Attach:
- server baseline log
- server speculative log
- baseline JSON
- speculative JSON
- exact target/draft hashes

## Sources

# Result — Experiment 20

## Environment

- Date:
- GPU:
- Driver:
- PyTorch:
- CUDA/HIP:
- OS:
- dtype:
- batch:
- heads:
- head dim:
- causal:
- reps:

Raw JSON:
- path / attachment:

## Results

| seq | backend | status | mean ms | peak delta MiB | max abs error vs math |
|---:|---|---|---:|---:|---:|
| | math | | | | |
| | flash | | | | |
| | auto | | | | |

## Questions

1. Which backend was actually available?
2. Did auto choose a fused path indirectly? What Evidence supports that?
3. At what N did latency separation become obvious?
4. At what N did memory behavior separate?
5. Was error vs math within expected floating-point tolerance?
6. Did any backend OOM or reject the shape/dtype?

## Interpretation boundary

Do not conclude:
- full LLM tokens/s from this operator microbenchmark;
- universal FlashAttention support from one GPU;
- exact runtime peak VRAM from peak-delta alone;
- decode speedup from square prefill-like attention shapes.

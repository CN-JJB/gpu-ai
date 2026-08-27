# Learning / Build Record — 2026-08-27 Attention IO Slice

## Slice

12 — Attention IO → online softmax → FlashAttention-style kernels.

## Why now

This slice connects:
- Slice 02 GPU scheduling;
- Slice 03 registers/shared memory/tiling;
- Slice 04 Roofline;
- LLM prefill/context behavior.

## Stable model

```
naive QK^T materialization
→ N×N HBM intermediate
→ softmax read/write
→ PV

vs

Q/K/V tiles
→ on-chip score tile
→ online softmax state
→ output accumulator
→ no full N×N HBM materialization
```

## Key distinction

```
quadratic compute
!=
quadratic materialized intermediate memory
```

FlashAttention-style exact dense attention reduces IO/materialization but does not remove N² dense attention compute.

## L0 verified

Experiment 19 validates:
- online blockwise exact attention;
- max error ~5.55e-17 in default deterministic case;
- quadratic materialization growth.

At fp16-like × two matrices × 32 heads:
- 4K → 2 GiB conceptual intermediates;
- 8K → 8 GiB;
- 16K → 32 GiB.

Not runtime peak-memory claims.

## Real path

Experiment 20 probes current PyTorch:
- math;
- FlashAttention backend when available;
- auto.

It records latency, peak allocation delta and numerical difference.

## Transfer targets

Learner should now explain:
- why recomputation can beat HBM traffic;
- how online softmax allows tiling;
- why FlashAttention is exact;
- why FA2 still needs better GPU scheduling;
- why prefill/decode differ;
- why GQA/MQA are complementary rather than identical.

## Next direction

Natural next GPU architecture slice:

```
matrix units / Tensor Cores / WMMA-MMA
→ FP16/BF16/TF32/FP8/INT8/INT4
→ accumulation precision
→ quantized GEMM
→ why theoretical TOPS often mislead local LLM buyers
```

This returns from attention kernels to hardware architecture and numerical formats.

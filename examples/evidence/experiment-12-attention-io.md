# Evidence — Experiment 12: IO-aware Attention / FlashAttention

状态：L0 correctness + materialization model verified；real GPU backend probe ready, no fabricated GPU performance.

## Claim

> Exact dense attention can be reorganized so that the full N×N score/probability matrix does not need to be materialized in HBM. Online softmax enables tiled exact processing; the benefit comes from reducing IO/materialization, while dense attention compute remains quadratic.

## L0 correctness evidence

Experiment:
- `labs/experiments/19-attention-online-softmax-io-model/`

Default deterministic toy case:
- N = 11
- d = 7
- dv = 5
- K/V block = 3

Verified max absolute difference between:
- naive full attention;
- tiled online-softmax attention;

was approximately:

```
5.55e-17
```

in the validation environment.

This supports:
```
tiling + online softmax
can preserve exact attention semantics
within floating-point rounding
```

## L0 materialization evidence

fp16-like, two conceptual N×N intermediates, 32 heads:

| N | two matrices/head | 32 heads |
|---:|---:|---:|
| 1024 | 4 MiB | 0.125 GiB |
| 2048 | 16 MiB | 0.5 GiB |
| 4096 | 64 MiB | 2 GiB |
| 8192 | 256 MiB | 8 GiB |
| 16384 | 1 GiB | 32 GiB |

This table is a conceptual naive materialization model, not runtime peak VRAM.

## Primary-source validation

FlashAttention paper:
- exact attention;
- IO-aware;
- tiling between HBM and SRAM;
- fewer HBM accesses.

FlashAttention-2:
- better block/warp work partition;
- fewer non-matmul FLOPs;
- higher parallelism.

NVIDIA Transformer Engine docs:
- describe tiling based on shared memory/register capacity;
- explain reduced global-memory intermediates and recomputation tradeoffs.

## Real Evidence path

`labs/experiments/20-real-sdpa-backend-probe/`

Must record:
- GPU;
- PyTorch/CUDA/HIP;
- dtype/shape;
- backend status;
- latency;
- peak allocated delta;
- error vs math;
- raw JSON.

Unsupported FlashAttention is a valid result.

## Stable conclusions

- FlashAttention is not approximate by definition.
- It does not make exact dense attention O(N).
- Reduced IO can outweigh extra arithmetic/recomputation.
- GPU scheduling still matters after IO optimization.
- prefill and decode require separate performance reasoning.
- GQA/MQA and FlashAttention reduce different traffic.

## Dynamic conclusions intentionally excluded

No claim here about:
- which consumer GPU supports current fused SDPA;
- exact PyTorch backend dispatch;
- exact current speedup;
- exact llama.cpp `-fa` behavior.

Those belong in intelligence.

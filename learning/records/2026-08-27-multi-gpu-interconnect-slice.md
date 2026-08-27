# Learning / Build Record — 2026-08-27 Multi-GPU Interconnect Slice

## Slice

11 — Single-node multi-GPU / interconnect.

## Problem

Correct the common intuition:

> 2×12 GiB = one 24 GiB GPU, and two GPUs should be about twice as fast.

## Stable model established

Separate three goals:
1. fit a larger single model;
2. reduce one-request latency;
3. increase independent-request throughput.

Separate three broad strategies:
- replicas/data parallel;
- layer/pipeline split;
- tensor/row-style within-layer parallelism.

New performance model:

```
compute roof
+ memory roof
+ interconnect roof
```

and:

```
T_N ≈ T_compute/N + T_comm + T_sync + T_imbalance
```

## Artifacts

Research/reference:
- `research/gpu/0005-multi-gpu-interconnect-scaling.md`
- `reference/gpu/multi-gpu-split-interconnect.md`

Lesson:
- `lessons/11-multi-gpu/01-capacity-split-interconnect.html`

L0:
- `labs/experiments/17-multi-gpu-interconnect-roof-model/`

Real:
- `labs/experiments/18-real-multi-gpu-scaling/`

Evidence:
- `examples/evidence/experiment-11-multi-gpu-interconnect.md`

Dynamic intelligence:
- `intelligence/gpu/multi-gpu-topology-2026-08-27.md`

## Verified L0 result

Default model:
- one GPU = 10 ms/token;
- ideal two-GPU compute = 5 ms;
- 64 MiB/token critical transfer;
- 0.2 ms sync.

At:
- 8 GiB/s → 0.7685× speedup;
- 32 GiB/s → 1.3980×;
- 128 GiB/s → 1.7580×.

This proves the causal lesson only. It does not benchmark any hardware.

## Real experiment discipline

Performance scaling A/B uses a model that fits on one GPU.
Capacity-only test may use an oversized model, but does not report speedup against a non-existent single-GPU run.

Always preserve:
- topology;
- P2P;
- PP;
- TG;
- exact runtime/model identity;
- raw outputs.

## Transfer test

Learner should be able to explain:
- why aggregate VRAM is not contiguous VRAM;
- why layer split can increase capacity without reducing token latency;
- why tensor parallel is more link-sensitive;
- why P2P capability and peer bandwidth are different facts;
- why PP and TG can scale differently;
- when replicas can be better than model parallelism.

## Next course direction

After this slice, a natural next bridge is modern attention/kernel IO optimization:

```
Attention work
→ materialized intermediates
→ SRAM/shared-memory tiling
→ IO-aware kernels
→ FlashAttention family
→ LLM prefill/context performance
```

This connects Slice 03 tiling, Slice 04 Roofline and the later LLM serving stack.

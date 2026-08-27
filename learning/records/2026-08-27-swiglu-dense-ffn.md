# Learning / Build Record — 2026-08-27 SwiGLU / Dense FFN

## Slice

27 — SwiGLU / dense FFN, gate/up/down weights, PP/TG shape and weight-traffic consequences.

## Production output

Research:
- `research/llm/0010-swiglu-dense-ffn.md`

Reference:
- `reference/llm/swiglu-ffn-weight-traffic.md`

Lesson:
- `lessons/27-swiglu-ffn/01-gate-up-down.html`

Labs:
- `labs/experiments/48-dense-swiglu-ffn-model/`
- `labs/experiments/49-real-model-ffn-structure-compare/`

Evidence:
- `examples/evidence/experiment-27-swiglu-dense-ffn.md`

## Verified L0 result

Default dense example:

```
FFN weights/layer = 135,266,304
attention projection weights/layer = 67,108,864
ratio = 2.015625×
```

Storage proxy:
- FP16 = 258 MiB/layer;
- 4.5 bpw = 72.5625 MiB/layer.

## Stable skill

Learner can connect:
```
intermediate_size
→ FFN matrix shapes
→ parameter/storage share
→ prefill GEMM regime
→ decode weight-streaming regime
```

## Next

MoE:
- router;
- experts;
- top-k;
- total vs active parameters;
- per-token expert traffic;
- expert batching;
- routing imbalance;
- multi-GPU expert placement.

# Learning / Build Record — 2026-08-27 RMSNorm / RoPE

## Slice

25 — RMSNorm, pre-norm residual path and RoPE.

## Production output

Research:
- `research/llm/0008-rmsnorm-residual-rope.md`

Reference:
- `reference/llm/rmsnorm-residual-rope.md`

Lesson:
- `lessons/25-rmsnorm-rope/01-rmsnorm-residual-rope.html`

Labs:
- `labs/experiments/44-rmsnorm-scale-model/`
- `labs/experiments/45-rope-relative-position-model/`

Evidence:
- `examples/evidence/experiment-25-rmsnorm-residual-rope.md`

## Verified L0 results

RMSNorm:
- output mean not zero;
- positive scale invariance holds to epsilon-level difference.

RoPE:
- rotation norm preserved;
- common position shift preserves base RoPE dot product to floating-point error;
- changing relative offset changes the dot product.

## Stable transfer

The learner can now explain:

```
RMSNorm
→ scale

Residual
→ information/update path

RoPE
→ positional Q/K geometry
```

and why cache identity includes position/RoPE state.

## Next

MHA / MQA / GQA:
- Q heads vs KV heads;
- projection parameter differences;
- KV capacity;
- decode bandwidth;
- quality/speed tradeoff.

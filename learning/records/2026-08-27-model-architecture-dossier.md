# Learning / Build Record — 2026-08-27 Model Architecture Dossier

## Slice

29 — Integrate model architecture into a hardware-facing dossier.

## Production output

Research:
- `research/llm/0012-model-architecture-dossier.md`

Reference:
- `reference/llm/model-architecture-dossier-card.md`

Lesson:
- `lessons/29-model-dossier/01-config-to-hardware-hypothesis.html`

Labs:
- `labs/experiments/52-model-architecture-dossier-model/`
- `labs/experiments/53-real-model-architecture-dossier/`

Evidence:
- `examples/evidence/experiment-29-model-architecture-dossier.md`

## Key discipline

```
known facts
!= derived proxy
!= runtime measurement
```

Capacity formulas can prove some definite failures, but cannot prove successful runtime fit.

## Synthetic checks

Dense:
```
9.191 GiB lower-bound proxy on 12 GiB
→ POSSIBLE-NOT-PROVEN
```

MoE:
```
47B × 4.5 bpw
≈ 24.622 GiB weight proxy alone
→ 24 GiB cannot fully contain weight+KV+reserve
→ FAIL-WITHOUT-OFFLOAD
```

## Repository navigation

COURSE-MAP / lesson index / experiment index refreshed through Slice 29 / Experiment 53.

## Next

Modern attention/context structures that break the simple homogeneous full-attention KV model.

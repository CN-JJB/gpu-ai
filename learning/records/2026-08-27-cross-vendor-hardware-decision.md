# Learning / Build Record — 2026-08-27 Cross-Vendor Hardware Decision Slice

## Slice

18 — Cross-vendor used-hardware decision framework.

## Production output

Research:
- `research/hardware/0001-cross-vendor-used-hardware-decision-framework.md`

Reference:
- `reference/hardware/cross-vendor-decision-card.md`

Lesson:
- `lessons/18-hardware-decision/01-fit-support-roofs-tco.html`

Labs:
- `labs/experiments/31-scenario-hardware-decision-model/`
- `labs/experiments/32-real-used-hardware-candidate-dossier/`

Evidence:
- `examples/evidence/experiment-18-cross-vendor-decision.md`

## Stable decision model

```
workload
→ fit gate
→ support gate
→ identify expected roof
→ run comparable Evidence
→ TCO
→ risk
→ action
```

## Why no universal 100-point score

The same hardware can be rationally ranked differently for:
- 7B interactive use;
- 32B long context;
- multi-user service;
- architecture-learning lab.

Therefore:
- hard gates are universal;
- weights are scenario-specific.

## L0 result

Experiment 31 confirms:
- hard-gate failures do not enter ranking;
- changing workload/weights can change the rational ranking.

Experiment 32 confirms:
- missing critical fields produce NEEDS EVIDENCE;
- the tool refuses to auto-buy.

## Transfer goal

The learner can now take any candidate from NVIDIA, AMD, Apple or Intel and ask the same questions without erasing architecture differences.

## Next slice

China secondhand-market intelligence and transaction risk:

```
listing sample
→ normalize exact SKU/condition
→ asking-price distribution
→ sold-price confidence
→ seller/board risk
→ test-before-pay checklist
→ price threshold
→ candidate dossier
```

Stable market methodology must be separated from dated price snapshots.

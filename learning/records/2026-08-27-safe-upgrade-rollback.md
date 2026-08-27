# Learning / Build Record — 2026-08-27 Safe Upgrade / Rollback

## Slice

40 — Release identity, predeclared gates, candidate acceptance and verified rollback.

## Production output

Research:
- `research/llm/0022-safe-upgrade-rollback.md`

Reference:
- `reference/llm/safe-upgrade-rollback.md`

Lesson:
- `lessons/40-safe-upgrade/01-release-gates-rollback.html`

Labs:
- `labs/experiments/74-release-gate-model/`
- `labs/experiments/75-real-release-gate-rollback/`

Evidence:
- `examples/evidence/experiment-40-safe-upgrade-rollback.md`

## Verified L0

Good candidate:
```
TG 1.08×
PPL ratio 1.01
TTFT 450 ms
SLO 99.3%
→ ACCEPT
```

Fast-but-bad:
```
TG 1.20×
PPL 1.04
TTFT 900 ms
SLO 92%
→ ROLLBACK
```

Rollback restores baseline identity and readiness/smoke.

## Real gate hardening

Incomplete numeric evidence is blocked rather than divided by zero or interpreted as measurement.

## Stable skill

Learner can now treat release engineering as:

```
known-good baseline
→ predeclared policy
→ candidate gates
→ accept or exact rollback
→ rollback verification
```

## Next

Observability / incident diagnosis:
- symptoms vs causes;
- logs vs metrics vs traces;
- saturation/queue/VRAM/thermal signals;
- timeline correlation;
- incident evidence packet;
- avoid alerting on one noisy metric.

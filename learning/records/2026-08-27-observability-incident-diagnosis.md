# Learning / Build Record — 2026-08-27 Observability / Incident Diagnosis

## Slice

41 — Latency/traffic/errors/saturation, correlated timelines and evidence-based incident hypotheses.

## Production output

Research:
- `research/llm/0023-observability-incident-diagnosis.md`

Reference:
- `reference/llm/observability-incident-diagnosis.md`

Lesson:
- `lessons/41-observability/01-symptom-timeline-hypothesis.html`

Labs:
- `labs/experiments/76-incident-diagnosis-cases/`
- `labs/experiments/77-real-incident-evidence/`

Evidence:
- `examples/evidence/experiment-41-observability-incident-diagnosis.md`

## Verified L0

Queue:
```
TTFT 6.0×
deferred +9
ITL 1.06×
→ queue-compatible
```

Thermal:
```
temp +18C
clock 0.667×
ITL 1.9×
→ thermal/clock hypothesis
```

Stable VRAM:
```
96.25% peak
0.1 GiB range
latency stable
→ high occupancy alone is not leak evidence
```

## Real collector

Read-only:
- localhost only;
- <=300 s;
- no power/clock/driver changes;
- raw metrics/vendor telemetry retained.

## Stable skill

Learner can now write:
```
evidence supports hypothesis X
```
instead of converting one metric directly into a root-cause story.

## Next

Power/energy efficiency:
- watts vs joules/token;
- idle vs active power;
- throughput/watt;
- energy/request;
- thermal/power limit interaction;
- electricity-cost/TCO link.

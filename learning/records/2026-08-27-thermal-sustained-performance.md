# Learning / Build Record — 2026-08-27 Thermal / Cooling / Sustained Performance

## Slice

45 — Thermal soak, sensor/limiter distinctions, sustained TG drift and read-only cooling evidence.

## Production output

Research:
- `research/gpu/0006-thermal-cooling-sustained-performance.md`

Dynamic intelligence:
- `intelligence/gpu/thermal-telemetry-2026-08-27.md`

Reference:
- `reference/gpu/thermal-sustained-performance.md`

Lesson:
- `lessons/45-thermal-sustained/01-temperature-clocks-drift.html`

Labs:
- `labs/experiments/84-thermal-sustained-model/`
- `labs/experiments/85-real-sustained-thermal/`

Evidence:
- `examples/evidence/experiment-45-thermal-sustained-performance.md`

## Verified L0

```
thermal case:
+31C
clock 0.763×
TG 0.764×
→ compatible thermal/clock drift

hot stable:
TG -0.4%
→ stable

clock drift with +6C:
→ investigate non-thermal/power limiter
```

## Real wrapper

Fake-bench integration verified:
- samples arrays captured;
- controlled fields protected;
- hidden environment overrides stripped.

## Stable skill

Learner can separate:

```
temperature
clock change
performance drift
thermal limiter evidence
```

instead of treating them as synonyms.

## Next

Used-GPU hardware validation:
- identity/spoofing;
- VRAM errors;
- sustained load;
- PCIe link width/gen;
- display/output vs compute stability;
- seller claims vs evidence;
- safe purchase acceptance checklist.

# Experiment 76 — Synthetic Incident Diagnosis Cases

硬件等级：L0

## Goal

Practice distinguishing symptom patterns without claiming causation.

## Case 1 — Queue pressure

```bash
python3 diagnose.py case-queue.csv
```

Expected hypothesis:

```
QUEUE_PRESSURE_COMPATIBLE
```

because:
- TTFT rises 6×;
- deferred requests rise;
- ITL remains near-flat;
- clocks stay near-flat.

## Case 2 — Thermal/clock

```bash
python3 diagnose.py case-thermal.csv
```

Expected:

```
THERMAL_CLOCK_HYPOTHESIS
```

because:
- temperature rises;
- SM clock falls;
- ITL worsens.

It is still a hypothesis.

## Case 3 — High stable VRAM

```bash
python3 diagnose.py case-vram-stable.csv
```

Expected:

```
HIGH_STABLE_VRAM
```

because VRAM is >95% but stable while latency is stable.

This is evidence **against calling high occupancy alone a leak**.

## Scope

All telemetry is synthetic.

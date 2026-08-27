# Experiment 84 — Sustained Thermal / Clock Drift Cases

硬件等级：L0

## Goal

Practice reading:

```
temperature
clock
power
TG
```

as one timeline.

## Thermal-drift case

```bash
python3 analyze.py case-thermal-drift.csv
```

Expected:
```
temp +31 C
clock last/first ≈ 0.763x
TG last/first ≈ 0.764x
THERMAL_CLOCK_PERF_DRIFT_COMPATIBLE
```

This is still not exact throttle-cause proof.

## Hot-stable case

```bash
python3 analyze.py case-hot-stable.csv
```

Expected:
```
TG drift ≈ -0.4%
clock nearly stable
SUSTAINED_STABLE
```

The numeric temperature is synthetic and must not become a universal GPU threshold.

## Clock/perf drift without large thermal rise

```bash
python3 analyze.py case-clock-other-limit.csv
```

Expected:
```
CLOCK_PERF_DRIFT_WITHOUT_LARGE_THERMAL_RISE
```

Possible next evidence:
- power-cap/event reason;
- driver policy;
- workload/background state.

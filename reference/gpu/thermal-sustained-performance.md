# Thermal / Sustained Performance Card

## Timeline

```
time
→ power
→ temperature
→ clock
→ TG/ITL
```

## Drift

```
TG drift %
=
(last-window / first-window - 1) × 100
```

Record:
- first-window TG;
- last-window TG;
- min/max;
- temperature delta;
- clock delta.

## Stronger thermal hypothesis

```
temperature ↑
+
clock ↓
+
performance ↓
+
thermal limiter/event evidence
```

is stronger than temperature alone.

## Do not equate

```
high temperature
=
throttling
```

or:

```
clock drop
=
thermal cause
```

## Test identity

- ambient:
- case/open bench:
- fan policy:
- model/runtime:
- TG token count:
- repetitions:
- warmup:
- GPU device:
- power/clocks untouched?:

## Default safety

Measure only:
- no OC/UV;
- no power-limit change;
- no fan-curve change.

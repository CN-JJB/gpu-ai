# Experiment 78 — Power / Energy Efficiency Model

硬件等级：L0

## Goal

Compute:
- job duration;
- joules;
- J/output-token;
- tokens/J;
- incremental J/token above idle;
- kWh per 1M output tokens.

## Run

```bash
python3 energy.py scenarios.csv
```

Default hypothetical electricity price:

```
0.20 currency / kWh
```

## Key result

```
fast-high-power:
5.0 J/token

balanced:
4.4 J/token

low-power:
~4.286 J/token
```

The fastest synthetic GPU is not the most energy-efficient.

## Boundary

These are constant board-power toy values.

They are not real GPU measurements or whole-system electricity costs.

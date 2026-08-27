# Experiment 44 — RMSNorm Scale / Mean Model

硬件等级：L0

## Goal

Verify two facts:

1. RMSNorm is approximately invariant to positive global re-scaling.
2. RMSNorm does not force output mean to zero.

Default vector:

```
x = [1, -2, 3, -4]
```

Compare:

```
x
3x
```

using unit gain and epsilon = 1e-6.

## Run

```bash
python3 simulate.py
```

The script also computes a simple LayerNorm-style normalized vector for contrast.

## Expected concept

RMSNorm outputs for x and 3x should be nearly identical.

But RMSNorm output mean should not be forced to zero.

LayerNorm-style output mean should be near zero.

# Experiment 45 — RoPE Relative-Position Geometry

硬件等级：L0

## Goal

Verify:

1. rotation preserves vector norm;
2. base RoPE dot product depends on relative position;
3. shifting both positions by the same offset preserves the idealized RoPE dot product.

Toy dimension:
```
d = 4
```

Pairs use standard-style inverse frequencies:

```
omega_i = base^(-2i/d)
```

Default:
```
base = 10000
q = [1, 0, 1, 0]
k = [0.6, 0.8, 0.3, -0.4]
q position = 3
k position = 7
shared shift = 11
```

## Run

```bash
python3 simulate.py
```

## Expected concept

```
dot(R(3)q, R(7)k)
≈
dot(R(14)q, R(18)k)
```

because both pairs have relative offset 4.

Changing only one position should change the dot product.

## Scope

This demonstrates base RoPE geometry only.

It is not a claim that:
- whole model output is shift invariant;
- every model uses the same base/scaling;
- every runtime stores K internally in the same representation.

# Experiment 50 — MoE Total / Active / Weight-Reuse Model

硬件等级：L0

## Goal

Separate four quantities:

```
total expert params
active expert params/token
resident expert bytes
idealized batch expert-weight bytes/token
```

Default:

```
d = 4096
expert d_ff = 14336
experts = 8
top-k = 2
MoE layers = 32
effective weight bits = 4.5
batch tokens = 16
```

## Run

```bash
python3 model.py
```

The script evaluates two synthetic routing patterns:

### Balanced

32 assignments spread evenly:

```
[4,4,4,4,4,4,4,4]
```

### Skewed

All tokens choose experts 0 and 1:

```
[16,16,0,0,0,0,0,0]
```

## What it demonstrates

Balanced routing:
- better expert/device utilization;
- more unique expert weights touched.

Skewed routing:
- stronger weight reuse;
- terrible expert-parallel load balance.

So:
```
minimum weight bytes
!=
minimum latency
```

## Scope

The batch weight-read calculation is an **ideal lower-bound proxy**:
one expert weight set counted once if at least one token uses it.

Real runtimes tile weights, have finite cache, dequantize, schedule kernels and may move activations/weights differently.

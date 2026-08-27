# Evidence — Experiment 42: Power / Energy Efficiency

状态：stable power/energy lesson complete; L0 J/token arithmetic verified; NVIDIA board-power integration path ready.

## Claim

> Instantaneous power in watts is not total energy. Local-LLM energy efficiency must combine power and runtime, with a clearly declared measurement boundary such as GPU-board or whole-system wall energy.

## Core math

```
1 W = 1 J/s

E = ∫ P(t) dt

J/token = energy / useful tokens

tokens/J = 1 / (J/token)
```

For steady constant power/rate:

```
tok/s/W = tok/J
```

## Experiment 78 verification

Synthetic 1000 output-token jobs:

### fast-high-power

```
300 W
60 tok/s

duration = 16.666667 s
energy = 5000 J
J/token = 5.0
tokens/J = 0.2
incremental above 70W idle = 3.833333 J/token
```

### balanced

```
220 W
50 tok/s

duration = 20 s
energy = 4400 J
J/token = 4.4
tokens/J ≈ 0.227273
incremental = 3.0 J/token
```

### low-power

```
180 W
42 tok/s

duration ≈ 23.809524 s
energy ≈ 4285.714286 J
J/token ≈ 4.285714
tokens/J ≈ 0.233333
incremental ≈ 2.619048 J/token
```

So the fastest synthetic configuration is not the best J/token configuration.

## Electricity arithmetic

```
1 kWh = 3.6e6 J
```

Verified synthetic:
- 5.0 J/token → 1.388889 kWh / 1M tokens;
- 4.4 J/token → 1.222222 kWh / 1M;
- 4.285714 J/token → 1.190476 kWh / 1M.

The bundled default price is explicitly hypothetical and user-overridable.

## Integration check

A synthetic 3-point board-power trace:

```
t=0: 100 W
t=1: 120 W
t=2: 140 W
```

Trapezoidal integration verifies:

```
energy = 240 J
average power = 120 W
```

With aggregate idle baseline:

```
50 W
```

incremental energy verifies:

```
140 J
```

## Current NVIDIA evidence

Current NVIDIA documentation describes read-only monitoring/reporting of:
- utilization;
- current clocks/performance state;
- temperature;
- board power draw on products that expose it.

References:
- https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
- https://docs.nvidia.com/vgpu/latest/grid-vgpu-user-guide/performance-monitoring-gpu.html

## Experiment 79

The real path integrates Experiment 77 NVIDIA raw samples using actual `elapsed_s`.

It:
- sums selected participating GPU indices;
- supports multi-GPU board power;
- rejects missing samples;
- rejects changing selected-GPU count;
- rejects non-increasing time;
- uses trapezoidal integration;
- optionally computes incremental-above-idle energy;
- optionally computes board-energy electricity arithmetic.

No real energy value ships with the course.

## Measurement boundaries

The course explicitly distinguishes:

```
GPU board energy
!=
whole-system wall energy
```

Whole-system electricity additionally includes:
- CPU/RAM/platform;
- storage;
- cooling/fans;
- PSU loss;
- unrelated devices.

For TCO/electricity, wall/system measurement is stronger.

## PP/TG boundary

```
J/output-token
```

for decode cannot be silently reused as:

```
J/prompt-token
```

for prefill.

Workload identity remains mandatory.

## Learner should reject

- lower watts means lower job energy;
- faster means better J/token;
- GPU board telemetry equals wall power;
- one watt sample is job energy;
- TG energy represents PP;
- idle subtraction is mandatory rather than a chosen boundary;
- TDP alone predicts inference electricity cost.

# Research Note 0024 — Power / Energy Efficiency for Local LLMs

日期：2026-08-27

## Research question

If one GPU is faster and another uses fewer watts, which is actually more efficient?

You must separate:

```
power
from
energy
```

and:

```
speed
from
energy per useful work
```

---

# Part I — Watts

Power:

```
1 watt
=
1 joule / second
```

A 300 W reading is an instantaneous/rate quantity.

It does not say how long the workload runs.

---

# Part II — Joules

Energy over a time interval:

```
E
=
∫ P(t) dt
```

If power is approximately constant:

```
E
≈
P × time
```

So:
- 300 W for 10 s = 3000 J;
- 200 W for 20 s = 4000 J.

The lower-watt workload can consume more total energy if it runs much longer.

---

# Part III — Joules per token

For output generation:

```
J/output-token
=
energy during generation
/
generated output tokens
```

Lower is more energy-efficient for that measured boundary.

For prompt processing:

```
J/prompt-token
```

is a separate metric.

Do not mix PP and TG token energy without declaring the workload composition.

---

# Part IV — Tokens per joule

```
tokens/J
=
tokens / energy
```

This is the reciprocal of:

```
J/token
```

For a steady workload:

```
tok/s/W
=
tokens/J
```

because:

```
(tok/s) / (J/s)
=
tok/J
```

---

# Part V — Synthetic constant-power examples

All output:

```
1000 tokens
```

## A — fast/high power

```
300 W
60 tok/s
```

Duration:

```
16.667 s
```

Energy:

```
5000 J
```

Efficiency:

```
5.0 J/token
```

## B — slower/lower power

```
220 W
50 tok/s
```

Duration:

```
20 s
```

Energy:

```
4400 J
```

Efficiency:

```
4.4 J/token
```

B is slower but uses less energy per token.

## C — lower-power/lower-speed

```
180 W
42 tok/s
```

Duration:

```
23.810 s
```

Energy:

```
≈4285.7 J
```

Efficiency:

```
≈4.286 J/token
```

In this synthetic set, C is slowest but most energy-efficient.

---

# Part VI — Efficiency is workload-specific

A GPU can be efficient at:
- large PP;
- batched serving;

and less efficient at:
- single-user TG;
- tiny prompts.

Hardware utilization and memory/compute balance change.

Benchmark energy under the workload you actually care about.

---

# Part VII — Idle baseline

A GPU/server already consumes power while idle.

Two useful energy boundaries:

## Total measured energy

```
∫ P_active(t) dt
```

## Incremental above idle

```
∫ max(P_active(t)-P_idle, 0) dt
```

Both are useful, but must be labeled separately.

---

# Part VIII — GPU board vs whole system

GPU telemetry can measure/report board-device power on supported devices.

Whole-system wall power additionally includes:
- CPU;
- RAM;
- motherboard;
- storage;
- fans/pumps;
- PSU conversion loss;
- other GPUs/devices.

Therefore:

```
GPU board J/token
!=
whole-system J/token
```

For electricity cost/TCO, wall-meter/system-level energy is stronger evidence.

---

# Part IX — Current NVIDIA evidence

Current NVIDIA documentation describes management telemetry including:
- GPU utilization;
- current clocks/performance state;
- temperature;
- board power draw/power limits on products reporting those measurements.

Official references:
- https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
- https://docs.nvidia.com/vgpu/latest/grid-vgpu-user-guide/performance-monitoring-gpu.html

The course uses read-only `nvidia-smi` output when available.

Not every GPU/driver exposes every power field identically.

UNKNOWN/unavailable must remain explicit.

---

# Part X — Sampling/integration

If power samples are:

```
(t0,P0)
(t1,P1)
...
```

a simple trapezoidal approximation is:

```
E
≈
Σ
((P_i + P_(i+1))/2)
×
(t_(i+1)-t_i)
```

Record:
- sample interval;
- tool;
- selected devices.

---

# Part XI — Electricity unit

```
1 kWh
=
3,600,000 J
```

So:

```
kWh
=
J / 3.6e6
```

Cost:

```
energy_kWh × local_price_per_kWh
```

Do not hardcode one country's electricity price into the course.

---

# Part XII — Cost per million output tokens

If:

```
4.4 J/token
```

then one million output tokens:

```
4.4e6 J
≈
1.222 kWh
```

At a hypothetical:
```
0.20 currency/kWh
```

energy cost:

```
≈0.244 currency / 1M output tokens
```

This is synthetic board-energy arithmetic, not a real TCO result.

---

# Part XIII — TCO

Energy is only one part:

```
purchase price
+ electricity
+ cooling
+ PSU/platform
+ failures/replacement
+ time/software risk
```

Use actual duty cycle.

---

# Part XIV — Thermal stability

Higher sustained power can raise temperature.

If cooling becomes limiting:

```
temperature ↑
clock ↓
performance ↓
```

Then:
- tok/s falls;
- J/token can worsen.

Measure after reaching representative thermal state for sustained workloads.

---

# Part XV — Power-limit tradeoff

Lowering a power limit can sometimes reduce power more than throughput, improving J/token.

But the result is hardware/workload-specific.

This course does not change power limits in the default real lab.

First measure read-only.

---

# Part XVI — Multi-GPU

For multi-GPU serving:

```
total GPU board power
=
Σ board power of participating GPUs
```

If unrelated GPUs are sampled, summing all overstates workload energy.

Experiment 79 can filter explicit NVIDIA GPU indices.

---

# Part XVII — Request energy

For serving:

```
J/request
=
energy over serving window
/
completed requests
```

But mixed request lengths make average J/request hard to compare.

Also record:
- prompt tokens/request;
- output tokens/request;
- concurrency.

---

# Part XVIII — Queue attribution

Client E2E includes queue waiting.

GPU may not be doing work for that request while it waits.

Therefore:

```
client E2E × instantaneous GPU power
```

is not a valid per-request energy attribution under concurrency.

Prefer aggregate workload-window energy unless a validated attribution method exists.

---

# Claims to avoid

- "lower watts means lower energy";
- "faster means more energy-efficient";
- "GPU board power equals wall power";
- "one sampled watt value is job energy";
- "J/token from TG can be applied to PP";
- "idle power should always be subtracted";
- "all GPUs expose identical power telemetry";
- "electricity cost alone is TCO";
- "client E2E directly attributes GPU energy to one concurrent request".

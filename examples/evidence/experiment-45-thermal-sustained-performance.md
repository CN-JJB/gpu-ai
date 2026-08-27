# Evidence — Experiment 45: Thermal / Cooling / Sustained Performance

状态：stable sustained-performance lesson complete; three L0 thermal/clock cases verified; real repeated-TG wrapper self-checked.

## Claim

> Short cold-run performance is not automatically sustained performance. Thermal diagnosis requires a timeline of workload, temperature, clocks, power and throughput, plus limiter/event evidence where supported.

## Dynamic vendor evidence

NVIDIA current documentation exposes concepts including:
- temperature;
- power readings;
- current/performance clocks;
- performance state;
- clock-event reasons.

Current clock-event reason families distinguish thermal, power-cap, power-brake and other limiting states.

Official:
- https://docs.nvidia.com/deploy/nvidia-smi/index.html
- https://docs.nvidia.com/deploy/nvml-api/group__nvmlClocksEventReasons.html

AMD SMI current documentation exposes monitoring around:
- edge/hotspot/memory temperatures where supported;
- GFX/memory clocks;
- activity;
- power;
- VRAM.

Official:
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/how-to/amdsmi-cli-tool.html
- https://rocm.docs.amd.com/projects/amdsmi/en/latest/doxygen/docBin/html/group__tagGPUMonitor.html

Dated dynamic summary:
- `intelligence/gpu/thermal-telemetry-2026-08-27.md`

## Experiment 84 — thermal drift

Verified synthetic:

```
temperature:
55 → 86 C
delta = +31 C

clock:
1900 → 1450 MHz
last/first = 0.763158×

TG:
55 → 42 tok/s
last/first = 0.763636×
drift = -23.636%
```

Classification:

```
THERMAL_CLOCK_PERF_DRIFT_COMPATIBLE
```

This supports a thermal/clock-management hypothesis but does not prove the exact limiter.

## Hot-stable case

Verified:

```
temperature:
80 → 84 C

clock:
1800 → 1790 MHz

TG:
50 → 49.8 tok/s
drift = -0.4%
```

Classification:

```
SUSTAINED_STABLE
```

Central lesson:

```
higher temperature
!= automatic throttling
```

The synthetic temperatures are not universal GPU limits.

## Clock/performance drift without large thermal rise

Verified:

```
temperature:
64 → 70 C
delta = +6 C

clock:
1850 → 1580 MHz
ratio ≈ 0.854054×

TG:
52 → 44 tok/s
ratio ≈ 0.846154×
```

Classification:

```
CLOCK_PERF_DRIFT_WITHOUT_LARGE_THERMAL_RISE
```

Next evidence should include:
- power cap;
- clock-event/limiter reasons;
- driver/policy;
- workload/background-state checks.

## Current pinned llama-bench

Pinned:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current llama-bench supports:
- `-r/--repetitions`;
- JSON/JSONL output;
- per-repetition `samples_ts`;
- per-repetition `samples_ns`;
- optional `--no-warmup`.

The installed `--help` remains authoritative.

## Experiment 85 wrapper self-check

The real wrapper was executed against a fake local llama-bench implementation.

Verified:
- local model path forced;
- TG prompt size forced to zero;
- n-gen/repetition/output format controlled;
- per-repetition samples preserved;
- hidden `LLAMA_ARG_*` removed;
- `HF_TOKEN` removed;
- safe performance extra args such as `-ngl all` remain possible;
- `--extra-arg=--model` is rejected.

This protects experiment identity without installing/changing a system service.

## Real baseline safety

Experiment 85 changes none of:
- overclock;
- voltage;
- power limit;
- fan curve.

It reuses read-only telemetry.

## Limiter language

Strong thermal-throttle evidence is more like:

```
temperature rise
+
clock decline
+
performance decline
+
thermal limiter/event evidence
```

rather than:

```
temperature > one magic number
```

## Environment

A valid cooler/card comparison records:
- ambient;
- open bench vs closed case;
- fan policy;
- neighboring GPUs/slot spacing;
- warmup policy.

## Learner should reject

- 80 C always means throttling;
- clock drop always means thermal cause;
- short benchmark equals sustained performance;
- hotter GPU is automatically slower;
- power-cap slowdown is thermal slowdown;
- one temperature sensor represents all components;
- open-bench thermals equal closed-case multi-GPU thermals.

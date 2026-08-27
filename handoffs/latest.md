# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–44 are implemented.
Experiments 01–83 exist.

## Slice 44 core

Linux:

```
MemFree
!=
MemAvailable
```

File-backed cache and anonymous memory have different reclaim behavior.

Synthetic verified:

```
cache-heavy:
free 2 GiB
available proxy 16.4 GiB
→ 8 GiB request fits after toy reclaim

anonymous-heavy:
free 2 GiB
available proxy 4.4 GiB
→ 3.6 GiB shortfall
```

The proxy is explicitly NOT the Linux MemAvailable formula.

Real Linux collector:
- /proc/meminfo;
- /proc/vmstat deltas;
- optional /proc/PID status/smaps;
- optional NVIDIA VRAM snapshot;
- no stress allocation;
- no swap/cache/sysctl changes.

Memory domains:

```
host RAM OOM
!= discrete GPU VRAM OOM
```

Apple silicon is handled as unified-memory special architecture.

## Active next slice — Thermal / Cooling / Sustained Performance

Teach:

```
workload duration
→ power
→ temperature
→ clock behavior
→ sustained tok/s
```

Need to distinguish:
- short cold burst;
- warm steady-state benchmark;
- temperature vs vendor hotspot/junction fields;
- clock drop correlated with TG/ITL drift;
- airflow/case/fan/noise constraints.

Real lab:
- read-only vendor telemetry;
- fixed repeated TG workload;
- no overclock;
- no power-limit changes;
- no fan-control changes by default.

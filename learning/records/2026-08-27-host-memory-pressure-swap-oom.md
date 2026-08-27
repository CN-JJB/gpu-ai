# Learning / Build Record — 2026-08-27 Host Memory Pressure / Swap / OOM

## Slice

44 — Free vs available memory, file-cache reclaim, anonymous memory, swap activity and host-vs-GPU OOM domains.

## Production output

Research:
- `research/llm/0026-host-memory-pressure-swap-oom.md`

Reference:
- `reference/llm/host-memory-pressure-swap-oom.md`

Lesson:
- `lessons/44-host-memory/01-available-cache-swap-oom.html`

Labs:
- `labs/experiments/82-host-memory-reclaim-model/`
- `labs/experiments/83-real-memory-pressure-evidence/`

Evidence:
- `examples/evidence/experiment-44-host-memory-pressure-swap-oom.md`

## Verified L0

```
cache-heavy:
free 2 GiB
available proxy 16.4 GiB
8 GiB request fits after toy reclaim

anonymous-heavy:
free 2 GiB
available proxy 4.4 GiB
8 GiB request has 3.6 GiB shortfall
```

## Verified real collector

1-second Linux read-only window:
- 2 samples;
- no stress allocation;
- no system changes;
- vmstat deltas computed successfully.

## Stable skill

Learner can now separate:

```
low free RAM
from
actual host pressure
from
host OOM
from
GPU VRAM OOM
```

and uses MemAvailable/activity deltas rather than one snapshot.

## Next

Thermal / cooling / sustained performance:
- temperature vs hotspot/junction;
- clocks;
- power;
- sustained TG drift;
- case airflow;
- thermal throttling evidence;
- fan/noise tradeoffs.

# Experiment 82 — Host Memory Reclaim Model

硬件等级：L0

## Goal

Understand why:

```
MemFree low
```

does not automatically mean:

```
no usable RAM remains
```

The model separates:
- anonymous memory;
- file cache;
- kernel/other;
- free RAM;
- a synthetic reclaimable-cache fraction.

## Run

```bash
python3 memory_model.py scenarios.csv
```

## Important

The calculated:

```
available_proxy
```

is **not** the Linux `MemAvailable` algorithm.

It is only a teaching proxy.

For real Linux evidence, read:

```
/proc/meminfo: MemAvailable
```

## Key cases

Cache-heavy:
```
free = 2 GiB
proxy available = 16.4 GiB
8 GiB request fits after synthetic reclaim
```

Anonymous-heavy:
```
free = 2 GiB
proxy available = 4.4 GiB
8 GiB request leaves 3.6 GiB shortfall
```

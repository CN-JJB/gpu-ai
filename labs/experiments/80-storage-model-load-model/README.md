# Experiment 80 — Storage / Model-Load Stage Model

硬件等级：L0

## Goal

Separate:
- source read time;
- host/backend overhead;
- device upload;
- steady TG.

## Run

```bash
python3 model_load.py scenarios.csv
```

Synthetic setup:

```
model = 20 GiB
host/backend = 1 s
GPU upload = 20 GiB @ 12 GiB/s
steady TG = 50 tok/s
```

Only source bandwidth changes.

## Lesson

Startup can change by tens of seconds while steady TG remains fixed in the model.

This demonstrates:

```
storage startup bottleneck
!=
steady decode bottleneck
```

## Boundary

The script assumes serial full-read + upload stages.

Real mmap, page faults, read-ahead and device loading may overlap or defer work.

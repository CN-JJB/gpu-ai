# Experiment 79 — Real NVIDIA Board-Energy Integration

硬件等级：L2，NVIDIA 主线。

## Goal

Integrate read-only NVIDIA board-power samples over a known workload window.

Reuse Experiment 77:

```
incident-evidence/
  timeline.csv
  vendor-raw/0000-nvidia.csv
  vendor-raw/0001-nvidia.csv
  ...
```

## Capture

Run Experiment 77 telemetry while you run:
- llama-bench TG;
- or Experiment 63 fixed serving workload.

Record exact output token count for the same time boundary.

## Integrate

```bash
python3 integrate_nvidia_energy.py \
  incident-evidence/timeline.csv \
  incident-evidence/vendor-raw \
  --output-tokens 1024
```

Specific participating GPU(s):

```bash
--gpu-index 0
--gpu-index 1
```

## Optional idle baseline

```bash
--idle-watts 70
```

Reports incremental energy above that aggregate selected-GPU idle baseline.

## Optional electricity arithmetic

```bash
--price-per-kwh YOUR_PRICE
```

This cost uses GPU board energy only.

For household/TCO electricity, a wall meter or validated whole-system measurement is stronger.

## Integration

Uses trapezoidal integration over actual `elapsed_s`.

It fails if:
- a NVIDIA sample file is missing;
- no power row can be parsed;
- selected GPU count changes;
- timestamps are non-increasing.

It does not silently interpolate gaps.

## Multi-GPU caution

If unrelated GPUs are doing other work, select only participating indices.

## Thermal state

Record:
- starting/ending temperature;
- clocks;
- performance drift.

A short cold run may not represent sustained efficiency.

## Complete

Fill:
`RESULT-TEMPLATE.md`.

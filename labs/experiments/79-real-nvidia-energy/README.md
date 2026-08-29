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


## Why this experiment

理论 J/token 只有在真实功率时间序列与同一 workload token 边界绑定后，才能升级成实际设备证据。这个实验把 NVIDIA board-power telemetry 做时间积分，而不是拿一个瞬时 Watts 截图做能效结论。

## Hypothesis

在一个边界明确的固定 workload 窗口内，梯形积分得到的 board energy 除以 exact output tokens，可以形成可复查的 GPU-board J/token；加入 idle baseline 后还能估算增量能量。

## Fixed variables

模型、runtime、workload、参与 GPU、采样方式和 token 计数边界固定。做 A/B 时一次只改一个声明变量。

## What to observe

1. elapsed_s 是否严格递增。
2. 选定 GPU 数是否稳定。
3. power samples 是否覆盖整个 workload window。
4. total J、J/token、optional incremental J/token。
5. 起止 temperature/clock 是否说明 run 尚未进入稳态。

## Troubleshooting

- board power 不是 wall power。
- 缺 sample 时工具故意失败，不应静默插值。
- unrelated GPU 必须排除。
- output tokens 必须和同一时间窗对应。
- short cold run 不能代表 sustained efficiency。

## Evidence to save

保存 timeline.csv、vendor raw samples、benchmark/token evidence、integration output 和 RESULT-TEMPLATE。

## What this proves

你能产生一个真实 NVIDIA board-energy / token 证据。

## What this does NOT prove

它不等于整机耗电或家庭电费，也不代表其他 workload。

## No-hardware fallback

没有 NVIDIA 真机时完成 Experiment 78；本实验留到 Learner Verified。

## Transfer question

为什么同一次运行里只记录“平均 280W”还不够，需要同时保存时间边界和 output token count？

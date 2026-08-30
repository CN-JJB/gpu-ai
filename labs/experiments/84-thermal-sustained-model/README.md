# Experiment 84 — Sustained Thermal / Clock Drift Cases

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/thermal-sustained.svg" alt="短时 boost 与持续稳态是两种工作区间；热饱和后频率、功耗和吞吐可能进入新的平衡点。">
  <figcaption>短时 boost 与持续稳态是两种工作区间；热饱和后频率、功耗和吞吐可能进入新的平衡点。</figcaption>
</figure>

## Goal

Practice reading:

```
temperature
clock
power
TG
```

as one timeline.

## Thermal-drift case

```bash
python3 analyze.py case-thermal-drift.csv
```

Expected:
```
temp +31 C
clock last/first ≈ 0.763x
TG last/first ≈ 0.764x
THERMAL_CLOCK_PERF_DRIFT_COMPATIBLE
```

This is still not exact throttle-cause proof.

## Hot-stable case

```bash
python3 analyze.py case-hot-stable.csv
```

Expected:
```
TG drift ≈ -0.4%
clock nearly stable
SUSTAINED_STABLE
```

The numeric temperature is synthetic and must not become a universal GPU threshold.

## Clock/perf drift without large thermal rise

```bash
python3 analyze.py case-clock-other-limit.csv
```

Expected:
```
CLOCK_PERF_DRIFT_WITHOUT_LARGE_THERMAL_RISE
```

Possible next evidence:
- power-cap/event reason;
- driver policy;
- workload/background state.


## Why this experiment

一次短跑的高 TG 不能代表 20 分钟后的稳态。这个实验训练你把 temperature、clock、power、TG 放在同一时间线上看，而不是单独盯温度数字。

## Hypothesis

thermal-drift case 应表现为温度上升、clock 下滑、TG 同方向下降；hot-stable case 说明“温度高”本身不足以证明 throttling；other-limit case 则提示还要继续找 power/event 等证据。

## Fixed variables

每个 CSV trace 不修改。只比较不同 symptom pattern，不把一个 case 的阈值套到另一个 case。

## What to observe

1. first→last 的 temp/clock/TG 变化。
2. clock ratio 与 TG ratio 是否同步。
3. high temperature 但 stable TG 的反例。
4. clock/TG drift 无明显温升时，下一步证据是什么。

## Troubleshooting

- 不要背一个通用 80°C 阈值。
- 不要把 correlation 直接写成 exact throttle cause。
- 真实机器还应查 thermal/power limiter、hotspot/memory temp、ambient、fan。

## Evidence to save

保存三次输出，并给每个 case 写：Observed pattern / Compatible hypothesis / Missing evidence。

## What this proves

你能区分热相关性能漂移、热但稳定、以及其他限制的基本模式。

## What this does NOT prove

synthetic trace 不证明任何具体 GPU 的真实温度阈值或故障。

## No-hardware path

完整 L0。

## Transfer question

如果温度升高 20°C，但 clock 和 TG 都几乎不变，你能直接说发生 thermal throttling 吗？为什么？

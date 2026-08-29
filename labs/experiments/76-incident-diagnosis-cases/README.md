# Experiment 76 — Synthetic Incident Diagnosis Cases

硬件等级：L0

## Goal

Practice distinguishing symptom patterns without claiming causation.

## Case 1 — Queue pressure

```bash
python3 diagnose.py case-queue.csv
```

Expected hypothesis:

```
QUEUE_PRESSURE_COMPATIBLE
```

because:
- TTFT rises 6×;
- deferred requests rise;
- ITL remains near-flat;
- clocks stay near-flat.

## Case 2 — Thermal/clock

```bash
python3 diagnose.py case-thermal.csv
```

Expected:

```
THERMAL_CLOCK_HYPOTHESIS
```

because:
- temperature rises;
- SM clock falls;
- ITL worsens.

It is still a hypothesis.

## Case 3 — High stable VRAM

```bash
python3 diagnose.py case-vram-stable.csv
```

Expected:

```
HIGH_STABLE_VRAM
```

because VRAM is >95% but stable while latency is stable.

This is evidence **against calling high occupancy alone a leak**.

## Scope

All telemetry is synthetic.


## Why this experiment

看到一个异常指标就直接下结论，是运维最常见的推理错误。本实验训练你把“症状模式”写成 hypothesis-compatible，而不是把相关性冒充因果。

## Hypothesis

不同 synthetic case 应支持不同的优先假设：queue pressure、thermal/clock、high-but-stable VRAM。特别是“VRAM >95%”本身不应自动被叫做 memory leak。

## Fixed variables

每个 case 的 trace 不修改；你只根据时间序列中的多信号关系分类。

## What to observe

1. TTFT、ITL、queue/deferred、clock、temperature、VRAM 的时间关系。
2. 哪些信号一起变化，哪些保持稳定。
3. 每个 hypothesis 还缺什么 discriminating evidence 才能升级为根因。

## Troubleshooting

- 先对齐时间戳，不要跨时间比较无关样本。
- high utilization / high VRAM 都不是单独的 root cause。
- “thermal hypothesis”仍需 limiter/event reason 等证据进一步区分 power vs thermal。
- queue pressure 也要确认 offered load 和 active capacity。

## Evidence to save

保存每个 case 的输出，并写三栏：Observed / Hypothesis / Next discriminating test。

## What this proves

你会从多指标模式生成可验证假设，并主动保留不确定性。

## What this does NOT prove

所有 telemetry 都是 synthetic；没有任何真实机器根因结论。

## No-hardware path

完整 L0。

## Transfer question

如果 TTFT 变差但 ITL、clock、temperature 都稳定，同时 deferred requests 上升，你会优先查 GPU 热问题还是 queue？为什么？

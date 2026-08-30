# Experiment 62 — Serving Tail-Latency Trace Analyzer

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/serving-slo-timeline.svg" alt="Serving trace 要把 queue、prefill、decode 与请求完成放在时间线上看；平均延迟不能代替 p95/p99 尾延迟。">
  <figcaption>Serving trace 要把 queue、prefill、decode 与请求完成放在时间线上看；平均延迟不能代替 p95/p99 尾延迟。</figcaption>
</figure>

## Goal

Learn to compute:
- queue wait;
- TTFT;
- E2E;
- request-level mean ITL;
- p50/p95/p99;
- request throughput;
- output-token throughput;
- SLO compliance.

The bundled CSV is **synthetic**.

## Run

```bash
python3 analyze_trace.py trace-synthetic.csv
```

Default SLO:

```
TTFT <= 500 ms
AND
mean ITL <= 80 ms
for >= 99% of requests
```

## Why the trace is useful

11 requests have TTFT between 100–150 ms.

One request queues for 1000 ms and gets:

```
TTFT = 1200 ms
```

All requests have request-level mean ITL:

```
50 ms
```

This isolates the idea:

```
queue tail
→ TTFT tail
```

without changing active-generation cadence.

## Percentile method

The script deliberately uses:

```
nearest-rank
rank = ceil(p × N)
```

Other tools can use different estimators.

## Scope

This trace is not a continuous-batching simulator and contains no real hardware result.

It is a metric-reading exercise.


## Why this experiment

平均延迟可以把少数非常差的用户体验藏掉。这个实验故意只制造一个 queue outlier，让你看到 p95/p99、SLO compliance 与 mean 的差异。

## Hypothesis

因为 active-generation cadence 固定，ITL 应保持稳定；唯一严重 queue wait 应主要拉高 TTFT tail，并可能使严格 SLO 失败。

## Fixed variables

使用同一 synthetic trace 和同一 percentile estimator。不要一边改 trace 一边比较阈值。

## What to observe

1. queue wait 如何进入 TTFT。
2. mean TTFT 与 p95/p99 的差别。
3. ITL 为什么仍然是 50ms。
4. request throughput 与 output-token throughput 的单位区别。
5. 默认 SLO 中到底是哪一条 gate 被 outlier 影响。

## Troubleshooting

- percentile estimator 不同，结果可能略有差异，必须记录算法。
- chunk gap 不一定是真 token ITL。
- client TTFT 包含 queue/transport 等，不是纯 GPU prefill。

## Evidence to save

保存 trace、命令、分析输出，并自己指出那一条 outlier request 在时间线上的位置。

## What this proves

你会从 request trace 计算 tail latency 与 SLO，而不是只看平均值。

## What this does NOT prove

它不是 continuous-batching simulator，也没有任何真实 GPU 性能。

## No-hardware path

完整 L0。

## Transfer question

如果平均 TTFT=180ms、p99=4s，你会向交互聊天用户只汇报“平均 180ms”吗？为什么？

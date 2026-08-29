# Experiment 66 — Overload / Retry Amplification Model

硬件等级：L0

## Goal

Compare four synthetic overload policies.

Workload:

```
10 original requests
arrival spacing = 0.5 s
service time = 1.0 s
one active server
```

Scenarios:
1. unbounded queue;
2. queue limit 2, no retry;
3. queue limit 2, immediate retry every 0.1 s, max 3 retries;
4. queue limit 2, deterministic exponential backoff 0.5/1/2 s.

## Run

```bash
python3 simulate.py
```

## Key expected result

Immediate retry:

```
10 originals
→
19 total attempts
```

while completed originals remain:

```
7
```

the same as bounded/no-retry.

That is retry amplification without benefit.

## Caveat

The model uses:
- deterministic arrivals;
- one server;
- fixed service time;
- FIFO queue;
- no jitter.

It is a teaching model, not a production queue simulator.


## Why this experiment

过载时“多重试几次”看起来像提高可靠性，实际上可能把一个容量问题放大成重试风暴。本实验用最小队列模型把这种反馈环画出来。

## Hypothesis

立即短间隔 retry 会显著增加 total attempts，却不一定增加 completed originals；带 backoff 的策略可能降低放大效应，但仍需在成功率与等待时间之间做 tradeoff。

## Fixed variables

original workload、service time、server 数和 FIFO 规则保持不变，只改变 queue/retry policy。

## What to observe

1. completed originals。
2. total HTTP attempts。
3. reject/drop 数。
4. wait/tail latency。
5. 为什么“最终成功”仍可能有糟糕 UX。

## Troubleshooting

- 不要把 attempt count 当 original request count。
- 比较 policy 时保持同一 arrival trace。
- 真实系统通常需要 jitter；本 toy 的 deterministic backoff 只是教学。
- client timeout 不代表 server work 自动取消。

## Evidence to save

保存四种 scenario 输出，做一张表：policy / attempts / completed / rejected / tail wait。

## What this proves

你能识别 retry amplification，并理解 bounded queue、reject、backoff 的基本关系。

## What this does NOT prove

它不模拟真实 continuous batching、network jitter、多个 server、动态 service time 或 cancellation。

## No-hardware path

完整 L0。

## Transfer question

一个 server 已经持续过载时，为什么把 max retries 从 3 提到 20 可能让成功率更差而不是更好？

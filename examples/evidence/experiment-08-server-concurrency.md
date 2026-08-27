---
experiment_id: example-server-slots-continuous-batching
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

slots、queue 与 continuous admission 如何同时影响 aggregate throughput 和 first-token wait？

## Hardware

无特殊硬件。

## Software

Python 3。

## Configuration

Part A：

- 8 requests
- each 32 output tokens
- all arrive at t=0
- slots = 1 / 2 / 4 / 8 / 16
- synthetic step_time(batch) = 1 + 0.22 × (batch - 1)

Part B：

- request lengths = 8,32,8,32,8,32
- slots=2
- compare static groups vs continuous admission

## Raw Results

### Part A

| slots | active step | makespan | aggregate tok/u | avg first-token wait proxy | max first |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.00 | 256.00 | 1.000 | 113.00 | 225.00 |
| 2 | 1.22 | 156.16 | 1.639 | 59.78 | 118.34 |
| 4 | 1.66 | 106.24 | 2.410 | 28.22 | 54.78 |
| 8 | 2.54 | 81.28 | 3.150 | 2.54 | 2.54 |
| 16 | 2.54 | 81.28 | 3.150 | 2.54 | 2.54 |

### Part B

| strategy | makespan | aggregate tok/u | avg first-token wait |
|---|---:|---:|---:|
| static groups | 101.28 | 1.185 | 34.98 |
| continuous admission | 82.56 | 1.453 | 20.74 |

## Observations

1. slots 增加减少 queue waves。
2. active batch 增大时，synthetic step time 也增大。
3. aggregate throughput 上升，但远低于线性 slots 倍率。
4. slots 超过请求数以后没有额外并发价值。
5. mixed-length workload 下，continuous admission 能把短请求完成后留下的 slot 立即交给 queued request。

## Conclusion

Server concurrency 有至少三个不同方向：

~~~text
slots ↑
→ queue wait ↓

active batch ↑
→ aggregate throughput opportunity ↑

active batch ↑
→ per-step time / user cadence cost may ↑
~~~

continuous batching 的主要教学价值是：

~~~text
active set can change while other requests are still decoding
~~~

它不是“免费把模型变快”。

## Reproducibility

见：

- labs/experiments/11-server-slots-continuous-batching/simulate.py
- labs/experiments/11-server-slots-continuous-batching/EXPECTED.md

## Boundary

所有 time-unit 都是 synthetic。

真实 llama-server 结果必须由 Experiment 12 产生，并保存 runtime/model/raw metrics。

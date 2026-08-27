# Experiment 11 — Slots、Queue 与 Continuous Batching 概念实验

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

## 问题

为什么 server slots 增加时：

- aggregate throughput 可能上升；
- queue wait 可能下降；
- active-user token cadence 却可能变慢？

continuous batching 又为什么比固定 static groups 更适合长短请求混合？

## 模型

每个 decode step：

- 对每个 active request 产生 1 token；
- batch 越大，step 越慢；
- 但成本低于线性增长。

抽象公式：

~~~text
step_time(batch) = 1 + 0.22 × (batch - 1)
~~~

这不是任何真实 GPU 的 timing model。

它只用来隔离：

~~~text
queue
batch amortization
per-user cadence
dynamic admission
~~~

## Part A — 8 个同时到达的等长请求

配置：

- 8 requests
- each 32 output tokens
- all arrive at t=0
- slots = 1 / 2 / 4 / 8 / 16

运行：

~~~bash
python simulate.py
~~~

观察：

- makespan
- aggregate tokens / time-unit
- average first-token wait proxy
- max first-token wait proxy
- active step time

注意 first-token wait proxy：

- 包含 queue + first decode step；
- 不包含真实 prompt processing / tokenization / network。

所以不要把它叫真实 TTFT。

## Part B — Static vs Continuous

请求 output lengths：

~~~text
8, 32, 8, 32, 8, 32
~~~

slots=2。

### Static groups

先固定两两成组。

即使短请求完成，也要等同组长请求结束，下一组才能进来。

### Continuous admission

任何 request 完成后，queue 中下一个 request 立刻填入空 slot。

## Expected insight

continuous batching 不要求：

~~~text
所有 request 同时开始
所有 request 同时结束
~~~

它让 active set 动态变化。

## Evidence

回答：

1. 为什么 slots 1→8 时 aggregate throughput 不是 8×？
2. 为什么 slots 越多 active step time 反而增加？
3. 为什么 queue wait 同时下降？
4. static groups 为什么在长短请求混合时浪费 slot？
5. slots=16 为什么对只有 8 个请求没有进一步收益？
6. 这个模型为什么不能用来预测真实 llama-server 的 tok/s？

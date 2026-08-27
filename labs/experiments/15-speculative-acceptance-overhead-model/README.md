# Experiment 15 — Acceptance × Draft Length × Overhead

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

## 问题

为什么：

~~~text
acceptance 高
~~~

不等于：

~~~text
draft 越长越快
~~~

甚至 acceptance 较低时 speculation 可能慢于 baseline？

## Simplified model

Baseline：

~~~text
target serial cost / token = 1.0
~~~

Speculative round：

~~~text
draft D tokens
→ cost = 0.08 × D

target verifies draft batch
→ cost = 1.08 + 0.04 × D
~~~

Total：

~~~text
spec round cost
= 1.08 + 0.12 × D
~~~

Assume each draft position survives independently with probability p until first rejection.

Expected progress：

~~~text
1 + p + p² + ... + p^D
~~~

Speedup ceiling：

~~~text
expected baseline time for same progress
----------------------------------------
spec round cost
~~~

Since baseline target time/token = 1：

~~~text
speedup = expected progress / spec round cost
~~~

## 运行

~~~bash
python simulate.py
~~~

## Sweep

Acceptance：

~~~text
30%
60%
90%
~~~

Draft length：

~~~text
1
2
4
8
~~~

## 你应该看到

### p=0.30

~~~text
D=1 → 1.083×
D=2 → 1.053×
D=4 → 0.914×
D=8 → 0.700×
~~~

长 draft 反而亏。

### p=0.60

~~~text
D=2 around best in this cost model
D=8 loses much of the gain
~~~

### p=0.90

长 draft 继续有价值：

~~~text
D=8 → ~3.00× model ceiling
~~~

## Sensitivity

再运行：

~~~bash
python simulate.py --draft-cost 0.16
~~~

观察 proposer 变慢后 optimum 如何左移。

或者：

~~~bash
python simulate.py --verify-base 1.35
~~~

观察 target verification overhead 变高后的结果。

## 重要限制

这个模型不是：

- exact speculative-sampling probability model；
- real GPU latency model；
- llama.cpp performance predictor；
- tree speculation simulator。

它只训练一个判断：

~~~text
useful accepted progress
must beat
proposal + verification overhead
~~~

## Evidence

回答：

1. p=0.3 为什么 D=8 的 expected progress 几乎不比 D=4 高？
2. p=0.6 为什么 D=2 可能比 D=8 更快？
3. proposer cost 翻倍时 optimum 怎么变化？
4. acceptance 不变但 verification cost 上升，speedup 为什么下降？
5. 为什么 real benchmark 还要记录 concurrency？
6. two-model speculation 为什么还要记录 VRAM/offload？

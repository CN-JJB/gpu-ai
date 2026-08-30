# Experiment 15 — Acceptance × Draft Length × Overhead

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3

<figure>
  <img src="../../../assets/diagrams/experiment-speculative-acceptance-flow.svg" alt="Speculative decoding 的收益来自 accepted tokens/cycle，同时要扣掉 draft 与 target verification 的额外成本。">
  <figcaption>Speculative decoding 的收益来自 accepted tokens/cycle，同时要扣掉 draft 与 target verification 的额外成本。</figcaption>
</figure>

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


## Hypothesis

Speculation 只有在 expected useful progress 足以覆盖 draft + verification overhead 时才有正收益；acceptance 较低或 proposer/verification 太贵时，增加 draft length 会出现收益递减甚至负收益。

## Fixed variables

一次 sweep 固定 cost model，只改变 p 和 D；Sensitivity 实验一次只改 draft-cost 或 verify-base。

## What to observe

- p=0.3/0.6/0.9 下 optimal D 的变化；
- expected progress 对 D 的饱和；
- proposer 变慢时 optimum 左移；
- verification overhead 增加时所有 speedup 下移；
- speedup ceiling 与真实 end-to-end speedup 的边界。

## Troubleshooting

- p 是 toy independent survival probability，不是真实 acceptance trace。
- 不能用模型 ceiling 宣布某 runtime 会 3×。
- two-model path 还会消耗额外 VRAM/带宽。
- concurrency 会改变 proposer/target scheduling，因此真实 benchmark 必须记录。

## What this proves

你能解释 acceptance、draft length 与 overhead 三者共同决定 speculative opportunity。

## What this does NOT prove

它不预测 llama.cpp、tree speculation 或任何具体模型组合的性能。

## No-hardware path

完整 L0。

## Transfer question

acceptance 从 90% 降到 60%，为什么“继续把 draft length 拉长”可能反而更慢？

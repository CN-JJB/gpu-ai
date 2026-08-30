# Experiment 01 — 为什么统一执行池能减少有人忙死、有人闲着？

Hardware level: L0  
Risk: safe  
需要：Python 3

<figure>
  <img src="../../../assets/diagrams/gpu-evolution-causal-timeline.svg" alt="从固定功能到统一执行资源：这个实验只聚焦“固定分区为什么会浪费、统一池为什么能减少结构性闲置”。">
  <figcaption>从固定功能到统一执行资源：这个实验只聚焦“固定分区为什么会浪费、统一池为什么能减少结构性闲置”。</figcaption>
</figure>

## 问题

假设一块抽象 GPU 有 128 个执行单元，其中 64 个只能做 Vertex，64 个只能做 Pixel。

如果工作量突然变成 80% Vertex、20% Pixel，会发生什么？

另一种抽象设计让 128 个单元可以统一分配，但付出 5% 调度和通用化开销，会怎样？

## 运行

~~~bash
python simulate.py
~~~

## 观察

- workload 比例匹配固定分区时，固定设计可以非常高效。
- workload 严重偏斜时，一类固定单元会闲置，另一类成为瓶颈。
- 统一池能把资源重新分给更忙的一类，因此偏斜 workload 下利用率更稳定。
- 统一设计不是魔法：如果 workload 完美匹配固定硬件，而且统一化有开销，它未必更快。

## 注意

这不是现实 GPU 周期模拟器，只保留静态资源分区 vs 动态共享资源池这个概念。

## Evidence

提交 Experiment Card，并回答：
1. 为什么 balanced 场景里 fixed 反而略快？
2. 为什么这不能推出所有硬件都应该统一？
3. Tensor Core 的出现为什么不和 Unified Shader 的历史矛盾？


## Hypothesis

当 workload 比例与固定 50/50 分区严重不匹配时，统一池应减少闲置资源；当 workload 恰好匹配固定分区时，固定设计可能因无通用化开销而略优。

## Fixed variables

总执行单元固定为 128；固定设计保持 64/64；统一池保持 5% 教学开销。只改变 Vertex/Pixel workload 比例。

## Procedure

先运行默认场景，再把比例改成 50/50、90/10、10/90。每次只改 workload ratio，并记录 fixed utilization、unified utilization 和 winner。

## What to record

做一张三列表：workload ratio / fixed utilization / unified utilization。再写一句解释“哪里出现闲置”。

## Expected pattern

- 50/50：固定分区很匹配，统一池未必更好。
- 80/20、90/10：固定分区一边排队、一边闲置；统一池更稳定。
- 把 5% 开销改大时，统一化需要更强的 workload imbalance 才值得。

## Troubleshooting

如果结果和直觉相反，先检查利用率定义是否按“完成的有效工作 / 总资源能力”计算，而不是简单把两类百分比相加。

## No-hardware fallback

本实验本身就是 L0 fallback，不需要任何 GPU。

## What this proves

统一资源池能改善不均衡 workload 下的静态分区浪费。

## What this does NOT prove

它不证明现实 Unified Shader 在所有 workload 上都更快，也不模拟 cache、scheduler、专用单元等真实 GPU 细节。

## Transfer

把 Vertex/Pixel 换成“不同类型 kernel/work queue”，你仍然可以用同一思路理解动态资源共享。

# Experiment 01 — 为什么统一执行池能减少有人忙死、有人闲着？

Hardware level: L0  
Risk: safe  
需要：Python 3

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

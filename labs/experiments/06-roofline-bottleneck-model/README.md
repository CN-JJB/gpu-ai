# Experiment 06 — 算力翻倍和带宽翻倍，谁能加速你的 workload？

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3  
替代路径：手算公式也可以。

## 问题

我们造三张完全抽象的 GPU：

### GPU A

- compute = 20 TFLOP/s
- bandwidth = 500 GB/s

### GPU B

只把 compute 翻倍：

- compute = 40 TFLOP/s
- bandwidth = 500 GB/s

### GPU C

只把 bandwidth 翻倍：

- compute = 20 TFLOP/s
- bandwidth = 1000 GB/s

对不同 arithmetic intensity 的 workload：

~~~text
AI = 0.25, 1, 4, 16, 40, 80, 160 FLOP/B
~~~

哪张更快？

## 公式

~~~text
memory roof = bandwidth × arithmetic intensity
performance ceiling = min(compute roof, memory roof)
ridge = compute / bandwidth
~~~

单位换算：

~~~text
TFLOP/s × 1000 / GB/s = FLOP/B
~~~

## 运行

~~~bash
python simulate.py
~~~

## Expected shape

~~~text
GPU A: 20 TFLOP/s, 500 GB/s, ridge=40 FLOP/B
AI=  0.25 ->   0.125 TFLOP/s  memory-bound
AI=  1.00 ->   0.500 TFLOP/s  memory-bound
AI=  4.00 ->   2.000 TFLOP/s  memory-bound
AI= 16.00 ->   8.000 TFLOP/s  memory-bound
AI= 40.00 ->  20.000 TFLOP/s  ridge/compute ceiling
AI= 80.00 ->  20.000 TFLOP/s  compute-bound
AI=160.00 ->  20.000 TFLOP/s  compute-bound
~~~

然后比较 GPU B/C。

## 你应该发现

### AI=4

- A = 2 TFLOP/s
- B = 2 TFLOP/s
- C = 4 TFLOP/s

只加 compute 没用。

### AI=80

- A = 20 TFLOP/s
- B = 40 TFLOP/s
- C = 20 TFLOP/s

这时只加 bandwidth 没用。

## 迁移到现实

真实卡不会刚好达到 roof。

Roofline 只是上限：

~~~text
achieved <= roof
~~~

如果实际性能远低于 roof，还要查：
- occupancy；
- scheduler stalls；
- coalescing；
- cache；
- bank conflicts；
- software path；
- launch/configuration。

## Evidence

提交 Experiment Card，并回答：

1. GPU A 的 ridge 为什么是 40 FLOP/B？
2. GPU B 算力更高，为什么 AI=4 时没有收益？
3. GPU C 带宽更高，为什么 AI=80 时没有收益？
4. 上一节 tile 16 → tile 32，本质上如何改变 AI？
5. 如果真实 kernel 只有 Roofline 上限的 30%，你为什么不能直接怪显存带宽？
6. 对 decode-heavy 本地 LLM，你会优先查哪些 hardware/software 指标？

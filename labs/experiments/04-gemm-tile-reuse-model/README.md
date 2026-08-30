# Experiment 04 — Tile 为什么能减少 global-memory load requests？

Hardware level: L0  
Risk: safe  
Cost: 0  
需要：Python 3  
替代路径：没有 Python 时可手算 N=8、tile=2 的小矩阵。

<figure>
  <img src="../../../assets/diagrams/gpu-memory-hierarchy-reuse.svg" alt="Tile reuse 的核心是让同一批数据在更近、更快的层级被多次消费，从而减少外部内存流量。">
  <figcaption>Tile reuse 的核心是让同一批数据在更近、更快的层级被多次消费，从而减少外部内存流量。</figcaption>
</figure>

## 问题

对一个简化的方阵 GEMM：

~~~text
C = A × B
~~~

naive 方案让每个 output element 独立做 K 次：

~~~text
load A
load B
multiply-add
~~~

如果一个 block 先把 A/B 的 tile 各加载一次到 shared memory/LDS，再让 tile 内所有 output threads 重用，算法级 global input-load requests 会发生什么变化？

## 模型

默认：

- N = 1024
- FP32 = 4 bytes
- tile widths = 4, 8, 16, 32
- 每个 output element 仍做同样的 2N FLOPs
- naive：每个 output 的每个 K step 都发出 A+B 两个 input load requests
- tiled：每个 block、每个 K tile，只把 A tile 和 B tile 各加载一次

## 非常重要的限制

这个模型：

- **不模拟 cache**
- **不模拟 broadcast**
- **不模拟真实 memory transaction granularity**
- **不模拟 coalescing**
- **不模拟 bank conflicts**
- **不模拟 synchronization**
- **不模拟 register pressure**
- **不模拟真实 occupancy**

因此输出的 “bytes” 是由算法级 load/store requests 推导的概念流量，不等于 profiler 的 DRAM bytes。

## 运行

~~~bash
python simulate.py
~~~

## 你应该看到

~~~text
N=1024, FP32 concept model; counts algorithmic global element requests and ignores cache/broadcast effects
naive: input-load requests=2,147,483,648, approx bytes=8.004 GiB, arithmetic intensity=0.250 FLOP/B

  tile  threads/block   shared/block      input loads  load reduction   approx GiB    AI FLOP/B
----------------------------------------------------------------------------------------------------
     4             16         0.12 KiB      536,870,912            4.0x        2.004        0.998
     8             64         0.50 KiB      268,435,456            8.0x        1.004        1.992
    16            256         2.00 KiB      134,217,728           16.0x        0.504        3.969
    32           1024         8.00 KiB       67,108,864           32.0x        0.254        7.877
~~~

## 解释

在理想 tile reuse 模型里：

tile width = T
→ A/B tile 被 T 个 output positions 重用
→ input-load requests 近似减少 T 倍。

同时，tile 越大：

- shared-memory/LDS footprint 增加；
- threads/block 在这个简单 1-thread-per-output 模型里按 T² 增加。

tile 32 已经需要 1024 threads/block。

这就是关键 trade-off：

**reuse 不是免费的，它拿片上资源和并行调度空间换 global traffic。**

## Evidence

提交 Experiment Card，并回答：

1. tile 16 为什么在本模型中正好把 input-load requests 减少 16×？
2. 为什么这个 16× 不能直接写成“真实 GPU 显存流量减少 16×”？
3. tile 32 比 tile 16 的 reuse 更高，它可能在哪些资源上更糟？
4. coalescing 为什么没有被这个模型回答？
5. 把 shared memory/LDS 改成 registers，为什么不能让整个 block 随便共享这些数据？


## Hypothesis

在这个理想算法级模型中，tile width T 允许 A/B tile 被约 T 个 output positions 复用，因此 global input-load requests 近似减少 T 倍；但 tile 变大同时提高 threads/block 与 shared-memory footprint。

## Fixed variables

N、dtype、GEMM FLOPs 与 load-counting rule 固定，只改变 tile width。

## What to observe

- input-load reduction；
- conceptual bytes 与 arithmetic intensity；
- shared/block 与 threads/block；
- tile 16→32 的 reuse 收益与资源代价；
- 为什么 profiler DRAM bytes 可能与 toy bytes 不同。

## Troubleshooting

- 不要把算法级 load requests 当 memory transactions。
- cache/coalescing/broadcast/bank conflict 均未建模。
- tile 大到超出真实 thread/block/resource limit 时不能照搬。
- reuse 增强不等于 performance 一定线性提升。

## What this proves

你能解释 tiling 如何用片上资源交换 global-data reuse，并提高概念 arithmetic intensity。

## What this does NOT prove

它不预测真实 GEMM kernel 的 DRAM bytes、occupancy 或 speedup。

## No-hardware path

完整 L0，可手算 N=8/tile=2。

## Transfer question

tile 32 的概念 load reduction 比 tile 16 好，为什么真实 kernel 仍可能 tile 16 更快？

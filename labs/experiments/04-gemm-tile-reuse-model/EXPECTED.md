# Expected result

Verified with Python 3.

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

## Interpretation

### Naive

每个 output element 都独立做 N 次 multiply-add，并在每个 K step 发出一个 A load 和一个 B load。

算法级 input-load requests：

~~~text
N² outputs × N steps × 2 inputs = 2N³
~~~

### Tiled

tile width = T 时：

- 每 block 计算 T² outputs；
- 每个 K tile 只加载 T² 个 A + T² 个 B；
- 共 N/T 个 K tiles。

总 input-load requests：

~~~text
(N/T)² blocks × (N/T) K-tiles × 2T² loads
= 2N³ / T
~~~

因此理想 reuse factor 正好是 T。

## 为什么 arithmetic intensity 上升？

FLOPs 没变，算法级 global bytes 下降。

所以：

~~~text
FLOPs / global bytes ↑
~~~

这就是 tiling 在概念上把 workload 往 compute-heavy 方向推的原因。

## 不要过度解释

这些数字不能当真实 DRAM traffic。

现实 GPU 还有：
- caches；
- warp/wave broadcast；
- coalescing / transaction size；
- bank conflicts；
- prefetch；
- register allocation；
- shared/LDS occupancy limits；
- synchronization；
- compiler transformations。

Experiment 05 才会在真实 CUDA/HIP GPU 上测 timing 和 resource usage。

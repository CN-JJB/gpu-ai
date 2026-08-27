# Expected result

Verified with Python 3.

~~~text
Abstract Roofline model; these are not real GPUs.

GPU A: 20 TFLOP/s, 500 GB/s, ridge=40.0 FLOP/B (base)
  AI=  0.25 ->   0.125 TFLOP/s  memory-bound
  AI=  1.00 ->   0.500 TFLOP/s  memory-bound
  AI=  4.00 ->   2.000 TFLOP/s  memory-bound
  AI= 16.00 ->   8.000 TFLOP/s  memory-bound
  AI= 40.00 ->  20.000 TFLOP/s  ridge/compute ceiling
  AI= 80.00 ->  20.000 TFLOP/s  compute-bound
  AI=160.00 ->  20.000 TFLOP/s  compute-bound

GPU B: 40 TFLOP/s, 500 GB/s, ridge=80.0 FLOP/B (2x compute, same bandwidth)
  AI=  0.25 ->   0.125 TFLOP/s  memory-bound
  AI=  1.00 ->   0.500 TFLOP/s  memory-bound
  AI=  4.00 ->   2.000 TFLOP/s  memory-bound
  AI= 16.00 ->   8.000 TFLOP/s  memory-bound
  AI= 40.00 ->  20.000 TFLOP/s  memory-bound
  AI= 80.00 ->  40.000 TFLOP/s  ridge/compute ceiling
  AI=160.00 ->  40.000 TFLOP/s  compute-bound

GPU C: 20 TFLOP/s, 1000 GB/s, ridge=20.0 FLOP/B (same compute, 2x bandwidth)
  AI=  0.25 ->   0.250 TFLOP/s  memory-bound
  AI=  1.00 ->   1.000 TFLOP/s  memory-bound
  AI=  4.00 ->   4.000 TFLOP/s  memory-bound
  AI= 16.00 ->  16.000 TFLOP/s  memory-bound
  AI= 40.00 ->  20.000 TFLOP/s  compute-bound
  AI= 80.00 ->  20.000 TFLOP/s  compute-bound
  AI=160.00 ->  20.000 TFLOP/s  compute-bound
~~~

## Key interpretation

### AI=4

GPU B 的 compute 是 GPU A 的 2×，但 performance ceiling 完全相同。

原因：

~~~text
500 GB/s × 4 FLOP/B = 2000 GFLOP/s = 2 TFLOP/s
~~~

memory roof 先撞到。

### AI=80

GPU C 的 bandwidth 是 GPU A 的 2×，但两者都被 20 TFLOP/s compute roof 限制。

### Ridge point 不是“GPU 性能分数”

ridge 只是这个 GPU 的 compute-to-bandwidth balance。

更右的 ridge 并不自动更好；它表示 workload 需要更高 AI 才能真正利用全部 compute。

## Link to previous experiment

Experiment 04 中 tile reuse 把算法级 bytes 降低，从而提高 AI。

因此 memory optimization 可以把 workload：
- 在斜坡上往右上移动；
- 最终跨过 ridge；
- 之后 compute optimization 才成为主要方向。

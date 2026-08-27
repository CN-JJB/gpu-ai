---
experiment_id: example-gemm-tile-reuse-model
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

对简化方阵 GEMM，shared-memory/LDS tiling 能把算法级 global input-load requests 降低多少？tile size 增大时要付出哪些片上资源成本？

## Hardware

无特殊硬件；CPU 运行 Python 概念模型。

## Software

Python 3。

## Configuration

- N = 1024
- FP32
- tile widths = 4, 8, 16, 32
- naive：每 output、每 K step 独立请求 A+B
- tiled：每 block、每 K tile 只请求一次 A tile + B tile
- 不模拟 cache / broadcast / coalescing / bank conflicts / occupancy

## Procedure

运行：

~~~bash
python labs/experiments/04-gemm-tile-reuse-model/simulate.py
~~~

## Raw Results

| tile | threads/block | shared/block | input-load requests | reduction | approx AI |
|---:|---:|---:|---:|---:|---:|
| naive | — | 0 | 2,147,483,648 | 1× | 0.250 FLOP/B |
| 4 | 16 | 0.125 KiB | 536,870,912 | 4× | 0.998 FLOP/B |
| 8 | 64 | 0.5 KiB | 268,435,456 | 8× | 1.992 FLOP/B |
| 16 | 256 | 2 KiB | 134,217,728 | 16× | 3.969 FLOP/B |
| 32 | 1024 | 8 KiB | 67,108,864 | 32× | 7.877 FLOP/B |

## Observations

tile width = T 时，理想模型把算法级 input-load requests 从 2N³ 降为 2N³/T。

但 tile 增大同时让这个简单 kernel 的：
- threads/block 按 T² 增长；
- shared/LDS footprint 按 T² 增长。

因此 reuse 与 execution-resource pressure 同时上升。

## Conclusion

Tiling 的根本价值是 data reuse：

**把远端 global 数据加载一次，在更近的 shared/LDS 和 registers 中使用多次。**

这提高 arithmetic intensity，但不是免费优化。

tile 32 在概念上比 tile 16 少一半 input-load requests，却已经达到 1024 threads/block，并消耗更大片上资源。真实 GPU 还需要检查 occupancy、register pressure、bank conflicts、coalescing、cache、parallel tiles 和 measured throughput。

## Reproducibility

见：

- labs/experiments/04-gemm-tile-reuse-model/simulate.py
- labs/experiments/04-gemm-tile-reuse-model/EXPECTED.md

## Sources

- NVIDIA CUDA C++ Best Practices Guide — Shared Memory in Matrix Multiplication
- NVIDIA Matrix Multiplication Background
- NVIDIA CUTLASS — Efficient GEMM in CUDA
- AMD ROCm HIP — Performance guidelines

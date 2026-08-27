---
experiment_id: example-unified-shader-load-balance
date: 2026-08-26
hardware_level: L0
risk_level: safe
status: reference-example
---

# Question

静态 50/50 执行资源分区和统一资源池，在 workload 比例变化时会有什么差异？

## Hardware

无特殊硬件；CPU 运行 Python 概念模型。

## Software

Python 3。

## Configuration

固定模型：128 单元，Vertex 64，Pixel 64。  
统一模型：128 单元，共享；人为加入 5% 通用化/调度开销。

## Procedure

分别运行 vertex-heavy、balanced、pixel-heavy 三种 workload。

## Results

- vertex-heavy：fixed 62.5% utilization，unified 95.2%，模型速度比约 1.52x。
- balanced：fixed 100%，unified 95.2%，统一模型约 0.95x。
- pixel-heavy：与 vertex-heavy 对称。

## Conclusion

统一资源池的价值来自适应 workload mix，而不是无条件提高峰值效率。现实 GPU 的 Unified Shader 也不能理解成所有功能都变通用；纹理、ROP、矩阵等专用单元仍然存在。

## Reproducibility

见 labs/experiments/01-unified-shader-load-balancing/simulate.py 和 EXPECTED.md。

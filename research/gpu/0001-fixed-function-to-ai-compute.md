# Research Note 0001 — 从固定功能 GPU 到 AI 计算

日期：2026-08-26

## Research question

GPU 从图形专用硬件演进到现代 AI/LLM 计算平台，最关键的可编程性与资源组织转折是什么？

## Primary sources

1. NVIDIA CUDA Programming Guide — Introduction  
   https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/introduction.html  
   GPU 起初是 3D 图形固定功能硬件，随后逐代变得可编程；NVIDIA 在 2006 年引入 CUDA，使计算不必依赖图形 API。

2. NVIDIA Research — A User-Programmable Vertex Engine, SIGGRAPH 2001  
   https://research.nvidia.com/publication/2001-08_user-programmable-vertex-engine  
   GeForce3 vertex engine 从高度优化的固定功能 pipeline 演进出用户可编程 vertex engine。

3. NVIDIA GeForce 8 Series Tech Specs  
   https://www.nvidia.com/en-us/drivers/geforce-8600-8500-tech-specs/  
   GeForce 8 系列公开标注 unified shader architecture、GigaThread 和 Shader Model 4。

4. NVIDIA CUDA Refresher  
   https://developer.nvidia.com/blog/cuda-refresher-getting-started-with-cuda/  
   CUDA 第一版于 2006 年 11 月发布；blocks、shared memory、barriers 等抽象使 GPU 通用并行计算更直接。

5. NVIDIA Volta Architecture  
   https://www.nvidia.com/en-sg/data-center/volta-gpu-architecture/  
   Volta 将 Tensor Cores 作为深度学习矩阵计算加速单元引入。

6. NVIDIA Volta Architecture Whitepaper  
   https://www.nvidia.com/content/gated-pdfs/Volta-Architecture-Whitepaper-v1.0.pdf  
   白皮书描述 V100 Tensor Core、矩阵乘加以及 GEMM 在神经网络训练和推理中的核心作用。

7. AMD ROCm HIP — Hardware implementation  
   https://rocmdocs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html  
   AMD 以 CU 为基本执行块，GCN 使用 wavefront、SIMD、LDS；CDNA 面向 HPC/ML 增加矩阵加速。

## Findings

### F1 — GPU 变成 AI 处理器不是一次跳跃
更合理的因果链是：固定功能图形 → 局部可编程 → 大量可编程并行执行资源 → 通用计算编程模型 → 针对矩阵热点的专用数据通路。

### F2 — 可编程 Shader 的首要价值是表达能力
GeForce3 的代表性变化不是简单跑得更快，而是允许开发者写此前固定流水线表达不了的处理。

### F3 — Unified Shader 解决静态资源分区问题之一
vertex/pixel/geometry 工作量随场景变化时，固定数量的专用执行资源可能一边繁忙、一边闲置。统一执行池能动态分配可编程资源。它不表示所有 GPU 单元都统一。

### F4 — CUDA 是编程模型转折
CUDA 把线程、block、shared memory、barrier 等概念直接暴露给通用计算。图形和计算继续共存。

### F5 — Tensor Core 是重新专用化
深度学习让 GEMM/矩阵乘加成为高价值热点后，GPU 在可编程通用架构内部加入专用矩阵数据通路。现代 GPU 是通用并行执行 + 专用加速单元 + 复杂内存系统的组合。

### F6 — 概念可迁移，术语不能硬等价
NVIDIA 的 SM/warp/shared memory/Tensor Core 可与 AMD 的 CU/wavefront/LDS/MFMA 或 matrix acceleration 做功能对照，但不能假设微架构相同。

## Claims to avoid

- 不把厂商自称世界第一之类营销绝对化为行业历史。
- Unified Shader 不等于 CUDA。
- Tensor Core 不等于 LLM 专用单元。
- 有 Tensor Core 不代表任何后端、任何模型都一定更快。

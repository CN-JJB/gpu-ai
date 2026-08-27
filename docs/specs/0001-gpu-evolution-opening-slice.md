---
status: active
skills:
  - teach
  - research
  - domain-modeling
---

# Spec 0001 — GPU 演进开篇垂直切片

## Problem Statement

学习者经常从 CUDA Core、Tensor Core、TFLOPS、显存这些现代名词开始，缺少一个因果模型：GPU 为什么从图形专用流水线变成高度可编程的大规模并行处理器，又为什么进一步加入矩阵加速单元。没有这条因果链，就很难把架构差异迁移到本地 LLM 的硬件选择。

## Solution

用一个短、自包含的开篇 Lesson 建立五阶段因果链：

1. 固定功能图形流水线：快但不灵活。
2. 可编程 Shader：允许开发者在部分阶段运行自定义程序。
3. Unified Shader：不同 shader 工作共享一类执行资源，改善负载不平衡。
4. CUDA/GPGPU：把通用并行计算从借图形 API 做计算变成正式编程模型。
5. Matrix/Tensor acceleration：当深度学习中矩阵乘成为高价值热点后，GPU 增加专用矩阵数据通路。

Lesson 不把 NVIDIA 历史包装成整个 GPU 行业唯一历史；NVIDIA 作为代表性主线，AMD 的 CU/wavefront/CDNA 作为迁移对照。

## User Stories

1. 作为电脑爱好者，我希望知道显卡为什么会变成 AI 卡，从而不把现代 GPU 术语当成孤立名词。
2. 作为垃圾佬，我希望理解统一执行资源的价值，从而能看懂不同架构的执行单元设计。
3. 作为本地 LLM 用户，我希望知道 Tensor/Matrix 单元为什么出现，从而理解游戏性能与 AI 性能不能简单画等号。
4. 作为初学者，我希望不用独显也能完成第一个实验，从而立即获得可观察结果。
5. 作为未来的硬件调查者，我希望学会把厂商营销语言与可验证架构事实分开。

## Implementation Decisions

- Lesson 采用 HTML，复用共享 CSS 和交互组件。
- Research note 先保存原始来源与事实，再进入 Reference 和 Lesson。
- Reference 保存稳定演进框架，不放当前市场价格。
- L0 实验使用 Python 模拟固定分区 vs 统一池的负载利用率，不声称它是任何真实 GPU 的周期精确模型。
- 交互网页使用相同抽象，让学习者拖动 workload mix 即时观察利用率。
- Lesson 结尾必须把因果链映射回 LLM：矩阵乘、低精度、高吞吐、内存系统。

## Testing Decisions

- Python 模拟器验证 vertex-heavy、balanced、pixel-heavy 三种场景。
- 固定 64/64 分区在偏斜 workload 下应出现明显空闲；balanced 应接近满利用。
- 统一池模型保留 5% 抽象开销，避免制造统一设计永远更快的错误结论。
- HTML 交互只作为概念可视化，不作为真实 GPU benchmark。

## Out of Scope

完整图形学、全部厂商型号史、CUDA kernel 细节、Tensor Core 指令级编程、真实硬件排名。

## Completion Criteria

Research → Reference → HTML Lesson → L0 Experiment 全部存在且互相链接；事实来源可追溯；实验结果与 Lesson 结论一致。

---
date: 2026-08-26
type: course-build-record
---

# First vertical slice validated

第一次用新仓库架构完成完整闭环：

Spec → Research → Reference → HTML Lesson → Interactive Asset → L0 Experiment → Expected Result → Example Evidence。

## Architecture lessons

- 稳定知识与动态情报分层可以自然工作；本切片没有把当前价格或型号排名写进 Lesson。
- teach + research 的组合适合内容生产：先建立学习目标，再研究一手来源。
- scaffold-exercises 的 problem/solution/explainer 思路有价值，但本课程不沿用其 TypeScript/ai-hero 专属 lint 约束。
- Experiment Card 应同时支持真实硬件实验和 L0 概念模型。
- 对厂商历史必须保留 source bias 意识，避免把公司营销话术变成行业绝对事实。

## Next

进入 GPU 执行模型：thread → warp/wavefront → SM/CU → scheduler → latency hiding，并继续使用最小实验验证。

---
date: 2026-08-26
type: course-build-record
---

# GPU execution-model vertical slice completed

第二个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → Example Evidence → optional L2 real-GPU Experiment → Learning update。

## Built artifacts

- research/gpu/0002-execution-model-latency-hiding.md
- reference/gpu/execution-model-thread-warp-sm-latency.md
- lessons/02-gpu-execution-model/01-thread-warp-sm-scheduler-latency.html
- labs/experiments/02-latency-hiding-scheduler-model/
- labs/experiments/03-real-gpu-latency-hiding/
- examples/evidence/experiment-02-latency-hiding.md
- learning/CURRENT.md

## Research conclusions

- NVIDIA 的稳定主线是 thread block → SM residency → 32-thread warp → warp scheduler → ready warp issue。
- AMD 可以做作用层迁移：work-group → CU → wavefront/warp → scheduler；但 Wave32/Wave64、WGP/CU 组织和具体 pipeline 不能硬套 NVIDIA。
- NVIDIA 与 AMD 官方资料都把大量 resident warps/wavefronts 与 latency hiding 联系起来。
- registers 与 shared memory/LDS 会限制 resident blocks/groups 与 occupancy。
- 重要纠偏：occupancy 是 latency-hiding headroom，不是性能分数；更高 occupancy 不总等于更高 performance。

## Teaching decisions

### L0 first

继续遵守“无独显也能开始”。L0 simulator 只模拟一个 scheduler、一个 issue slot 和长延迟 dependency，用最小机制让学习者亲眼看到：

更多 ready resident groups
→ fewer idle cycles
→ better issue utilization
→ diminishing returns after enough concurrency。

没有把它包装成真实 GPU 周期模拟器。

### L2 as optional evidence

增加真实 CUDA/HIP 实验：用 dependent pointer chain 制造 latency-sensitive workload，再用 dynamic shared memory/LDS 改变 per-block resource footprint。

程序调用 CUDA/HIP occupancy API 报告 theoretical active blocks，并测真实 throughput。这样 Evidence 不只报数字，还能把资源限制、occupancy 和 throughput 放在同一张 Experiment Card 里。

本 build 环境没有可用于课程 benchmark 的 NVIDIA/AMD GPU，因此没有伪造 L2 结果；该路径明确标记为等待 learner hardware evidence。

## Skill workflow notes

- 使用 teach：保持短 lesson、真实问题、retrieval practice、ZPD 与 Evidence 导向。
- 使用 research：真实课程事实先从 NVIDIA CUDA 与 AMD ROCm/HIP 官方一手资料建立 research note，再压缩进 reference/lesson。
- 借用 scaffold-exercises 的 problem/solution/explainer 与可验证练习思想，但没有引入其 TypeScript/ai-hero 专属约束。
- 未触发 domain-modeling：本切片没有改变 CONTEXT.md 的领域语言边界。
- 未触发 to-spec / grill：v1 需求与当前 bounded slice 已冻结清楚。

## Validation

L0 模型期望值已用 Python 逻辑验证：

- 1 resident group：20.8% issue utilization
- 8 groups：76.4%
- 16 groups：94.4%
- 32 groups：100%

这个结果同时构造了“occupancy 边际收益递减”的最小反例。

## Next

进入 registers / shared memory-LDS / tiling / memory hierarchy，继续把 execution model 接到 GEMM 与 Attention kernel 的真实资源 trade-off。

# Handoff — GPU × Local LLM Course

## Next session focus

Continue building the course from the validated first vertical slice. The next bounded slice is:

**thread → warp/wavefront → SM/CU → scheduler → latency hiding**

The goal is to keep the same production loop:

**Research → Reference → Lesson → Experiment → Evidence → Learning update**

## Repository

- Repo: CN-JJB/llm-course
- Branch: course-v1
- Working branch URL: https://github.com/CN-JJB/llm-course/tree/course-v1

## Read first

1. `MISSION.md`
2. `AGENTS.md`
3. `CONTEXT.md`
4. `COURSE-MAP.md`
5. `skills/SKILL-MAP.md`
6. `skills/WORKFLOWS.md`
7. `learning/PROFILE.md`
8. `learning/CURRENT.md`

Then inspect the first completed vertical slice:

- `docs/specs/0001-gpu-evolution-opening-slice.md`
- `research/gpu/0001-fixed-function-to-ai-compute.md`
- `reference/gpu/evolution-fixed-to-ai.md`
- `lessons/01-gpu-evolution/01-fixed-function-to-unified-compute.html`
- `labs/experiments/01-unified-shader-load-balancing/`
- `examples/evidence/experiment-01-unified-shader.md`
- `learning/records/2026-08-26-first-vertical-slice.md`

## Requirements already frozen

Do not reopen course scope unless a contradiction is discovered.

Core ability stack:

**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Core teaching pattern:

**真实问题 → 必要原理 → 小实验 → 可玩项目 → 结果分析 → 如何选择 → 如何迁移到其他平台/硬件**

Other important constraints:
- Self-study first.
- No discrete GPU required to begin.
- Linux is the main practical platform.
- GPU architecture evolution opens the course.
- NVIDIA primary, AMD systematic secondary, Apple special section, Intel lighter.
- Consumer + professional/data-center/OEM/special cards are in scope.
- LLM is the primary AI workload.
- Stable knowledge is separated from dynamic intelligence.
- Important experiments use Experiment Card and reproducible conditions.
- Mainline milestones + Challenge Labs.
- China secondhand market primary, global technical/community intelligence secondary.
- Research is used when writing real content, not for endless architecture discussion.
- Prefer reusing open-source implementations before building tools from scratch.

## Matt Pocock skills

Use the repository's skill routing, not every skill mechanically.

Likely skills for the next slice:
- `teach`
- `research`
- `domain-modeling` only if terminology changes
- `wait-what` when a learner explanation needs repair
- `handoff` when switching sessions

For larger tooling work later:
`prototype → to-spec → to-tickets → implement → tdd/diagnosing-bugs → code-review`.

## Current state

The repository architecture and first vertical slice are already implemented and validated. Do not restart from a blank outline.

## Next bounded action

Research authoritative NVIDIA CUDA and AMD ROCm/HIP primary docs for:
- thread hierarchy
- warp / wavefront
- SM / CU
- schedulers
- latency hiding
- occupancy
- relation to registers/shared memory/LDS

Then design:
1. one L0 conceptual experiment,
2. one optional L2 real-GPU experiment,
3. a short HTML lesson connecting the execution model to later LLM kernels and performance bottlenecks.

Update `learning/CURRENT.md` and add a learning/build record when the slice is complete.

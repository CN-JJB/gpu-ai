# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main
- Working URL: https://github.com/CN-JJB/gpu-ai

## Read first

1. `MISSION.md`
2. `AGENTS.md`
3. `CONTEXT.md`
4. `COURSE-MAP.md`
5. `skills/SKILL-MAP.md`
6. `skills/WORKFLOWS.md`
7. `learning/PROFILE.md`
8. `learning/CURRENT.md`

## Requirements already frozen

Do not reopen course scope unless a contradiction is discovered.

Core ability stack:

**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Core teaching pattern:

**真实问题 → 必要原理 → 小实验 → 可玩项目 → 结果分析 → 如何选择 → 如何迁移到其他平台/硬件**

Important constraints:
- Self-study first.
- No discrete GPU required to begin.
- Linux is the main practical platform.
- GPU architecture evolution opens the course.
- NVIDIA primary, AMD systematic secondary, Apple special section, Intel lighter.
- LLM is the primary AI workload.
- Stable knowledge is separated from dynamic intelligence.
- Important experiments use reproducible Evidence.
- Mainline milestones + Challenge Labs.
- China secondhand market primary, global technical/community intelligence secondary.
- Prefer first-party/official evidence for real course claims.
- Reuse open-source implementations before building tools from scratch.

## Completed main slices

01. GPU evolution
02. GPU execution model / latency hiding
03. On-chip memory / tiling / reuse
04. Bandwidth / arithmetic intensity / Roofline
05. Local LLM VRAM capacity
06. Quantization / format / backend
07. First reproducible local LLM deployment
08. Server concurrency / continuous batching
09. Prefix / paged KV cache
10. Speculative decoding

## Active slice — 11 single-node multi-GPU / interconnect

Research and reference are already present:

- `research/gpu/0005-multi-gpu-interconnect-scaling.md`
- `reference/gpu/multi-gpu-split-interconnect.md`

Key established model:

**partition → per-GPU compute → cross-GPU movement → synchronization → scaling efficiency**

Do not reduce multi-GPU to “2× VRAM = one larger GPU” or “2 GPUs = 2× speed”.

The next production loop is:

**Lesson → L0 Experiment → real two-GPU probe → Evidence → Learning update**

Recommended remaining artifacts:

- `lessons/11-multi-gpu/01-capacity-split-interconnect.html`
- `labs/experiments/17-multi-gpu-interconnect-roof-model/`
- `labs/experiments/18-real-multi-gpu-scaling/`
- `examples/evidence/experiment-11-multi-gpu-interconnect.md`
- `intelligence/gpu/multi-gpu-topology-2026-08-26.md`
- a new learning/build record

Real multi-GPU work must record topology/P2P first, then one-GPU PP/TG baseline, then multi-GPU PP/TG. Do not fabricate hardware benchmark results.

## Matt Pocock skills

Use the repository's routing rather than applying every skill mechanically.

High-frequency:
- `teach`
- `research`

Use scaffold/problem-solution ideas for verifiable exercises where useful. Use domain-modeling only when domain language changes. Scope is frozen, so do not restart discovery/spec grilling.

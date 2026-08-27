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

## Frozen course constraints

Core ability stack:

**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Core teaching pattern:

**真实问题 → 必要原理 → 小实验 → 可玩项目 → 结果分析 → 如何选择 → 如何迁移到其他平台/硬件**

NVIDIA primary, AMD systematic secondary, Apple special section, Intel lighter.
No CPU-architecture course.
Stable architecture knowledge is separated from current software/market intelligence.
Never fabricate real benchmark numbers.

## Completed frontier

Slices 01–14 are implemented.

Most recent completed slice:

**14 — NVIDIA architecture generation spine**

```
Tesla/G80
→ Fermi
→ Kepler
→ Maxwell
→ Pascal
→ Volta
→ Turing
→ Ampere
→ Ada / Hopper
→ Blackwell
```

Key files:
- `research/gpu/0008-nvidia-architecture-generation-spine.md`
- `reference/gpu/nvidia-generation-spine.md`
- `lessons/14-nvidia-architecture/`
- `labs/experiments/23-nvidia-generation-feature-traps/`
- `labs/experiments/24-real-nvidia-capability-inventory/`
- `examples/evidence/experiment-14-nvidia-generation-spine.md`
- `intelligence/gpu/nvidia-generation-support-2026-08-27.md`

Current 2026 support boundary is dynamic intelligence:
Maxwell/Pascal/Volta are pinned to CUDA 12.x-era support; Turing+ remains on the current line at the snapshot date.

## Active next slice — AMD architecture spine

Build a systematic AMD-native lineage:

```
GCN
→ Vega
→ RDNA / CDNA split
→ RDNA2 / CDNA2
→ RDNA3 / CDNA3
→ RDNA4 / CDNA4
→ current CDNA5 frontier
```

Use AMD-native concepts:
- wavefront / Wave64 / Wave32;
- CU / WGP;
- SGPR / VGPR;
- LDS;
- cache hierarchy / Infinity Cache / HBM;
- MFMA / WMMA / matrix cores;
- Infinity Fabric / xGMI;
- HIP / ROCm gfx target;
- Radeon vs Instinct product-line split.

Do **not** translate AMD into fake NVIDIA terminology.

Production loop:

**Research → Reference → detailed Lessons → L0 lineage experiment → real ROCm/HIP inventory probe → Evidence → dynamic support intelligence → learning update**

## After AMD

Apple Silicon special section:
- unified memory;
- Metal GPU execution;
- GPU vs Neural Engine;
- memory-bandwidth/capacity implications;
- MLX / llama.cpp / Metal runtime reality.

## Matt Pocock skills

High-frequency:
- `teach`
- `research`

Use scaffold/problem-solution patterns for verifiable exercises. Do not reopen frozen scope.

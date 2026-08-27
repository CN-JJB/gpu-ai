# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main
- Working URL: https://github.com/CN-JJB/gpu-ai

## Frozen course constraints

Core ability stack:
**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Core teaching pattern:
**真实问题 → 必要原理 → 小实验 → 可玩项目 → 结果分析 → 如何选择 → 如何迁移到其他平台/硬件**

NVIDIA primary, AMD systematic secondary, Apple special section, Intel lighter.
No CPU architecture course.
Stable knowledge and dynamic support/market intelligence remain separate.
Never fabricate real benchmark results.

## Completed frontier

Slices 01–16 are implemented.

Recent architecture spine:

### NVIDIA — Slice 14
```
Tesla/G80 → Fermi → Kepler → Maxwell → Pascal
→ Volta → Turing → Ampere → Ada/Hopper → Blackwell
```

### AMD — Slice 15
```
GCN/Vega → RDNA/CDNA split
→ RDNA2/CDNA2 → RDNA3/CDNA3
→ RDNA4/CDNA4 → current CDNA5 frontier
```

### Apple — Slice 16
```
M1 unified-memory SoC
→ Metal GPU SIMD/threadgroup
→ M3 Dynamic Caching
→ M5 GPU Neural Accelerators / Metal 4 Tensor API
+ separate Neural Engine
+ MLX CPU/GPU unified-memory execution
```

Key Apple files:
- `research/gpu/0010-apple-silicon-unified-memory-metal-ane.md`
- `reference/gpu/apple-silicon-unified-memory-metal.md`
- `lessons/16-apple-silicon/`
- `labs/experiments/27-apple-unified-memory-budget-model/`
- `labs/experiments/28-real-apple-metal-mlx-inventory/`
- `intelligence/gpu/apple-silicon-metal-mlx-2026-08-27.md`

## Active next slice — Intel lighter coverage

Build:

```
Gen graphics / EU
→ Xe-LP
→ Xe-HPG / Arc Alchemist
→ XMX matrix engines
→ Xe2 / Battlemage
→ oneAPI / Level Zero / SYCL
→ local LLM backend reality
```

Keep Intel shorter than NVIDIA/AMD.

Focus on transferable questions:
- execution grouping;
- memory/cache;
- XMX matrix path;
- discrete VRAM/bandwidth;
- driver/API/runtime support;
- current llama.cpp/PyTorch/oneAPI availability.

Production loop:
**Research → Reference → 1–2 Lessons → L0 terminology trap → real inventory probe → Evidence → intelligence → learning update**

## After Intel

Converge all ecosystems into:
**cross-vendor used-GPU / local-LLM hardware decision framework**

Decision axes:
- capacity;
- bandwidth;
- compute datatype path;
- interconnect;
- software support;
- power/cooling;
- used-market risk;
- repairability;
- TCO;
- PP/TG Evidence.

## Matt Pocock skills

High-frequency:
- `teach`
- `research`

Use verifiable exercises. Do not reopen frozen scope.

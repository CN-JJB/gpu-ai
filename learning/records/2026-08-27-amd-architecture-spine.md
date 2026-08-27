# Learning / Build Record — 2026-08-27 AMD Architecture Spine

## Slice

15 — AMD architecture generations: GCN/Vega → RDNA/CDNA branches → current RDNA4/CDNA5 frontier.

## Production output

Research:
- `research/gpu/0009-amd-architecture-generation-spine.md`

Reference:
- `reference/gpu/amd-generation-spine.md`

Lessons:
- `lessons/15-amd-architecture/01-gcn-vega.html`
- `lessons/15-amd-architecture/02-rdna-rdna2.html`
- `lessons/15-amd-architecture/03-cdna-cdna2-cdna3.html`
- `lessons/15-amd-architecture/04-rdna3-rdna4-cdna4-cdna5.html`

Experiments:
- `labs/experiments/25-amd-generation-terminology-traps/`
- `labs/experiments/26-real-amd-rocm-inventory/`

Evidence/intelligence:
- `examples/evidence/experiment-15-amd-generation-spine.md`
- `intelligence/gpu/amd-rocm-generation-support-2026-08-27.md`

## Stable model

### GCN
Wave64 + CU + SGPR/VGPR + LDS.

### Vega
packed lower precision + HBM2 / broader memory hierarchy ideas.

### RDNA
Wave32 primary + Wave64 compatibility + WGP + lower-latency cache/execution organization.

### CDNA
dedicated HPC/AI branch + MFMA Matrix Core + HBM + Infinity Fabric.

### RDNA3/4
consumer graphics branch gains chiplets, dual-issue and explicit AI accelerators.

### CDNA3/4/5
compute branch gains XCD/chiplets, FP8/MX formats, ever-larger HBM/fabric systems; current CDNA5 adopts new WGP/Wave32 direction.

## L0 result

Terminology/lineage checker:

```
12/12
```

## Key teaching win

A learner can now distinguish:

```
wavefront
CU
WGP
LDS
SGPR
VGPR
MFMA
Infinity Cache
Infinity Fabric
gfx target
```

without replacing them with fake NVIDIA terminology.

## Current software finding

As of 2026-08-27:
- ROCm Core SDK 7.14 is current snapshot;
- standard Instinct table lists through CDNA4;
- Radeon support is exact SKU/gfx-target/OS specific;
- current release notes document an RDNA3/Ryzen AI LLM performance issue;
- CDNA5 hardware is already current frontier, but its standard stable SDK support must be checked separately.

## Transfer goals

Learner should explain:
1. why classic GCN wave64 and RDNA wave32 are not merely different thread counts;
2. why WGP changes the scheduling/cache grouping;
3. why Infinity Cache is not VRAM;
4. why RDNA and CDNA are branches;
5. why MFMA and Tensor Core are comparable problem classes but not interchangeable units;
6. why exact gfx target matters more than "RX 6000 / RX 7000" marketing names for software support;
7. why runtime-visible and officially-supported are different states.

## Next slice

Apple Silicon special architecture:

```
SoC
→ unified memory
→ Metal GPU
→ GPU family / SIMD-group execution
→ Neural Engine
→ AMX/CPU matrix path boundary
→ MLX / llama.cpp Metal
→ local LLM capacity/bandwidth behavior
```

Do not model Apple as a discrete GPU with VRAM connected through PCIe.

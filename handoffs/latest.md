# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Frozen constraints

Core ability stack:
**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Never fabricate benchmark, market, transaction or hardware-health data.

## Completed frontier

Slices 01–22 are implemented.

Current end-to-end chain:

```
GPU fundamentals
→ LLM memory/quant/runtime
→ serving/cache/speculation/multi-GPU
→ NVIDIA/AMD/Apple/Intel architecture
→ cross-vendor purchase decision
→ China secondhand market
→ used-GPU acceptance
→ max-buy-price/watchlist
→ controlled real optimization capstone
```

## Slice 22 — Capstone

Key files:
- `research/system/0001-capstone-measure-diagnose-optimize.md`
- `reference/system/capstone-bottleneck-decision-tree.md`
- `lessons/22-capstone/01-measure-diagnose-one-variable.html`
- `labs/experiments/39-capstone-bottleneck-diagnosis/`
- `labs/experiments/40-real-llm-capstone/`

Core loop:

```
profile
→ baseline
→ diagnose
→ ONE semantic variable
→ validate A/B
→ compare
→ explain
```

The real manifest validator checks frozen identity and rejects multi-variable experiments.

A build-time bug where command strings were counted as a second variable was fixed by separating:
- semantic `config`;
- audit-only `command_record`.

No real benchmark results are prefilled.

## Active next slice — vendor capstone runbooks

Create four practical paths:

### NVIDIA
```
nvidia-smi / compute capability
→ CUDA llama.cpp
→ PP/TG
→ memory/power telemetry
→ evidence-selected optimization
```

### AMD
```
gfx target / ROCm
→ HIP llama.cpp
→ PP/TG
→ amd-smi/RAS
→ evidence-selected optimization
```

### Apple
```
unified-memory working set
→ Metal/MLX identity
→ PP/TG
→ capacity/bandwidth interpretation
→ evidence-selected optimization
```

### Intel
```
Level Zero/SYCL/XPU
→ llama.cpp SYCL
→ PP/TG
→ dedicated/shared memory distinction
→ evidence-selected optimization
```

Reuse Experiment 40. Do not create vendor-specific fake benchmark numbers.

## Repository maintenance after runbooks

Audit:
- COURSE-MAP.md
- lessons/README.md
- labs/experiments/README.md
- resources/RESOURCES.md
- learning/CURRENT.md
- handoffs/latest.md

so recent slices are easy to navigate.

## Matt Pocock skills

High-frequency:
- `teach`
- `research`

Use verifiable exercises and explicit provenance.

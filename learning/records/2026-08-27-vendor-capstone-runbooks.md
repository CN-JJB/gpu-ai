# Learning / Build Record — 2026-08-27 Vendor Capstone Runbooks

## Slice

23 — NVIDIA CUDA / AMD ROCm-HIP / Apple Metal / Intel SYCL capstone runbooks.

## Production output

Research:
- `research/system/0002-vendor-capstone-runbooks.md`

Reference:
- `reference/system/vendor-capstone-runbooks.md`

Lessons:
- `lessons/23-vendor-capstone/01-nvidia-cuda.html`
- `lessons/23-vendor-capstone/02-amd-rocm.html`
- `lessons/23-vendor-capstone/03-apple-metal.html`
- `lessons/23-vendor-capstone/04-intel-sycl.html`

Lab:
- `labs/experiments/41-vendor-capstone-preflight/`

Evidence:
- `examples/evidence/experiment-23-vendor-capstone-runbooks.md`

## Key skill

The learner can preserve one scientific loop across four ecosystems while keeping:
- vendor device language;
- memory topology;
- support state;
- backend build;
- telemetry;

separate.

## Current upstream verification

Pinned llama.cpp build docs were checked before writing runbooks.

## Repository navigation audit

Updated:
- COURSE-MAP.md
- lessons/README.md
- labs/experiments/README.md

to expose all implemented Slices 01–23 and Experiments 01–41.

## Next missing course spine

The largest missing first-principles area is LLM model architecture itself.

Next:
```
Transformer / decoder-only execution anatomy
→ norm / residual
→ RoPE
→ MHA/MQA/GQA
→ SwiGLU/FFN
→ MoE
→ local-inference implications
```

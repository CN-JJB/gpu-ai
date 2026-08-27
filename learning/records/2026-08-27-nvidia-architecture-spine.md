# Learning / Build Record — 2026-08-27 NVIDIA Architecture Spine

## Slice

14 — NVIDIA architecture generations: Tesla/G80 → Blackwell.

## Why this slice matters

The course now has enough prior models—warp scheduling, memory hierarchy, Roofline, matrix units and FlashAttention—to explain generations causally rather than by marketing names.

## Production output

Research:
- `research/gpu/0008-nvidia-architecture-generation-spine.md`

Reference:
- `reference/gpu/nvidia-generation-spine.md`

Detailed lessons:
- `lessons/14-nvidia-architecture/01-tesla-fermi-kepler.html`
- `lessons/14-nvidia-architecture/02-maxwell-pascal.html`
- `lessons/14-nvidia-architecture/03-volta-turing.html`
- `lessons/14-nvidia-architecture/04-ampere-ada.html`
- `lessons/14-nvidia-architecture/05-hopper-blackwell.html`

Experiments:
- `labs/experiments/23-nvidia-generation-feature-traps/`
- `labs/experiments/24-real-nvidia-capability-inventory/`

Evidence/intelligence:
- `examples/evidence/experiment-14-nvidia-generation-spine.md`
- `intelligence/gpu/nvidia-generation-support-2026-08-27.md`

## Stable spine

- Tesla/G80 → unified programmable GPU / SIMT foundation.
- Fermi → compute cache hierarchy + reliability/concurrency.
- Kepler → wide SMX, TLP/ILP, warp-level communication.
- Maxwell → partitioned SMM and efficiency.
- Pascal → GP100 vs GP10x split becomes essential.
- Volta → Tensor Core + Independent Thread Scheduling.
- Turing → modern Tensor/inference + FP/INT concurrency in RTX.
- Ampere → BF16/TF32 + async data-movement pipeline.
- Ada → fourth-gen Tensor + large top-end L2 + modern RTX/media efficiency.
- Hopper → FP8 + TMA + block clusters.
- Blackwell → FP4-class + fifth-gen Tensor; datacenter/RTX branches remain distinct.

## L0 result

Feature-lineage checker:

```
10/10
```

Key pedagogical win:
the learner must reject architecture-family overgeneralization.

## Current software-longevity finding

As of 2026-08-27:
- Maxwell/Pascal/Volta: CUDA 12.x ceiling in current NVIDIA matrix; R580 last driver family;
- CUDA 13 removed offline compilation/library support;
- Turing+ remains ongoing.

Software lifespan is therefore a first-class used-GPU TCO variable.

## Transfer goals

Learner should be able to:
1. explain why Maxwell can improve efficiency despite fewer cores/SM than Kepler;
2. explain why Pascal GP100 and GP104 cannot share one AI-feature description;
3. explain why Volta changed both AI math and warp synchronization;
4. connect Ampere async copy to tiled GEMM/attention;
5. distinguish Hopper and Ada branches;
6. distinguish datacenter and RTX Blackwell;
7. use compute capability + current support docs before buying legacy hardware.

## Next recommended slice

Systematic AMD architecture mapping:

```
GCN
→ Vega
→ RDNA / CDNA split
→ RDNA2 / CDNA2
→ RDNA3 / CDNA3
→ RDNA4 / current ROCm
```

Use AMD-native concepts:
- wavefront;
- CU/WGP;
- LDS;
- scalar/vector execution;
- Infinity Cache / HBM;
- MFMA/matrix units;
- ROCm/HIP support.

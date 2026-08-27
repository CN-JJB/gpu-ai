# Learning / Build Record — 2026-08-27 Apple Silicon Slice

## Slice

16 — Apple Silicon: Unified Memory, Metal GPU, Neural Engine and MLX.

## Production output

Research:
- `research/gpu/0010-apple-silicon-unified-memory-metal-ane.md`

Reference:
- `reference/gpu/apple-silicon-unified-memory-metal.md`

Lessons:
- `lessons/16-apple-silicon/01-unified-memory-is-not-vram.html`
- `lessons/16-apple-silicon/02-metal-gpu-simd-threadgroup.html`
- `lessons/16-apple-silicon/03-m1-to-m5-gpu-ane-mlx.html`

Experiments:
- `labs/experiments/27-apple-unified-memory-budget-model/`
- `labs/experiments/28-real-apple-metal-mlx-inventory/`

Evidence/intelligence:
- `examples/evidence/experiment-16-apple-silicon.md`
- `intelligence/gpu/apple-silicon-metal-mlx-2026-08-27.md`

## Stable model

```
Apple SoC
├─ CPU
├─ Metal GPU
├─ separate Neural Engine
└─ unified memory subsystem
```

M5 adds:
```
GPU core
→ GPU Neural Accelerator
```

which remains distinct from the Neural Engine.

## Unified-memory lesson

Unified memory changes:
```
separate host RAM + dGPU VRAM
→ shared physical pool
```

It does not remove:
- OS/runtime headroom;
- work buffers;
- KV;
- synchronization;
- memory bandwidth;
- resource management.

## Metal execution model

```
grid
→ threadgroups
→ SIMD groups
```

Runtime query:
```
threadExecutionWidth
```

rather than assuming a fixed width.

Low-latency cooperative memory:
```
threadgroup memory
```

transfers the same tiling/reuse concepts learned with CUDA shared memory and AMD LDS.

## L0 result

Synthetic 32 GiB system:
- safe budget 23 GiB;
- 21 GiB runtime footprint fits with 2 GiB margin;
- same runtime does not fit full-resident in synthetic 16 GiB dGPU;
- memory traffic lowers decode roof even though capacity fits.

Pedagogical result:
```
fit != fast
```

## Real experiment path

Experiment 28 compiles a tiny Metal kernel and directly queries:
- unified-memory status;
- recommended working set;
- SIMD width;
- threadgroup limit.

It also records MLX and llama.cpp Metal identity if installed.

## Current dynamic finding

M5 introduces GPU Neural Accelerators + Metal 4 Tensor APIs.

As of this snapshot, llama.cpp has an open M5/A19 Metal-tensor issue and an open related PR.

This is preserved as dynamic evidence and deliberately excluded from the stable Lesson.

## Transfer goals

Learner should be able to:
1. explain why a large-memory Mac can fit models beyond conventional dGPU VRAM;
2. explain why installed UMA is not safe free model memory;
3. explain why TG can still be memory-bandwidth bound;
4. map SIMD group/threadgroup memory onto prior GPU execution concepts;
5. distinguish GPU vs ANE vs M5 GPU Neural Accelerator;
6. explain why MLX's unified-memory CPU/GPU model is different from CUDA host/device copying;
7. verify an actual Mac instead of assuming SIMD width or working-set budget.

## Next slice

Intel receives lighter but complete coverage:

```
Gen graphics / EU
→ Xe-LP
→ Xe-HPG / Arc Alchemist
→ Xe2 / Battlemage
→ XMX matrix engines
→ oneAPI / Level Zero / SYCL
→ current local-LLM backend reality
```

Then the architecture sections can converge into a cross-vendor used-hardware decision framework.

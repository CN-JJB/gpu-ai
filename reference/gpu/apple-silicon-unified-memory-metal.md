# Apple Silicon / Unified Memory / Metal 速查

## System model

Discrete GPU:

```
CPU RAM
→ PCIe copy
→ GPU VRAM
```

Apple Silicon:

```
CPU ─┐
GPU ─┼─→ unified memory pool
ANE ─┘
```

## Unified Memory means

- CPU and GPU can access the same physical memory pool.
- Metal reports `hasUnifiedMemory`.
- Apple Silicon defaults ordinary resources to shared storage mode.
- MLX can run CPU/GPU ops on the same arrays without explicit relocation.

## Unified Memory does NOT mean

- all installed RAM is safe model budget;
- no temporary allocations;
- no framework copies/repacking;
- no synchronization;
- infinite bandwidth;
- CPU/GPU/ANE do not contend for memory traffic.

## Capacity model

```
safe workload budget
≈ total unified memory
 - OS/apps reserve
 - safety headroom
```

```
runtime footprint
≈ weights + KV + workspace + runtime caches
```

Useful real Metal properties:

```
hasUnifiedMemory
recommendedMaxWorkingSetSize
currentAllocatedSize
```

## Decode roof

Simplified:

```
ideal TG ceiling
≈ usable memory bandwidth
 / weight bytes streamed/token
```

This is why Pro/Max/Ultra memory bandwidth matters.

## Metal execution

```
grid
→ threadgroup
→ threads
→ SIMD groups
```

Metal term:
```
threadExecutionWidth
```

= number of threads scheduled together by the compute pipeline.

Rule:

```
query at runtime
do not assume 32
```

## Threadgroup memory

Transferable model:

```
CUDA shared memory
≈ AMD LDS
≈ Metal threadgroup memory
```

Use for:
- tiling;
- reduction;
- cooperative reuse.

It is finite and can reduce occupancy.

## Divergence

SIMD-group lanes execute one instruction stream.

```
different branch paths
→ execute multiple paths
→ lower useful-lane efficiency
```

## GPU vs Neural Engine

Core ML options prove they are separate:

```
cpuOnly
cpuAndGPU
cpuAndNeuralEngine
all
```

Therefore:

```
Metal backend
!= ANE backend
```

## MLX

Current Apple-Silicon MLX:

```
unified-memory array
→ CPU stream
or
→ GPU stream
```

Current standard MLX device types on Apple Silicon:
- CPU
- GPU

Do not claim MLX automatically targets ANE.

## M-series architecture milestones

| generation | course-level lesson |
|---|---|
| M1 | SoC + Unified Memory baseline |
| M2 | evolutionary scale in GPU/memory |
| M3 | new GPU architecture + Dynamic Caching |
| M4 | stronger GPU/ANE/memory; M3-era model continues |
| M5 | GPU Neural Accelerator per core + Metal 4 Tensor APIs + 2nd-gen Dynamic Caching |

## M5 has two different "neural" ideas

```
GPU Neural Accelerator
→ part of GPU core
→ Metal 4 Tensor APIs

Neural Engine
→ separate SoC accelerator
→ Core ML / Apple frameworks
```

Do not merge them.

## Mac buyer checklist

1. exact M chip + tier?
2. unified memory capacity?
3. official memory bandwidth?
4. GPU cores?
5. Metal generation/features?
6. `recommendedMaxWorkingSetSize`?
7. runtime: llama.cpp Metal / MLX / Core ML?
8. actual execution unit: GPU vs ANE?
9. model quant?
10. PP and TG separately?
11. context/concurrency memory?
12. price / power / repairability / resale?

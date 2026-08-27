# Apple Silicon / Metal / MLX Snapshot — 2026-08-27

Purpose: dynamic software/product snapshot for Slice 16.

Stable architecture material:
- `research/gpu/0010-apple-silicon-unified-memory-metal-ane.md`
- `reference/gpu/apple-silicon-unified-memory-metal.md`
- `lessons/16-apple-silicon/`

## Current llama.cpp pin

Current upstream master snapshot used in this course:

```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Date:
```
2026-08-27
```

Current Metal/runtime behavior must be tied to an exact build.

## M-series current architecture frontier

### M1 — 2020

Apple's first Mac-designed SoC generation establishes:
- unified memory;
- integrated Apple GPU;
- separate Neural Engine.

### M2 — 2022

Apple officially documents:
- 100 GB/s unified-memory bandwidth on base M2;
- up to 24 GB unified memory;
- more GPU resources.

These exact values are product facts, not timeless architecture constants.

### M3 — 2023

Apple identifies a major new GPU architecture:
- Dynamic Caching;
- hardware ray tracing;
- mesh shading.

Dynamic Caching is the stable-relevant feature; ray/mesh features are graphics-oriented.

### M4 — 2024

Apple explicitly says the M4 GPU builds on the next-generation GPU architecture introduced with M3.

Current product material combines:
- Dynamic Caching;
- faster unified memory;
- stronger Neural Engine;
- CPU ML accelerators.

### M5 — 2025

Current Apple M5 material introduces:
- next-generation GPU;
- one Neural Accelerator in each GPU core;
- second-generation Dynamic Caching;
- Metal 4 Tensor APIs for directly programming GPU Neural Accelerators;
- separate 16-core Neural Engine;
- base M5 unified-memory bandwidth of 153 GB/s in the launch configuration.

Important:

```
GPU Neural Accelerator
!= Apple Neural Engine
```

## Current M5 Pro / M5 Max — 2026

Apple's March 2026 MacBook Pro announcement introduces:

```
Fusion Architecture
```

for M5 Pro and M5 Max.

Apple describes it as two dies connected into one SoC using high-bandwidth, low-latency advanced packaging.

Current product values:
- M5 Pro: up to 64 GB unified memory, up to 307 GB/s;
- M5 Max: up to 128 GB unified memory, up to 614 GB/s.

These are current product facts.

Do not generalize them to:
- base M5;
- every future M5-family package;
- every Apple-Silicon generation.

## Metal Unified Memory API

Current Apple Metal APIs expose:

```
MTLDevice.hasUnifiedMemory
MTLDevice.recommendedMaxWorkingSetSize
MTLDevice.currentAllocatedSize
```

Current docs define `recommendedMaxWorkingSetSize` as an approximation of how much memory the GPU can allocate without affecting runtime performance.

Current Apple-Silicon storage default:

```
MTLStorageMode.shared
```

for ordinary resources.

Current docs still require CPU/GPU synchronization for shared resources.

## Metal execution width

Current Metal API:

```
MTLComputePipelineState.threadExecutionWidth
```

Apple explicitly warns not to assume one SIMD-group width across Mac GPUs.

Experiment 28 queries it from a compiled compute pipeline.

## Current MLX

Current MLX documentation snapshot:
```
0.32.x
```

Apple-Silicon design:
- arrays live in unified memory;
- operations may run on CPU or GPU streams;
- ordinary documented Apple-Silicon device types are CPU and GPU;
- `device_info()` reports architecture/memory details.

Therefore:

```
MLX
!= automatic Neural Engine runtime
```

## Current Metal 4 Tensor APIs

Apple's current Metal performance guide says Metal 4 introduces tensor resources and Metal Performance Primitives for machine-learning kernels that can leverage GPU Neural Accelerators on M5-class hardware.

Current developer docs state:
- Apple10 GPU family and later has a neural accelerator in each core;
- tensor operations can be invoked from Metal shader/tensor APIs.

This is a GPU execution path.

It must not be merged with Core ML's Neural Engine path.

## Current llama.cpp M5 Tensor issue

As of 2026-08-27:

Issue:
```
ggml-org/llama.cpp #27473
```

Status:
```
open
label: bug-unconfirmed
```

Reported problem:
- M5/A19 Metal tensor API path can be disabled or miscompiled depending on Metal language/library build mode;
- reporter identified missing Metal 4 language selection in a source-compilation path;
- a second user reported a correctness failure with an external metallib path on M5 Max.

Related PR:
```
#27461
metal: enable Metal 4.0 tensor API on M5+/A19+
```

Current PR status at snapshot:
```
open / not merged
```

Course interpretation:

```
M5 hardware neural acceleration exists
but
current llama.cpp Metal tensor integration is an active upstream area
```

Do not state:
```
"llama.cpp on M5 cannot use Neural Accelerators forever"
```

and do not state:
```
"current master definitely uses them correctly"
```

Revalidate issue/PR/build before benchmarking.

## Current Core ML compute-unit separation

Current Apple Core ML API explicitly distinguishes:

```
cpuOnly
cpuAndGPU
cpuAndNeuralEngine
all
```

This remains strong Evidence that:
- GPU;
- Neural Engine;

are separate execution units even within one SoC.

## Support-state vocabulary for Apple AI

### Hardware available
The chip contains the feature.

### API available
Metal/Core ML exposes an API for it.

### Framework supported
MLX/Core ML/llama.cpp can dispatch relevant operations.

### Kernel active
The exact model/kernel is actually routed to that unit.

### Correct and faster
The active path passes correctness tests and improves the target workload.

Never collapse these five states into:

```
"supported"
```

## Revalidation triggers

Re-check this file when:
- a new M-series generation appears;
- Metal language/API major version changes;
- MLX changes Apple device types;
- llama.cpp #27473 / PR #27461 changes state;
- llama.cpp Metal tensor code is reworked;
- Core ML compute-unit behavior changes;
- new Pro/Max/Ultra package topologies appear.

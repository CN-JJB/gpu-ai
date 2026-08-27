# Evidence — Experiment 16: Apple Silicon / Unified Memory / Metal

状态：stable architecture research complete; L0 capacity/bandwidth model verified; real Metal/MLX inventory path ready.

## Claim

> Apple Silicon removes the discrete CPU-RAM↔GPU-VRAM physical pool boundary through unified memory, but it does not remove capacity headroom, synchronization, bandwidth limits or runtime-specific allocations. Metal GPU, GPU Neural Accelerators and Apple Neural Engine are distinct execution concepts.

## Stable official evidence

### Unified Memory

Apple M1 launch material describes:
- one high-bandwidth/low-latency memory pool;
- CPU/GPU/other SoC technologies accessing the same data;
- no requirement to copy data between separate physical pools.

Current Metal APIs expose:
```
hasUnifiedMemory
recommendedMaxWorkingSetSize
currentAllocatedSize
```

Current Apple-Silicon resources default to shared storage mode.

Current Metal docs still require correct synchronization between CPU/GPU accesses.

### Metal execution

Current Metal docs describe:
```
grid
→ threadgroups
→ SIMD groups
```

`threadExecutionWidth` is the runtime SIMD-group width.

Apple explicitly says not to assume the SIMD-group size across Mac GPUs.

### GPU vs Neural Engine

Current Core ML `MLComputeUnits` distinguishes:
- CPU;
- CPU+GPU without Neural Engine;
- CPU+Neural Engine without GPU;
- all units.

This directly validates:
```
GPU != Neural Engine
```

### MLX

Current MLX docs state:
- Apple-Silicon arrays live in unified memory;
- CPU/GPU operations can use the same arrays without explicit relocation;
- current ordinary Apple-Silicon devices are CPU and GPU.

Therefore MLX GPU execution is not Evidence of ANE use.

### M5

Apple current M5 docs state:
- neural accelerator in each GPU core;
- Metal 4 Tensor APIs can program GPU neural accelerators;
- separate Neural Engine is also present.

This validates:
```
GPU Neural Accelerator != Neural Engine
```

## L0 verification

Experiment:
`labs/experiments/27-apple-unified-memory-budget-model/`

Default synthetic input:
- 32 GiB installed unified memory;
- 6 GiB OS/apps reserve;
- 3 GiB safety headroom;
- 18 GiB weights;
- 2 GiB KV;
- 1 GiB workspace;
- 200 GiB/s synthetic memory bandwidth;
- 40 GiB/s other traffic;
- 16 GiB comparison dGPU VRAM.

Verified output:

```
safe unified workload budget = 23 GiB
runtime footprint            = 21 GiB
unified fit                  = YES
margin                       = 2 GiB
16-GiB dGPU full-resident    = NO

full bandwidth TG roof       = 11.111 tok/s
contended TG roof            = 8.889 tok/s
```

These values are synthetic and do not describe any Apple SKU.

## Real Evidence path

Experiment 28 records:
- exact Mac/chip;
- installed unified memory;
- `hasUnifiedMemory`;
- `recommendedMaxWorkingSetSize`;
- `currentAllocatedSize`;
- real Metal `threadExecutionWidth`;
- threadgroup limit;
- optional MLX device information;
- llama.cpp Metal device/build.

No real Mac benchmark numbers are prefilled.

## Dynamic 2026 upstream evidence

Current llama.cpp:
- master pin `d7a2074112d27649303fa107eb8c94db1ee435f3`;
- issue #27473 open and labeled bug-unconfirmed;
- PR #27461 open/not merged.

This is evidence of an active M5 Metal-tensor integration boundary, not a stable architecture limitation.

## Learner should reject

- "Unified memory = VRAM";
- "installed memory = safe GPU working set";
- "same memory = no synchronization";
- "unified memory = no bandwidth bottleneck";
- "Apple SIMD group = always 32";
- "Metal = Neural Engine";
- "MLX automatically uses ANE";
- "M5 GPU Neural Accelerator = Apple Neural Engine";
- "hardware tensor support proves the current LLM backend uses it";
- "one M-series name predicts LLM speed without capacity/bandwidth tier".

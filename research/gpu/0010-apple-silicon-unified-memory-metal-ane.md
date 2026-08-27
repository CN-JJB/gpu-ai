# Research Note 0010 — Apple Silicon: Unified Memory、Metal GPU、Neural Engine 与本地 LLM

日期：2026-08-27

## Research question

Apple Silicon 为什么不能用离散显卡的模型直接解释？

错误直觉通常有两种：

> “统一内存就是系统 RAM，GPU 很慢。”

或：

> “64 GB unified memory 就等于 64 GB 独显 VRAM，而且完全没有数据搬运成本。”

两种都不准确。

Apple Silicon 更合适的系统模型是：

```
one SoC
├─ CPU
├─ GPU
├─ Neural Engine
├─ media / I/O engines
└─ unified memory subsystem
```

学习目标：

1. 理解 Unified Memory 到底统一了什么；
2. 理解 Metal GPU 的 thread / threadgroup / SIMD-group；
3. 理解 threadgroup memory 与 register/cache 的位置；
4. 区分 GPU、Neural Engine、CPU compute path；
5. 理解 MLX 为什么特别适合 Apple Silicon；
6. 理解 M1→M5 哪些变化真正影响本地 LLM；
7. 学会用容量、带宽、backend，而不是“GPU core 数”，判断 Mac 的本地 LLM 价值。

---

# Part I — Unified Memory 不是“共享显存”的一句话

Primary sources:

Apple M1 launch:
https://www.apple.com/newsroom/2020/11/apple-unleashes-m1/

Metal storage modes:
https://developer.apple.com/documentation/metal/setting-resource-storage-modes

Metal device memory properties:
https://developer.apple.com/documentation/metal/mtldevice/hasunifiedmemory
https://developer.apple.com/documentation/metal/mtldevice/recommendedmaxworkingsetsize

MLX unified memory:
https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html

## What changes relative to a discrete GPU?

Typical discrete-GPU mental model:

```
CPU RAM
   │
 PCIe / interconnect copy
   ▼
GPU VRAM
```

The CPU and GPU usually have distinct physical memory pools.

Apple Silicon:

```
CPU ─┐
GPU ─┼─→ same unified physical memory pool
ANE ─┘
```

Apple's M1 launch material explicitly describes a single high-bandwidth, low-latency pool that SoC technologies can access without copying data between separate memory pools.

Metal exposes this with:

```
MTLDevice.hasUnifiedMemory == true
```

and Apple Silicon defaults resources to:

```
MTLStorageMode.shared
```

for ordinary CPU/GPU shared-access resources.

## Stable benefit

A framework can avoid the classic:

```
allocate host tensor
→ copy whole tensor to VRAM
→ maintain duplicate
```

boundary.

MLX makes this especially explicit:

```
one MLX array
→ CPU op
or
→ GPU op
```

without changing the array's memory location.

This is a real architectural advantage for:
- large models;
- mixed CPU/GPU pipelines;
- avoiding duplicate staging copies;
- fitting workloads larger than a conventional discrete GPU's VRAM pool.

## But "no copy" is not a universal law

Metal still supports:

```
MTLStorageMode.shared
MTLStorageMode.private
MTLStorageMode.memoryless
```

A framework may:
- create GPU-private resources;
- transform/repack tensors;
- create temporary buffers;
- allocate KV/workspaces;
- cache kernels/weights in optimized layouts.

So the stable statement is:

```
Unified Memory removes the requirement for
separate CPU-RAM ↔ discrete-VRAM physical pools.

It does not guarantee
every software path uses exactly one allocation with zero copying.
```

## Shared access still needs synchronization

Apple's Metal docs explicitly state that when CPU and GPU access shared resources, software still needs to ensure one participant's writes have completed before the other reads them.

So:

```
same memory
!=
same time
```

Memory dependency/order still matters.

---

# Part II — 64 GB unified memory is not "64 GB VRAM available to the model"

The memory pool is shared by:
- macOS;
- applications;
- CPU;
- GPU;
- Neural Engine/framework allocations;
- file/cache/system services;
- model weights;
- KV cache;
- runtime graph/workspaces.

Therefore:

```
usable model working set
<
installed unified memory
```

Metal exposes a useful dynamic property:

```
recommendedMaxWorkingSetSize
```

Apple defines it as an approximation of the amount of memory the GPU can allocate without hurting runtime performance.

Metal also exposes:

```
currentAllocatedSize
```

for current GPU resource allocation.

This is a better real-machine Evidence path than saying:

> “My Mac has 64 GB, therefore the GPU has 64 GB free.”

## Local LLM capacity model

A useful approximation:

```
runtime footprint
≈ weights
 + KV
 + compute/work buffers
 + runtime caches
```

and:

```
runtime footprint
must fit below a safe system working-set budget
```

The exact safe budget is dynamic and system-dependent.

---

# Part III — Unified Memory does not abolish bandwidth

If a model's decode step effectively streams a large fraction of its weights each token:

```
ideal decode ceiling
≈ usable memory bandwidth
 / weight bytes streamed per token
```

The same Roofline model still applies.

Apple changes:

```
where memory sits
and
who can access it
```

but not the physical reality that bytes must cross memory channels.

Also:

```
CPU + GPU + other engines
share the memory subsystem
```

So concurrent system activity can consume bandwidth.

Do not teach:

```
Unified Memory = infinite / free bandwidth
```

## Why Pro / Max / Ultra matter disproportionately

Within one M-series generation, variants can differ dramatically in:
- unified-memory capacity;
- memory bus width/bandwidth;
- GPU core count;
- package topology.

For memory-bound local LLM decode, memory bandwidth can matter more than a simple GPU-core-count comparison.

This is why:

```
"M3"
or
"M5"
```

is not enough information for a buying decision.

Need exact:
```
base / Pro / Max / Ultra
+ memory capacity
+ memory bandwidth
```

---

# Part IV — Metal compute execution model

Primary:
https://developer.apple.com/documentation/metal/creating-threads-and-threadgroups
https://developer.apple.com/documentation/apple-silicon/porting-your-metal-code-to-apple-silicon
https://developer.apple.com/documentation/metal/mtlcomputepipelinestate/threadexecutionwidth

## Metal hierarchy

Software:

```
grid
→ threadgroups
→ threads
```

Hardware execution:

```
threads in a threadgroup
→ SIMD groups
→ execute together
```

This is the Apple/Metal equivalent place to transfer our previous SIMT reasoning.

## SIMD group

Apple describes a SIMD group as threads that execute the same code concurrently.

Divergence problem:

```
some lanes take branch A
others take branch B
→ SIMD group may execute both paths
→ useful-lane efficiency falls
```

Same transferable principle as NVIDIA warp / AMD wavefront.

## Do NOT hardcode SIMD width

Metal provides:

```
pipelineState.threadExecutionWidth
```

Apple explicitly recommends querying the width at runtime and warns that SIMD-group size can differ between GPUs, especially Mac GPUs.

So stable course rule:

```
don't assume Apple SIMD group == 32
```

even if many Apple GPU configurations have historically used 32-wide execution.

## Threadgroup size is kernel-dependent

Metal also exposes:

```
maxTotalThreadsPerThreadgroup
```

and Apple notes it can differ between compute pipeline states on the same GPU because register/threadgroup-memory requirements change resource limits.

This is exactly the occupancy/resource-pressure model from Slice 02/03.

---

# Part V — Threadgroup memory

Metal's low-latency workgroup-local storage is:

```
threadgroup memory
```

Transferable mapping:

```
CUDA shared memory
ROCm LDS
Metal threadgroup memory
```

Same stable uses:
- tiling;
- local reduction;
- cooperative data reuse;
- avoiding repeated device-memory accesses.

Same stable costs:
- limited capacity;
- synchronization;
- bank/access-pattern effects;
- larger usage can reduce concurrently resident work.

## Registers and private thread state

Per-thread temporaries live in GPU register/private execution resources under compiler control.

As in NVIDIA/AMD:

```
too much per-thread state
→ lower concurrent occupancy / possible spill
```

Exact Apple register-file details are less publicly exposed than CUDA/ROCm, so the course should teach the transferable resource model without inventing undocumented register counts.

---

# Part VI — Apple GPU is not the Neural Engine

This distinction is critical.

Apple Silicon contains separate compute paths:

```
CPU
GPU
Neural Engine
```

Core ML makes this separation explicit through:

```
MLComputeUnits.cpuOnly
MLComputeUnits.cpuAndGPU
MLComputeUnits.cpuAndNeuralEngine
MLComputeUnits.all
```

Apple documents:
- `cpuAndGPU` excludes the Neural Engine;
- `cpuAndNeuralEngine` excludes the GPU;
- `all` may use the Neural Engine.

Therefore:

```
Metal GPU execution
!=
Neural Engine execution
```

## Why this matters for local LLM

A runtime that says:

```
Metal backend
```

is generally running GPU kernels.

It does NOT mean:
```
Apple Neural Engine is being used
```

unless the runtime/framework specifically maps supported operations to ANE/Core ML.

---

# Part VII — MLX and why Unified Memory changes framework design

Primary:
https://ml-explore.github.io/mlx/
https://ml-explore.github.io/mlx/build/html/usage/unified_memory.html

MLX is Apple ML Research's array framework designed around Apple Silicon.

Current Apple-Silicon MLX model:

```
array lives in unified memory
→ operation chooses CPU or GPU stream
→ no explicit tensor relocation required
```

This is more than a convenience API.

It changes scheduling opportunities:

```
large compute-dense op
→ GPU

tiny overhead-bound op
→ CPU
```

without a mandatory full tensor copy between two physical memory pools.

## Current MLX device path

Current docs list CPU and GPU as the supported Apple-Silicon device types for ordinary MLX execution.

Therefore stable/current lesson:

```
MLX GPU
!=
Neural Engine
```

Do not imply an MLX model automatically runs on ANE.

---

# Part VIII — M-series evolution: what actually changed?

## M1 — 2020: establish the architecture model

M1 is the foundational Mac Apple-Silicon generation.

Key stable ideas:
- SoC integration;
- Unified Memory Architecture;
- Apple GPU;
- Neural Engine;
- shared package memory subsystem.

For this course M1 matters more as:
```
the architectural baseline
```
than as a benchmark number.

## M2 — 2022: scale the same model

M2 primarily scales:
- GPU resources;
- unified-memory capacity/bandwidth;
- CPU/media capabilities.

For the architecture course:
```
M2 is evolutionary
```

not a brand-new GPU programming model.

## M3 — 2023: major GPU architecture change

Apple describes the M3 family as introducing a new GPU architecture.

The important new idea:

```
Dynamic Caching
```

Apple says local memory allocation is assigned dynamically in hardware based on actual workload needs.

Conceptual connection:

```
fixed / overprovisioned local-resource allocation
→ hardware-adaptive allocation
→ better average GPU utilization
```

M3 also adds:
- hardware ray tracing;
- mesh shading.

For pure LLM:
- Dynamic Caching is the transferable GPU-resource idea;
- ray tracing / mesh shading are mostly graphics features.

Do not claim ray-tracing blocks speed up llama.cpp.

## M4 — 2024: stronger AI/memory system, same broad GPU programming model

M4 improves:
- GPU;
- unified-memory bandwidth/capacity in product families;
- Neural Engine;
- CPU ML acceleration.

It continues the M3-era GPU feature direction rather than introducing a new CUDA-like programming hierarchy.

## M5 — 2025: AI hardware moves inside every GPU core

Apple's M5 launch introduces a major new distinction:

```
M5 GPU core
→ dedicated Neural Accelerator
```

Apple explicitly says developers can program these GPU Neural Accelerators through:

```
Metal 4 Tensor APIs
```

M5 also has:
- a separate 16-core Neural Engine;
- second-generation Dynamic Caching;
- next-generation GPU architecture.

This produces three distinct AI execution concepts:

```
CPU path
GPU shader / tensor path
separate Neural Engine
```

## M5 GPU Neural Accelerator is NOT the Neural Engine

Very important:

```
GPU Neural Accelerator
inside GPU core
```

and:

```
Apple Neural Engine
separate SoC accelerator
```

are different hardware blocks.

The former is accessible through current Metal 4 Tensor APIs on supported hardware.

---

# Part IX — M5-era Tensor API shows why backend support matters

Hardware may expose:

```
native neural/matrix acceleration
```

but an application only benefits if:

```
framework/backend
→ compiles correct Metal version
→ emits compatible tensor operations
→ validates correctness
→ dispatches to that path
```

This is the Apple version of Slice 13's rule:

```
hardware datatype / accelerator
!=
model automatically uses accelerator
```

Current llama.cpp status belongs in dynamic intelligence, not this stable research note.

---

# Part X — Apple vs discrete multi-GPU model

Do NOT apply Slice 11 literally:

```
GPU0 VRAM
↔ PCIe / P2P
↔ GPU1 VRAM
```

Apple Silicon normally looks more like:

```
CPU
GPU
ANE
other engines
  ↓
shared SoC fabric/cache/memory controllers
  ↓
unified memory
```

Transferable questions remain:
- capacity;
- bandwidth;
- concurrency;
- data movement;
- compute utilization;
- runtime support.

But the boundary is not a PCIe VRAM-copy boundary.

---

# Part XI — Local LLM performance model on Apple Silicon

## Capacity

```
fit?
≈ installed unified memory
 - OS/apps
 - runtime/KV/workspace
 - safety headroom
```

## Decode

Often:

```
memory-bandwidth limited
```

so a useful first roof is:

```
tok/s upper bound
≈ usable memory bandwidth
 / streamed weight bytes per token
```

## Prefill

Prefill tends to use larger matrix operations, so:
- GPU compute;
- matrix/tensor acceleration;
- Metal kernel quality;
- M5 GPU Neural Accelerator availability;

can matter more strongly.

Therefore:

```
Mac PP ranking
!=
Mac TG ranking
```

## Context / concurrency

KV cache consumes the same unified pool.

So:

```
long context
+ multiple slots
→ shared memory pressure
→ less room for weights / system
```

Unified memory does not remove the KV budget model.

---

# Part XII — What to record when comparing Macs

Never record only:

```
"M3 Max"
```

Record:
- exact chip;
- GPU core configuration;
- installed unified memory;
- memory bandwidth from official product docs;
- macOS version;
- Metal device name;
- `recommendedMaxWorkingSetSize`;
- runtime/build;
- model/quant;
- context;
- PP/TG;
- power/thermal mode.

For current M5 Pro/Max/Ultra-style systems, package topology may also differ; current exact details belong in intelligence.

---

# Stable claims to avoid

- "Unified memory is just slow system RAM."
- "64 GB unified memory = 64 GB free VRAM."
- "Apple Silicon never copies data."
- "CPU and GPU sharing memory means synchronization disappears."
- "Unified memory removes the memory-bandwidth bottleneck."
- "Apple SIMD group is always 32."
- "Metal GPU = Neural Engine."
- "MLX automatically uses the Neural Engine."
- "M3 Dynamic Caching is extra model memory."
- "M5 Neural Accelerators are the Apple Neural Engine."
- "M5 hardware Tensor API means every current LLM runtime already uses it."
- "GPU core count alone predicts Apple local-LLM speed."

# Research Note 0009 — AMD Architecture Spine: GCN → RDNA/CDNA → RDNA4/CDNA5

日期：2026-08-27

## Research question

AMD GPU 架构为什么不能被简单翻译成：

```
"AMD 版 CUDA Core / Tensor Core"
```

本课程用 AMD 自己的语言建立主线：

```
GCN wave64 / CU
→ Vega
→ RDNA wave32 / WGP
→ Radeon graphics/latency branch

and

GCN/Vega compute ancestry
→ CDNA
→ MFMA / Matrix Core
→ HBM / Infinity Fabric
→ Instinct AI/HPC branch
```

核心目标是让学习者能回答：

1. Wave64 为什么会变成 RDNA 的 Wave32 主路径？
2. CU 和 WGP 是什么关系？
3. LDS、SGPR、VGPR 在 AMD 上怎么对应之前学过的寄存器/shared-memory模型？
4. RDNA 为什么适合低延迟图形/消费 compute，而 CDNA 为什么更适合大吞吐 AI/HPC？
5. AMD Matrix Core / MFMA 和 NVIDIA Tensor Core 有什么相同问题、不同命名？
6. Infinity Cache、HBM、Infinity Fabric/xGMI 分别解决哪一层数据移动？
7. 为什么 Radeon 架构“很新”仍不自动等于 ROCm/LLM 生态最好？

## Primary sources

### AMD ROCm GPU architecture documentation

Current ROCm architecture index:
https://rocm.docs.amd.com/en/latest/reference/gpu-arch/index.html

It collects official docs for:
- CDNA;
- CDNA2;
- CDNA3;
- CDNA4;
- RDNA;
- RDNA2;
- RDNA3;
- RDNA4;
- older Vega/GCN.

This is the canonical navigation anchor for architecture research.

### HIP hardware implementation

https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html

Current official model distinguishes:
- vector ALUs;
- scalar ALUs;
- LDS;
- wavefront scheduling;
- MFMA matrix cores;
- RDNA Wave32/WGP;
- CDNA compute-first design.

### GPUOpen GCN articles

Official AMD GPUOpen material describes classic GCN CU:
- 4 SIMD units;
- wave64;
- 16-wide SIMD executing a 64-lane wave over 4 cycles;
- SGPR/VGPR split;
- 64 KiB LDS per CU in documented GCN examples;
- latency hiding via multiple resident waves.

### RDNA ISA / architecture guide

Official RDNA ISA states:
- supports Wave32 and Wave64;
- Wave32 is a fundamental new mode;
- WGP replaces CU as the basic grouping for compute scheduling/resource aggregation.

### Current CDNA architecture page

https://www.amd.com/en/technologies/cdna.html

Current AMD CDNA family page spans:
- CDNA / MI100;
- CDNA2 / MI200;
- CDNA3 / MI300;
- CDNA4 / MI350;
- current CDNA5 / MI400 frontier.

---

# Part I — GCN: wave64 + scalar/vector split + explicit LDS

## The GCN compute unit

Classic GCN mental model:

```
Compute Unit
├─ scalar path / SGPR
├─ SIMD0 + VGPR
├─ SIMD1 + VGPR
├─ SIMD2 + VGPR
├─ SIMD3 + VGPR
└─ LDS
```

A wavefront contains 64 work-items.

Classic hardware uses 16-wide SIMD:
```
wave64
→ 16 lanes per cycle
→ 4 cycles for one vector instruction
```

This is a major difference from NVIDIA's common "warp32" mental model.

## Why scalar + vector split matters

Some values are identical for the whole wave:
- loop counters;
- uniform pointers;
- constants;
- branch conditions that are wave-uniform.

GCN can keep such values in:
```
SGPR
→ scalar ALU
```

while per-lane values live in:
```
VGPR
→ vector ALU
```

Stable lesson:

```
don't waste 64 vector copies
when one wave-uniform scalar value is enough
```

This is one reason AMD terminology must be learned on its own.

## LDS

Local Data Share is AMD's low-latency on-CU scratchpad used for workgroup communication.

Transferable mapping:

```
NVIDIA shared memory
≈
AMD LDS
```

but exact size/banks/ports differ by architecture.

## Latency hiding

GCN also swaps among resident waves when one waits on memory.

Same stable principle:

```
more independent waves
→ more opportunities to hide memory latency
```

but resource limits come from:
- VGPR;
- SGPR;
- LDS;
- workgroup/block resources.

---

# Part II — Vega: push GCN toward flexible data types and high-bandwidth memory

Vega remains in the GCN family lineage but adds several important ideas.

Official AMD launch material highlights:
- Rapid Packed Math;
- High Bandwidth Cache Controller;
- HBM2 on Radeon RX Vega products;
- next-generation compute units.

## Rapid Packed Math

The key idea:

```
one 32-bit datapath slot
→ can process packed lower-precision values
```

For compatible operations, FP16/INT16-style packed math can increase throughput.

Stable lesson:

```
lower precision becomes a hardware throughput strategy
before modern dedicated matrix units dominate
```

## HBM2 / High Bandwidth Cache Controller

Vega aggressively explores:
- high-bandwidth HBM2;
- larger virtual-address/memory-management ideas;
- treating external memory/storage as a broader hierarchy.

For local LLM history this matters because AMD already had products where:
```
memory bandwidth + capacity architecture
```
was as important as arithmetic.

## Why Vega matters to the fork point

Vega-style GCN is near the point where AMD's GPU roadmap splits:

```
graphics / low-latency
→ RDNA

compute / HPC / AI
→ CDNA
```

Do not treat RDNA and CDNA as simple sequential generations of one line.

---

# Part III — RDNA: Wave32 and WGP reorganize the graphics/latency branch

Official RDNA architecture/ISA says RDNA makes a fundamental change to execution.

## Wave32

GCN:
```
wave64
```

RDNA:
```
wave32 primary
+ wave64 compatibility
```

Why Wave32 helps:
- lower wave lifetime;
- quicker ramp after barriers;
- less wasted work when only part of a 64-lane wave is active;
- reduced pressure for some per-wave resources;
- better fit to latency-oriented graphics workloads.

Important:

```
Wave32 does not mean "AMD copied NVIDIA warp32"
```

The surrounding scheduler/register/cache architecture is AMD-specific.

## 32-wide SIMD

RDNA combines work differently so a Wave32 can issue across a 32-wide vector datapath in one cycle rather than classic GCN's 16-wide × 4-cycle pattern.

## WGP — Work Group Processor

RDNA groups two closely coupled CUs under a WGP.

Mental model:

```
WGP
├─ CU0
├─ CU1
├─ shared higher-level resources
└─ WGP-level scheduling/cache organization
```

The WGP becomes a more important unit for workgroup scheduling/resource aggregation.

## Cache hierarchy change

Official HIP docs describe RDNA-style hierarchy:

```
per-CU L0
→ WGP-shared L1
→ global L2
```

This adds an intermediate cache level compared with GCN naming.

## Stable consequence

RDNA is not:
```
"GCN but faster"
```

It is a latency/efficiency-oriented execution reorganization:
- Wave32;
- WGP;
- new cache hierarchy;
- lower vector instruction latency.

---

# Part IV — RDNA2: Infinity Cache enters the consumer GPU memory story

AMD RDNA family page identifies RDNA2 as the first RDNA generation with Infinity Cache and first-generation ray accelerators.

## Infinity Cache

Basic goal:

```
large on-die cache
→ catch reusable memory traffic
→ reduce pressure on external GDDR
```

This is conceptually similar to the large-last-level-cache trend seen in later NVIDIA consumer architectures.

For local LLM:

```
Infinity Cache
!= extra VRAM
```

Large model weights can far exceed cache capacity.

It can help when data has reuse/locality, but decode weight streaming may still be bounded by external memory traffic.

## RDNA2 and compute

RDNA2 remains a graphics-first architecture.
ROCm support therefore depends heavily on:
- exact Radeon SKU;
- gfx target;
- current official matrix.

Architecture capability alone does not promise library support.

---

# Part V — CDNA: AMD formally separates compute/HPC from Radeon graphics

AMD CDNA whitepaper describes CDNA as a dedicated compute architecture for HPC/ML.

MI100 (CDNA / gfx908) introduces:
- Matrix Core Technology;
- HBM2;
- Infinity Fabric links;
- compute-focused Instinct product design.

## Matrix Core / MFMA

Current HIP docs call AMD matrix acceleration:

```
MFMA = Matrix Fused Multiply-Add
```

These units operate on matrix tiles and execute separately from ordinary VALU work.

Transferable comparison:

```
NVIDIA Tensor Core
and
AMD MFMA Matrix Core
```

solve similar classes of matrix throughput problems.

But:
- instruction shapes differ;
- data types differ;
- register organization differs;
- software libraries differ.

Never count them as if they were interchangeable unit counts.

## AGPR / accumulator resources

CDNA generations use specialized accumulation resources for matrix operations in documented implementations.

Again reinforces:

```
matrix input registers
!= accumulator storage
```

---

# Part VI — CDNA2: FP64 matrix compute + multi-die scale-up

CDNA2 powers MI200.

Official whitepaper highlights:
- matrix FP64 support;
- stronger BF16/FP16;
- multi-die packaging;
- Infinity Fabric communication;
- HBM2e.

## Why FP64 matrix hardware matters

CDNA2 isn't only an "AI lower precision" generation.

HPC needs:
```
high-accuracy FP64 GEMM
```

CDNA2 adds matrix instructions specifically for FP64.

This distinguishes the datacenter compute branch from gaming RDNA priorities.

## Multi-die

MI250-class products scale compute/memory across multiple GPU dies connected by high-bandwidth fabric.

This connects to Slice 11:

```
more dies / GPUs
→ more capacity/compute
→ communication becomes architecture
```

---

# Part VII — RDNA3: chiplets + dual-issue + explicit AI acceleration

Official AMD launch material identifies:
- Graphics Compute Die (GCD);
- Memory Cache Dies (MCDs);
- second-generation Infinity Cache;
- dedicated AI acceleration;
- second-generation ray tracing.

## Chiplet graphics GPU

RDNA3 separates:

```
GCD:
compute / core GPU logic

MCD:
memory controllers + cache
```

connected by Infinity Links/package fabric.

Stable lesson:

```
chiplet GPU architecture
moves some memory/cache functions off the main compute die
```

## Dual-issue VALU

RDNA3 ISA documents VOPD:
- one instruction encoding can represent two independent VALU operations;
- both can execute in parallel;
- Wave32 only;
- strict operand/register constraints.

This means advertised dual-issue potential is conditional:

```
independent instructions
+ legal register-bank pattern
+ compiler finds pairing
→ higher vector throughput
```

Not every workload gets 2×.

## AI accelerators

AMD identifies RDNA3 as the first RDNA generation with dedicated AI accelerators.

Still:
```
RDNA3 AI accelerator
!= CDNA3 Instinct Matrix Core system
```

The product goals and software stack differ.

---

# Part VIII — CDNA3: XCD chiplets + HBM3 + FP8 + heterogeneous unification

CDNA3 powers MI300.

Official whitepaper/microarchitecture introduces:

```
XCD = Accelerated Compute Die
```

MI300 systems integrate:
- multiple XCDs;
- I/O dies;
- HBM3;
- Infinity Fabric.

## MI300A vs MI300X

Again, exact product matters.

MI300A:
```
Zen 4 CPU chiplets
+ CDNA3 XCD
+ shared HBM
+ cache coherency
```

MI300X:
```
GPU-focused XCD composition
+ very large HBM capacity
```

So:
```
CDNA3 family
!= one package topology
```

## Matrix types

CDNA3 adds current AI-relevant formats:
- FP8;
- TF32;
- sparse support;
- existing FP16/BF16/INT8/FP32/FP64 families.

## Infinity Cache / memory system

MI300 repartitions memory/cache into I/O dies and uses large shared Infinity Cache plus HBM3.

Stable lesson:

```
large AI accelerator
= compute chiplets
+ cache
+ HBM
+ package fabric
```

not "one giant monolithic CU array".

---

# Part IX — RDNA4: Radeon AI becomes more explicit

RDNA4 powers Radeon RX 9000 generation.

Current official AMD page says:
- second-generation AI accelerators;
- FP8/INT4 support;
- improved on-chip scheduling;
- third-generation Infinity Cache;
- third-generation ray tracing.

Official 2025 launch material also describes FP8 WMMA use for FSR4.

## Why this matters for local AI

RDNA4 is the strongest evidence that AMD's consumer graphics line is increasingly AI-aware.

But this does NOT imply:
```
Radeon AI accelerator features
→ all ROCm/LLM kernels automatically use them
```

Kernel/library support remains software-dependent.

## Wave32 / Wave64 remains explicit

RDNA4 ISA documents support for both Wave32 and Wave64.

Wave64 can require issuing vector/memory work in halves in documented behavior.

This is a useful reminder:

```
wave size is a compile/runtime execution choice
with real throughput/resource consequences
```

---

# Part X — CDNA4 and current CDNA5 frontier

## CDNA4

Current AMD CDNA page identifies CDNA4 as MI350 architecture:
- HBM3E;
- Matrix Core;
- MXFP4/MXFP6/MXFP8;
- sparse low-precision support;
- compute-first Instinct design.

Current ROCm 7.14 official support matrix lists CDNA4 / gfx950.

## CDNA5 — current 2026 frontier

As of 2026-08-27, AMD has introduced CDNA5 for MI400 Series.

Current AMD architecture page describes:
- new WGP architecture;
- Wave32 execution;
- MXFP8/MXFP6/MXFP4;
- HBM4;
- large rackscale fabric focus.

This is a major conceptual convergence:

Classic CDNA:
```
wave64 compute branch
```

Current CDNA5:
```
new WGP + Wave32
```

showing that wave-size/WGP ideas are no longer confined to Radeon-style RDNA.

## Dynamic support caution

Current ROCm 7.14 support matrix captured in this course lists through CDNA4 in its standard supported Instinct table.

Therefore:
```
latest hardware architecture
!= automatically present in every current stable ROCm distribution matrix
```

CDNA5 product-specific software support must be revalidated when used.

---

# Cross-generation synthesis

## 1. Execution lineage

```
GCN:
wave64 + CU + 16-wide SIMD×4-cycle

RDNA:
Wave32 primary + WGP + 32-wide issue

CDNA:
compute-focused CU + MFMA

current CDNA5:
new WGP + Wave32 compute architecture
```

## 2. Register model

AMD makes the scalar/vector distinction explicit:

```
SGPR
→ wave-uniform data

VGPR
→ per-lane data

AGPR / matrix accumulator resources
→ matrix accumulation on relevant CDNA designs
```

## 3. On-chip scratchpad

```
LDS
```

is the stable AMD term for low-latency workgroup-shared storage.

Same reasoning as Slice 03:
- bank conflicts;
- tiling;
- reuse;
- occupancy/resource pressure.

## 4. Consumer memory direction

```
GDDR
+ larger Infinity Cache
```

tries to reduce external-memory traffic through locality.

## 5. Datacenter memory direction

```
HBM
+ Infinity Fabric/xGMI
+ package chiplets
```

raises raw bandwidth/capacity and scale-up connectivity.

## 6. AI math direction

```
Vega:
packed lower precision

CDNA:
MFMA / Matrix Core

RDNA3:
dedicated AI accelerators

RDNA4:
2nd-gen AI accelerators + FP8/INT4

CDNA3/4/5:
FP8/MX formats + HPC/AI matrix specialization
```

## 7. Software is the biggest practical differentiator

Unlike simply reading architecture papers, local LLM buying requires:

```
exact gfx target
+ official ROCm support
+ HIP runtime
+ library/kernel support
+ llama.cpp / PyTorch behavior
```

A Radeon card can be architecturally modern but absent from the current official ROCm list.

That is not a contradiction:
- hardware architecture;
- software product support;

are separate layers.

---

# Claims to avoid

- "AMD wavefront is always 64."
- "RDNA uses only Wave32."
- "WGP is just AMD's name for NVIDIA SM."
- "LDS is literally identical to CUDA shared memory."
- "All RDNA GPUs have the same ROCm support."
- "Infinity Cache is extra VRAM."
- "RDNA3 dual-issue means every FP32 shader is 2×."
- "RDNA AI accelerator = Instinct MFMA Matrix Core."
- "CDNA is simply RDNA without graphics."
- "MI300A and MI300X are the same package."
- "RDNA4 FP8/INT4 support means every quantized LLM uses those units."
- "CDNA5 hardware announcement means every stable ROCm release already supports it."

## Dynamic support

See:
`intelligence/gpu/amd-rocm-generation-support-2026-08-27.md`

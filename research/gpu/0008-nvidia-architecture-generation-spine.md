# Research Note 0008 — NVIDIA Architecture Generation Spine: Tesla → Blackwell

日期：2026-08-27

## Research question

如果不背“GTX/RTX 型号表”，NVIDIA 从 Tesla/G80 到 Blackwell 到底发生了什么？

本课程采用一条因果主线：

```
前一代的瓶颈 / 新 workload
→ SM / scheduler 改造
→ memory hierarchy / data movement 改造
→ new arithmetic / matrix hardware
→ CUDA programming consequences
→ AI / local LLM consequences
```

目标不是把每代芯片都当成“更多 CUDA Core + 更高频率”，而是识别 GPU 的几个长期演进方向：

1. fixed graphics hardware → unified programmable compute；
2. 单纯堆并行度 → 更有效率的 SM partition / scheduler；
3. explicit memory movement → cache hierarchy + managed memory + async pipelines；
4. scalar/vector FMA → specialized matrix units；
5. FP32/FP16 → BF16/TF32/FP8/FP4 等 workload-specific precision；
6. 单个 thread block locality → warp specialization / cluster / hardware data movers；
7. graphics-only optimization → graphics + HPC + AI 分支并行演化。

## Official architecture chronology

NVIDIA current architecture timeline lists:

- Tesla — 2006
- Fermi — 2010
- Kepler — 2012
- Maxwell — 2014
- Pascal — 2016
- Volta — 2017
- Turing — 2018
- Ampere — 2020
- Hopper — March 2022
- Ada Lovelace — September 2022
- Blackwell — March 2024

Source:
https://www.nvidia.com/en-us/technologies/

Important:

```
architecture name
!= one exact chip
!= one exact product line
```

Especially Pascal/Ampere/Blackwell have major datacenter-vs-consumer variants.

---

# Part I — Tesla / G80 era: make the GPU a programmable parallel machine

Primary:
- NVIDIA Research, *NVIDIA Tesla: A Unified Graphics and Computing Architecture*
  https://research.nvidia.com/publication/2008-04_nvidia-tesla-unified-graphics-and-computing-architecture
- Fermi whitepaper historical introduction
  https://www.nvidia.com/content/PDF/fermi_white_papers/NVIDIA_Fermi_Compute_architecture_Whitepaper.pdf

## Problem before Tesla

Earlier graphics processors had separate specialized pipelines:

```
vertex work
→ vertex pipeline

pixel work
→ pixel pipeline
```

If workload balance changed, idle units could not simply become another type of shader processor.

## Tesla/G80 breakthrough

The architectural shift:

```
different shader workloads
→ unified programmable processor pool
```

and a general parallel programming model emerges around:
- many lightweight threads；
- warps；
- Streaming Multiprocessors；
- SIMT；
- shared memory；
- thread barriers。

The NVIDIA Research paper describes Tesla as:
- massively multithreaded；
- scalable；
- programmable in C or graphics APIs。

This is the architecture foundation that makes CUDA practical.

### Stable consequence

GPU becomes:

```
not just graphics fixed-function hardware
but
a programmable throughput processor
```

### Local-LLM relevance today

Almost none as deployable hardware.

Its importance is conceptual:
- unified compute；
- SIMT；
- warp scheduling；
- explicit fast on-chip memory。

Those concepts still survive in modern CUDA kernels.

---

# Part II — Fermi: design a GPU explicitly for general-purpose computing

Primary:
- NVIDIA Fermi Compute Architecture whitepaper
- CUDA Toolkit 3.0 historical release notes

## Problem inherited from G80 / GT200

Early CUDA GPUs proved GPGPU worked, but compute workloads exposed weaknesses:
- weak cache hierarchy；
- expensive irregular/global-memory access；
- need for stronger FP64 / IEEE behavior；
- reliability requirements for HPC；
- more complex concurrent workloads。

## Major Fermi changes

### 1. Cache hierarchy becomes a first-class compute feature

Fermi introduced:
- configurable L1/shared on-chip storage；
- unified L2 servicing loads/stores/textures。

The whitepaper describes a 768 KB unified L2 on the flagship design.

Stable lesson:

```
programmer-managed shared memory
+
hardware cache hierarchy
```

become complementary tools.

### 2. Stronger numerical / HPC semantics

Fermi improves:
- IEEE 754-2008 behavior；
- FMA；
- double precision；
- 64-bit addressing。

### 3. Reliability / datacenter features

CUDA 3.0 release highlights include:
- ECC reporting；
- concurrent kernel execution；
- multiple copy engines；
- hardware debugging/profiling support。

### 4. More sophisticated SM

Fermi SM increases CUDA-core count and strengthens scheduling/execution relative to GT200.

## Stable consequence

Fermi is the point where GPU compute stops looking like:

```
"graphics hardware that happens to run C"
```

and starts looking like:

```
"a general accelerated-computing processor with caches,
reliability, concurrency and a mature toolchain"
```

---

# Part III — Kepler: scale parallelism, then expose more concurrency

Primary:
https://docs.nvidia.com/cuda/kepler-tuning-guide/

## Main problem

Fermi made CUDA more capable, but throughput scaling required:
- more work per SM；
- more simultaneous work；
- lower control/power overhead。

## SMX

Kepler replaces Fermi SM with larger SMX.

Official tuning guide emphasizes:
- significantly more CUDA cores per SMX；
- more parallelism needed per multiprocessor；
- balance of thread-level parallelism (TLP) and instruction-level parallelism (ILP)。

This is a key lesson:

```
more execution width
→ software must expose enough independent work
```

### Four warp schedulers

Kepler SMX uses four warp schedulers.

The guide notes peak SP throughput needs a combination of TLP and ILP because schedulers issue independent instructions from multiple warps.

### More blocks per multiprocessor

Maximum resident blocks rose from 8 to 16.

### Warp shuffle

Kepler introduced warp shuffle, allowing lanes to exchange register values without always round-tripping through shared memory.

This is an important ancestry of modern warp-level kernel design.

### Hyper-Q — GK110-specific

Hyper-Q increases independent hardware work queues/connections, reducing artificial serialization between independent CUDA streams/processes.

### Dynamic Parallelism — GK110-specific

GPU kernels can launch more GPU work.

Stable lesson:

```
GPU can become a more autonomous scheduler of nested work
```

but this did not become the universal answer for high-performance kernels; launch overhead and workload structure still matter.

## Critical caveat: Kepler is not one uniform feature set

GK104 and GK110 differ.

Do not teach:
```
"Kepler supports X"
```
without checking whether X is GK110-specific.

---

# Part IV — Maxwell: efficiency through SM partitioning

Primary:
https://docs.nvidia.com/cuda/maxwell-tuning-guide/

## Problem

Kepler SMX was very wide and demanded substantial parallelism / scheduling complexity.

Maxwell focuses on:

```
do similar useful work
with simpler / more deterministic internal partitioning
and better perf-per-area / perf-per-watt
```

## SMM restructure

Official tuning guide:
- four warp schedulers remain；
- each scheduler gets dedicated functional units；
- CUDA core count per partition becomes a power-of-two aligned with warp width；
- arithmetic latency reduced；
- single-issue can fully use CUDA cores in common cases。

This is not merely “fewer cores per SM”.

The deeper shift:

```
shared wide execution resources
→ scheduler-owned partitions
```

which reduces scheduling complexity/stalls.

## Shared memory / cache change

Fermi/Kepler:
```
same physical pool split between L1 and shared
```

Maxwell:
```
dedicated shared memory
+
unified L1/texture functionality
```

GM107 provides 64 KB shared per SMM; GM204 increases it further.

## More resident blocks

Maxwell doubles max active thread blocks per SM from 16 to 32, helping small-block kernels.

## Native shared-memory atomics

Maxwell adds native shared-memory integer atomics, useful for histograms and contention-heavy local reductions.

## Stable consequence

Maxwell teaches an essential architecture lesson:

```
a more efficient SM
can beat a wider but harder-to-schedule SM
without needing a simple "core count" story
```

This is directly relevant to why cross-generation CUDA-core counts cannot be compared mechanically.

---

# Part V — Pascal: one architecture name, two very different compute priorities

Primary:
https://docs.nvidia.com/cuda/pascal-tuning-guide/

Official guide explicitly says Pascal includes major variants such as GP100 and GP104.

## Why this matters

Pascal is where the course must stop treating an architecture family as one homogeneous chip.

### GP100 — HPC / training direction

Important features:
- HBM2；
- NVLink；
- strong FP64；
- high-throughput native FP16 `half2`；
- improved Unified Memory with page faults / migration；
- compute preemption。

GP100 SM has 64 FP32 cores, fewer than Maxwell SMM, but with more SMs and more resources per core.

That continues the “smaller, better-partitioned SM” trend.

### GP10x / GP104 — graphics / inference direction

Official Pascal guide states:
- GP104 FP16 throughput is much lower than GP100；
- GP104 adds high-throughput INT8 dot-product instructions such as DP4A。

So:

```
same Pascal family
→ very different low-precision strengths
```

## Unified Memory maturation

Pascal adds hardware page faulting and larger virtual addressing.

Managed memory moves from:
```
mostly runtime-managed placement
```
toward:
```
fault + migrate/map on demand
```

This is foundational for later heterogeneous memory systems, though performance still depends on access locality and migration behavior.

## NVLink

GP100 introduces NVLink into NVIDIA compute systems as a high-bandwidth path beyond PCIe for supported platforms.

This connects directly to Slice 11.

## Stable consequence

Pascal teaches:

```
architecture family
!= product capability
```

A used-card buyer must inspect the exact die/SKU, not only “Pascal”.

---

# Part VI — Volta: AI becomes a first-class hardware workload

Primary:
https://docs.nvidia.com/cuda/volta-tuning-guide/

## 1. Tensor Cores arrive

Volta GV100 adds first-generation Tensor Cores.

Instead of only:
```
scalar/vector FMA
```

the SM now includes:
```
warp-level matrix multiply-accumulate hardware
```

This is the architectural break that leads to modern AI throughput marketing.

## 2. Dedicated FP32 + INT32 paths

GV100 SM includes both FP32 and INT32 execution resources, enabling useful address/integer work to overlap with floating-point work.

## 3. Independent Thread Scheduling

This is one of the most important CUDA semantic changes.

Before Volta, programmers often relied on implicit warp lockstep behavior.

Volta makes thread scheduling inside a warp more independent.

Old unsafe assumption:
```
"threads in one warp are always implicitly synchronized"
```

New requirement:
- use `*_sync` warp intrinsics；
- use `__syncwarp()` when sharing data through memory；
- make synchronization intent explicit。

This improves flexibility but breaks old warp-synchronous tricks that relied on undocumented lockstep assumptions.

## 4. Unified L1 / texture / shared backing

Volta provides a combined 128 KB data-cache structure with configurable shared-memory carveout.

This brings large on-chip storage closer to the execution units and lowers some spill/global access costs.

## Stable consequence

Volta is not only:
```
"the first Tensor Core GPU"
```

It is also:
```
a modernized execution/synchronization model
+
a reorganized on-chip memory hierarchy
```

---

# Part VII — Turing: bring the modern AI/SM model into RTX / inference

Primary:
https://docs.nvidia.com/cuda/turing-tuning-guide/
https://developer.nvidia.com/blog/nvidia-turing-architecture-in-depth/

## Turing's role

Volta was primarily an HPC/AI datacenter design.

Turing brings many modern ideas into RTX/workstation/GeForce-class products:
- Independent Thread Scheduling；
- Tensor Cores；
- dedicated INT32 alongside FP32；
- unified L1/shared organization。

## Concurrent FP32 + INT32

Turing SM has dedicated FP32 and INT32 cores.

Why it matters:
- pointer/address calculations are integer work；
- floating-point pipelines do not need to stop every time address math runs。

This is useful beyond graphics.

## Second-generation Tensor Core era

Turing expands Tensor Core data types:
- FP16；
- INT8；
- INT4；
- binary modes in the documented MMA evolution。

This makes it especially important historically for inference.

## RT Core

Turing also adds dedicated ray-tracing hardware.

For this course, RT Core is secondary, but it marks the beginning of a broader pattern:

```
GPU
= programmable SM
+ specialized accelerator blocks
```

The same architectural philosophy later expands for AI/data movement.

## Unified L1/shared

Turing has 96 KB unified L1/shared resource per SM with configurable carveout.

## Stable consequence

Turing is the practical bridge between:
```
datacenter AI hardware
and
mainstream RTX compute
```

For modern local AI, it is also the oldest NVIDIA generation that remains on the current CUDA support line as of 2026 — but that support fact belongs in dynamic intelligence.

---

# Part VIII — Ampere: async pipelines and precision become central

Primary:
https://docs.nvidia.com/cuda/ampere-tuning-guide/

Again, distinguish:
- GA100 / compute capability 8.0；
- GA10x / compute capability 8.6 consumer/workstation variants。

## 1. Third-generation Tensor Cores

Ampere adds/expands:
- BF16；
- TF32；
- FP64 Tensor Core；
- INT8/INT4 MMA modes；
- structured sparsity support in relevant products/kernels。

## 2. TF32

TF32 illustrates:
```
memory storage format
!= matrix multiplication internal precision
```

FP32 tensors can use TF32-like reduced multiply precision with FP32 accumulation on supported Tensor Core paths.

## 3. Asynchronous global→shared copy

Ampere adds hardware-accelerated async copy:
```
global memory
→ shared memory
```

without forcing the normal register-staging path.

This is a major ancestor of modern pipelined GEMM/attention kernels:

```
load next tile
while
compute current tile
```

## 4. Split arrive/wait barriers

Hardware barriers support producer-consumer pipelines and finer asynchronous coordination.

## 5. Memory system

GA100 adds:
- much larger L2；
- L2 persistence/residency controls；
- high-bandwidth HBM2。

GA10x has different cache/memory characteristics.

## 6. 2× FP32 detail is variant-specific

Official guide notes compute capability 8.6 devices provide 2× FP32 operations/cycle/SM relative to 8.0.

So do not state:
```
"Ampere SM = one universal FP32 layout"
```

## Stable consequence

Ampere's long-term lesson:

```
modern fast kernels are pipelines,
not just arithmetic loops
```

They overlap:
- global memory；
- shared-memory staging；
- matrix math；
- synchronization。

---

# Part IX — Ada: optimize RTX/AI efficiency and cache locality

Primary:
https://www.nvidia.com/en-us/geforce/ada-lovelace-architecture/
https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf

## Fourth-generation Tensor Cores

Ada supports modern Tensor Core inference, including FP8 paths in current NVIDIA ecosystem documentation.

## Large L2 shift

Full AD102:
- 96 MB L2；
- 16× GA102's 6 MB according to NVIDIA whitepaper.

Stable lesson:
```
larger last-level cache
→ more opportunity to avoid external GDDR traffic
```

This does not make GDDR bandwidth irrelevant; it changes the locality tradeoff.

## Shader Execution Reordering (SER)

SER dynamically reorganizes divergent shader work for ray-tracing/neural-graphics workloads.

For local LLM, SER itself is not the key feature.

The transferable architecture idea is:
```
hardware/software scheduling can reorder irregular work
to restore execution coherence
```

## AV1 encode

Ada adds major media-block upgrades including AV1 encode.

Not core to LLM inference, but important for workstation / multimodal / creator use.

## Stable consequence for this course

Ada's most relevant lessons are:
- mature fourth-gen Tensor Core inference；
- very large L2 on top-end designs；
- high clocks/efficiency；
- modern media engine。

Avoid treating graphics-only SER/RT improvements as LLM acceleration.

---

# Part X — Hopper: transformers reshape the programming hierarchy

Primary:
https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/

Hopper is primarily a datacenter architecture branch, not the GeForce successor to Ampere.

Ada and Hopper coexist as different market branches.

## 1. Fourth-generation Tensor Cores + FP8

Hopper adds:
- FP8；
- Transformer Engine；
- fourth-gen Tensor Core improvements。

Transformer Engine manages precision/scaling choices around transformer layers.

## 2. Tensor Memory Accelerator (TMA)

Ampere async copy still asks CUDA threads to participate in address generation/copy orchestration.

Hopper TMA pushes more of this work into dedicated hardware:

```
global tensor tile
→ TMA
→ shared memory
```

A small number of threads can initiate large multidimensional transfers while other threads compute.

This is the hardware expression of:

```
data movement is important enough to deserve its own accelerator
```

## 3. Thread Block Clusters

CUDA hierarchy extends conceptually:

```
thread
→ warp
→ thread block
→ thread block cluster
→ grid
```

Blocks in a cluster can be scheduled close together and cooperate.

## 4. Distributed Shared Memory

Clusters enable cross-SM shared-memory-style cooperation.

This breaks the old simple rule:
```
shared memory belongs only to one block / one SM
```
for cluster-aware Hopper programming.

## Stable consequence

Hopper pushes CUDA toward:
- warp specialization；
- asynchronous producer/consumer roles；
- hardware-managed tensor movement；
- multi-SM cooperative locality。

These ideas strongly influence modern FlashAttention/GEMM kernels.

---

# Part XI — Blackwell: low precision + AI scheduling split across datacenter and RTX branches

Primary:
- NVIDIA architecture timeline
- RTX Blackwell whitepaper:
  https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf
- NVIDIA current RTX/PRO Blackwell product docs
- NVIDIA Blackwell datacenter docs

## Important: Blackwell is a family, not one topology

Datacenter Blackwell and RTX Blackwell share architecture lineage but differ significantly.

Do not copy a B200/GB200 multi-die or NVLink feature onto an RTX 50-series card.

## RTX Blackwell

Official RTX Blackwell whitepaper shows:
- fifth-generation Tensor Cores；
- FP4 support；
- fourth-generation RT Cores；
- 128 KB L1/shared in the shown SM；
- GDDR7 generation for RTX products；
- new neural-shader/AI scheduling features。

FP4 matters because it attacks both:
- model memory footprint；
- matrix throughput on supported native paths。

But Slice 13 rule remains:

```
an FP4-capable GPU
!= every 4-bit LLM automatically uses native FP4 Tensor Cores
```

Backend/kernel format compatibility remains decisive.

## Datacenter Blackwell

Datacenter variants emphasize:
- large-scale AI；
- high-bandwidth memory；
- high-bandwidth scale-up fabric；
- second-generation Transformer Engine；
- very low precision including FP4-class formats。

Some flagship Blackwell datacenter products use multi-die/package-level designs.

That statement must not be generalized to RTX Blackwell.

## Stable consequence

Blackwell continues three long-running trends:

1. lower precision moves from software compression toward hardware-native compute；
2. data movement/cache capacity keep rising in importance；
3. AI work increasingly receives dedicated scheduling/control hardware。

---

# Cross-generation synthesis

## A. The SM evolves from "wide processor" to "partitioned pipeline engine"

```
G80: unified programmable SM
Fermi: compute-oriented SM + cache
Kepler: very wide SMX
Maxwell: scheduler-owned SMM partitions
Pascal: smaller compute-oriented partitions on GP100
Volta/Turing: explicit FP/INT paths + modern scheduling
Ampere+: async pipelines + increasingly specialized matrix/data movement
```

## B. Memory hierarchy is as important as arithmetic

```
shared memory
→ L1/L2 compute caches
→ unified cache/shared designs
→ giant L2 on some consumer generations
→ async copies
→ TMA / cluster locality
```

This is the direct ancestry of:
- tiled GEMM；
- FlashAttention；
- fused dequant GEMM；
- KV-cache kernels。

## C. AI specialization arrives in layers

```
Pascal:
  FP16 / INT8 primitives

Volta:
  Tensor Cores

Turing:
  Tensor Core inference formats in mainstream RTX

Ampere:
  BF16 / TF32 / async pipelines

Ada:
  FP8-class RTX inference + large cache

Hopper:
  FP8 Transformer Engine + TMA/clusters

Blackwell:
  FP4-class native AI path + newer AI orchestration
```

## D. Datacenter and consumer branches must not be merged

Examples:
- Pascal GP100 vs GP104；
- Ampere GA100 vs GA10x；
- Hopper datacenter vs Ada consumer/workstation；
- Blackwell datacenter vs RTX Blackwell。

A course that says only:
```
"Pascal has HBM2"
"Ampere has 40 MB L2"
"Blackwell is dual-die"
```
without variant labels is wrong.

## E. Why this history matters for local LLM buyers

When looking at a used NVIDIA card, ask:

1. architecture / exact die?
2. compute capability?
3. VRAM capacity?
4. real memory bandwidth?
5. matrix datatype support?
6. current driver/toolkit support?
7. runtime/backend kernels?
8. does workload hit compute, memory, or interconnect roof?
9. PP vs TG?
10. power/cooling/TCO?

Architecture tells you what is *possible*.
The exact board + software stack tells you what is *usable*.

---

# Stable claims to avoid

- "CUDA core counts are comparable across generations."
- "Every chip in one architecture has the same AI features."
- "Pascal means HBM2/NVLink."
- "Volta only matters because Tensor Cores."
- "Turing is just ray tracing."
- "Ampere is one SM design."
- "Ada's graphics SER directly accelerates LLM decode."
- "Hopper is the GeForce generation after Ampere."
- "Every Blackwell GPU is dual-die."
- "FP4-capable Blackwell means any Q4 GGUF uses FP4 Tensor Cores."
- "Newer architecture automatically beats older architecture for every local-LLM workload."

---

# Dynamic support boundary

Current 2026 CUDA/driver support is intentionally NOT frozen here.

See:
```
intelligence/gpu/nvidia-generation-support-2026-08-27.md
```

because toolkit/driver support changes faster than architecture history.

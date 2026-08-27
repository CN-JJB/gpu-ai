# Research Note 0007 — 单机多 GPU：Capacity Aggregation、Split、P2P 与 Interconnect Roof

日期：2026-08-26

## Research question

垃圾佬最常见的多卡直觉：

> 两张 12 GB 卡就是 24 GB，而且算力也差不多翻倍吧？

为什么这个说法同时混淆了：

- memory capacity aggregation；
- model partitioning；
- single-request latency；
- aggregate throughput；
- GPU-to-GPU communication；
- physical topology / P2P；
- software backend split strategy？

本切片建立：

~~~text
work partition
→ per-GPU compute
→ cross-GPU data movement
→ synchronization
→ scaling efficiency
~~~

模型，并把之前的 Roofline 扩展为：

~~~text
compute roof
memory roof
interconnect roof
~~~

## Scope

Primary focus：

- single-node NVIDIA/AMD discrete multi-GPU；
- llama.cpp current split modes as real local-LLM implementation；
- PCIe / NVLink / xGMI-style topology principles；
- P2P measurement。

Apple Silicon 不机械套 discrete multi-GPU 模型；它的 unified-memory SoC GPU 路径在迁移章节单独说明。

Dynamic flags/topology tools go to：

intelligence/gpu/multi-gpu-topology-2026-08-26.md

llama.cpp pinned source：

d7a2074112d27649303fa107eb8c94db1ee435f3

## Primary sources

### 1. NVIDIA CUDA Programming Guide — Multi-GPU / peer access

https://docs.nvidia.com/cuda/cuda-programming-guide/

Current CUDA guide states multi-GPU applications must：

- enumerate/select devices；
- distribute data/work；
- manage contexts/execution；
- communicate results/data across devices。

It documents peer-to-peer memory access and transfers, and describes NVLink as a high-bandwidth peer communication path when available.

Stable point：

~~~text
multiple GPUs
→ communication is part of the algorithm
~~~

not a transparent pool of compute/memory.

### 2. NVIDIA nvidia-smi topology documentation

https://docs.nvidia.com/deploy/nvidia-smi/index.html

Current topology commands include：

~~~text
nvidia-smi topo -m
nvidia-smi topo -p2p r
nvidia-smi topo -p2p w
nvidia-smi topo -p2p p
~~~

The topology matrix distinguishes：

- PIX
- PXB
- PHB
- NODE
- SYS
- NV#

and reports CPU/NUMA affinity.

Teaching consequence：

two GPUs in the same machine can have very different communication paths.

### 3. AMD HIP — Multi-device management

https://rocm.docs.amd.com/projects/HIP/en/develop/how-to/hip_runtime_api/multi_device.html

Current HIP docs explicitly state：

- P2P lets one GPU directly access another GPU's memory；
- this avoids involving host memory；
- without activated P2P, hipMemcpy device-to-device can still work through host staging, with a performance penalty。

This is a key cross-vendor validation。

### 4. AMD RCCL

https://rocm.docs.amd.com/projects/rccl/en/develop/

RCCL provides optimized multi-GPU/multi-node collectives using PCIe/xGMI and topology-aware communication.

Collectives include patterns needed by model parallelism：

- all-reduce；
- all-gather；
- reduce-scatter；
- broadcast；
- send/recv。

Stable point：

tensor/model parallelism often needs communication collectives, not just memcpy.

### 5. AMD ROCm SMI topology

https://rocm.docs.amd.com/projects/rocm_smi_lib/en/latest/doxygen/html/group__HWTopo.html

Current API exposes：

- GPU-GPU link type/hops；
- min/max bandwidth information；
- P2P accessibility；
- NUMA node。

### 6. AMD TransferBench / RVS

https://rocm.docs.amd.com/projects/TransferBench/en/docs-1.66.02/reference/presets.html

https://rocm.docs.amd.com/projects/ROCmValidationSuite/en/master/ug1main.html

Current TransferBench offers P2P and all-to-all presets, reporting measured GPU↔GPU bandwidth.

Current RVS PBQT checks P2P compatibility and can benchmark uni/bidirectional peer throughput.

Current ROCm Bandwidth Test docs mark that older tool as deprecated/EOL and recommend migration to TransferBench/RVS.

### 7. PCI-SIG PCIe 4.0 FAQ

https://pcisig.com/faq?field_category_value%5B%5D=pci_express_4.0&keys=

PCI-SIG documents PCIe 4.0 signaling at 16 GT/s and twice PCIe 3.0 bandwidth.

Stable course point：

generation/width defines an upper transport capability, but application-visible P2P bandwidth must be measured and depends on topology/protocol/platform.

### 8. llama.cpp current multi-GPU controls

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

https://github.com/ggml-org/llama.cpp/blob/master/tools/llama-bench/README.md

Current common split modes：

~~~text
none
layer
row
tensor
~~~

Current server docs describe：

- none：one GPU；
- layer：split layers and KV across GPUs；
- row：split weights by rows, parallelized；
- tensor：split weights and KV, parallelized, currently experimental。

Current controls also include：

- tensor-split proportions；
- main GPU；
- device list；
- GPU layers。

These are dynamic llama.cpp implementation details; stable Lesson teaches split families, not eternal flag semantics.

## Findings

### F1 — Two VRAM capacities do not become one contiguous VRAM automatically

Two 12 GiB cards provide：

~~~text
12 GiB on GPU0
12 GiB on GPU1
~~~

not：

~~~text
one generic 24 GiB allocation
~~~

A 20 GiB model can use both only if software partitions/shards its tensors/state so each device's local allocations fit.

Therefore：

~~~text
capacity aggregation
requires software partitioning
~~~

### F2 — Even “capacity aggregation” is not simple addition

Per GPU also needs some combination of：

- runtime buffers；
- local KV；
- duplicated metadata/tensors；
- communication buffers；
- graph/workspace；
- allocator headroom。

So：

~~~text
2 × 12 GiB
!= exactly 24 GiB usable model payload
~~~

### F3 — Data Parallel and Model Parallel solve different goals

**Data parallel / replicas**

~~~text
GPU0: full model
GPU1: full model
~~~

Good for：

- independent requests；
- aggregate throughput。

Does not help a single model that cannot fit one GPU.

**Model parallel / sharding**

~~~text
one model
→ partitioned across GPUs
~~~

Needed to aggregate capacity for an oversized single model.

### F4 — Layer / Pipeline split is primarily a capacity strategy for one token

Simplified：

~~~text
layers 0..15 → GPU0
layers 16..31 → GPU1
~~~

One token must still pass through：

~~~text
GPU0 stage
→ activation transfer
→ GPU1 stage
~~~

The layers themselves remain causally sequential.

Therefore single-request latency often behaves more like：

~~~text
same total layer compute
+ inter-stage transfer
~~~

than ideal 2× compute speedup.

Pipeline/multiple active work can improve throughput by overlapping stages, but one-token critical path is not “half the layers therefore half latency.”

### F5 — Tensor parallel can reduce per-layer compute time but adds collectives

Simplified per layer：

~~~text
matrix/tensor split across GPU0/GPU1
→ both compute partial result
→ exchange/reduce/gather
→ next layer
~~~

Possible benefit：

~~~text
compute per GPU ≈ compute / N
~~~

New cost：

~~~text
communication + synchronization every layer/group
~~~

Hence tensor parallel is much more interconnect-sensitive.

### F6 — Communication adds a new Roofline

A simple latency model：

~~~text
T_N
≈ T_compute / N
+ bytes_on_critical_path / effective_link_bandwidth
+ synchronization
+ imbalance
~~~

Speedup：

~~~text
S_N = T_1 / T_N
~~~

Efficiency：

~~~text
E_N = S_N / N
~~~

If communication dominates：

~~~text
N ↑
but T_N stops falling
→ scaling efficiency collapses
~~~

### F7 — Interconnect bandwidth is not GPU VRAM bandwidth

A card may have：

~~~text
VRAM bandwidth = hundreds of GB/s or TB/s
~~~

while GPU↔GPU communication over PCIe is far lower.

Tensor-parallel kernels that repeatedly move partial results can therefore hit：

~~~text
interconnect roof
~~~

even though each GPU's local VRAM is fast.

### F8 — P2P direct path matters

NVIDIA/AMD both support direct peer access on compatible topology/config.

AMD official docs give the useful failure mode：

~~~text
no direct P2P
→ device copy can fall back through host staging
→ performance penalty
~~~

Thus before multi-GPU inference：

~~~text
can both GPUs enumerate?
~~~

is insufficient.

Need：

~~~text
can they peer?
what path?
what measured bandwidth?
~~~

### F9 — PCIe slot labels are not topology Evidence

Two physical x16-length slots can be：

- x16/x4 electrically；
- x8/x8 after bifurcation；
- behind one or multiple switches；
- on different CPU sockets/NUMA nodes；
- routed through host bridges。

NVIDIA's topology matrix explicitly distinguishes these paths.

Therefore garbage-hardware investigation must record：

- negotiated link width/speed；
- topology；
- P2P accessibility；
- measured bandwidth。

### F10 — NVLink/xGMI can raise the interconnect roof, but topology still matters

High-bandwidth direct links reduce communication penalty.

But：

- not every GPU SKU supports them；
- link count/topology differs；
- software must use the path；
- collectives can still have synchronization/algorithm overhead。

Do not convert “has NVLink/xGMI” into “multi-GPU scaling perfect.”

### F11 — Collectives matter for Tensor Parallel

Tensor parallel frequently requires operations analogous to：

- all-reduce；
- all-gather；
- reduce-scatter。

NCCL/RCCL exist because efficient collective scheduling/topology usage is a first-class problem.

A plain point-to-point bandwidth test is necessary but not sufficient to predict collective performance.

### F12 — Prefill and Decode respond differently to multi-GPU communication

Prefill：

- larger GEMMs；
- more compute per communication event；
- often more opportunity to amortize collective cost。

Decode：

- small per-token work；
- latency-sensitive；
- frequent synchronization；
- often memory/interconnect sensitive。

Therefore：

~~~text
multi-GPU PP speedup
!= multi-GPU TG speedup
~~~

Record both.

### F13 — Quantization can make the interconnect relatively more important

Weight quantization reduces：

- model capacity；
- local VRAM traffic；
- target compute in optimized kernels。

But some cross-GPU activation/collective communication may not shrink proportionally.

Thus after aggressive quantization：

~~~text
local compute/memory gets cheaper
→ communication fraction can grow
~~~

A setup can become interconnect-bound sooner.

### F14 — Heterogeneous GPUs create imbalance

Layer split can sometimes allocate more layers to stronger/larger devices.

Tensor parallel is synchronized within layers, so：

- slower GPU；
- lower bandwidth path；
- asymmetric link；
- weak peer capability；

can constrain the group.

~~~text
fastest GPU does not set group speed
critical/slowest synchronized path can
~~~

### F15 — Multi-GPU capacity, latency and throughput are three separate buying goals

**Goal A: fit a larger model**

Layer/model split may be enough even with limited speedup.

**Goal B: lower one-request latency**

Needs actual parallel compute and a fast communication path; tensor parallel is relevant but expensive in communication.

**Goal C: serve more independent users**

If model fits each GPU, replicas/data parallel may avoid model-parallel communication entirely.

These must not be ranked by one benchmark.

### F16 — CPU offload plus multi-GPU adds another link

A partially offloaded setup may simultaneously use：

~~~text
GPU0 local VRAM
GPU1 local VRAM
GPU↔GPU link
CPU RAM
PCIe CPU↔GPU
~~~

The slowest critical data path can become the true roof.

## L0 teaching scenario

Single-GPU target compute：

~~~text
10 ms/token
~~~

Two-GPU tensor split ideal compute：

~~~text
5 ms/token
~~~

Critical communication per token：

~~~text
64 MiB
~~~

Synchronization overhead：

~~~text
0.2 ms
~~~

Then：

~~~text
T_2
= 5 ms
+ 64 MiB / effective P2P bandwidth
+ 0.2 ms
~~~

At 8 GiB/s：

~~~text
T_2 ≈ 13.01 ms
speedup ≈ 0.77×
~~~

At 32 GiB/s：

~~~text
T_2 ≈ 7.15 ms
speedup ≈ 1.40×
~~~

At 128 GiB/s：

~~~text
T_2 ≈ 5.69 ms
speedup ≈ 1.76×
~~~

Same two GPUs, different interconnect roof → opposite buying conclusion.

These are synthetic units, not a claim about any named GPU.

## Stable investigation workflow

1. Does target model fit one GPU?
2. If not, what exactly must be sharded?
3. Data replica, layer split or tensor split?
4. Per-device usable memory/headroom?
5. Physical PCIe/link topology?
6. P2P available?
7. Actual unidirectional/bidirectional peer bandwidth?
8. PP vs TG one-GPU baseline?
9. Same artifact/config multi-GPU PP/TG?
10. Communication/sync overhead?
11. Scaling speedup and efficiency?
12. Only then decide whether second cheap GPU is worth it.

## Apple migration note

Apple Silicon unified-memory systems should not be modeled as two discrete VRAM pools connected by PCIe P2P.

The transferable questions are still：

- total memory capacity/headroom；
- local memory bandwidth；
- GPU execution path；
- whether work crosses another device/node boundary。

But the discrete-GPU split/topology model applies primarily to NVIDIA/AMD multi-adapter systems.

## Claims to avoid

- “2×12 GB = one 24 GB GPU。”
- “两张卡一定 2× tokens/s。”
- “模型能跨两卡加载就说明 P2P 正常。”
- “PCIe Gen4 x16 标签就等于实际 GPU↔GPU 31 GB/s。”
- “有 NVLink/xGMI 就一定线性 scaling。”
- “layer split 和 tensor parallel 是一回事。”
- “data parallel 能让 20 GB 模型塞进两张 12 GB 卡。”
- “PP scaling 可以直接代表 decode scaling。”
- “同型号双卡一定有相同 topology。”

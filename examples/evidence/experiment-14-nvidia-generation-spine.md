# Evidence — Experiment 14: NVIDIA Architecture Generation Spine

状态：stable architecture research complete; L0 lineage assertions verified; real-device inventory path ready.

## Claim under test

> NVIDIA generations are changes in execution, memory hierarchy, specialized math and programming model—not a monotonic CUDA-core list. An architecture-family name also does not guarantee identical features across every die/SKU.

## Official chronology

Current NVIDIA timeline confirms:

```
Tesla 2006
Fermi 2010
Kepler 2012
Maxwell 2014
Pascal 2016
Volta 2017
Turing 2018
Ampere 2020
Hopper 2022
Ada 2022
Blackwell 2024
```

Source:
https://www.nvidia.com/en-us/technologies/

## Stable architecture evidence

### Tesla / G80
NVIDIA Research describes a scalable unified, massively multithreaded architecture programmable in C.

### Fermi
Official whitepaper/CUDA history supports compute L1/L2 cache hierarchy, stronger numerical behavior, ECC and concurrent kernels.

### Kepler
Official tuning guide supports wider SMX, TLP+ILP, warp shuffle, and GK110-specific Hyper-Q/Dynamic Parallelism.

### Maxwell
Official tuning guide supports SMM scheduler-owned partitions, reduced arithmetic latency, dedicated shared memory, higher block residency and shared-memory atomics.

### Pascal
Official tuning guide explicitly distinguishes GP100 and GP104:
- GP100: high FP16 + HBM2;
- GP104: very different FP16 ratio + INT8 DP4A path.

This directly validates:
```
architecture family != uniform AI feature set
```

### Volta
Official tuning guide supports first Tensor Cores, Independent Thread Scheduling and the new warp synchronization rules.

### Turing
Official tuning guide/architecture material supports concurrent FP32+INT32, Independent Thread Scheduling and expanded Tensor inference types.

### Ampere
Official tuning guide supports BF16/TF32, async global→shared copy, split barriers, L2 residency controls and cc8.0/8.6 differences.

### Ada
Official docs support fourth-gen Tensor, FP8-era RTX path, AD102 96 MB L2, SER and AV1 encoding.

### Hopper
Official architecture docs support FP8 Transformer Engine, TMA and thread-block clusters.

### RTX Blackwell
Official current whitepaper supports fifth-gen Tensor, FP4, documented 128 KB L1/shared SM resource and GDDR7 path.

## L0 verification

Experiment:
`labs/experiments/23-nvidia-generation-feature-traps/`

Validated result:

```
10 / 10 PASS
```

Assertions include:
- Volta first Tensor Core;
- Volta first Independent Thread Scheduling;
- Ampere async global→shared;
- Hopper TMA/block clusters;
- all-Pascal-HBM2 false;
- all-Pascal-fast-FP16 false;
- all-Ampere-identical-SM false;
- Hopper-as-GeForce-successor false;
- all-Blackwell-dual-die false;
- Q4-GGUF-guarantees-FP4 false.

## Real Evidence path

Experiment 24 captures:
- exact name;
- compute capability;
- driver;
- memory;
- PCIe/topology;
- optional PyTorch build;
- raw nvidia-smi output.

No real GPU benchmark is prefilled.

## Dynamic 2026 software evidence

Current NVIDIA matrix says:
- Maxwell/Pascal/Volta end at CUDA 12.x and R580;
- Turing+ current/ongoing;
- Kepler/Fermi require much older stacks.

CUDA 13 release notes explicitly remove Maxwell/Pascal/Volta offline compilation and library support.

These facts live in:
`intelligence/gpu/nvidia-generation-support-2026-08-27.md`.

## Learner should reject

- CUDA-core-count-only comparisons;
- architecture-name-only feature claims;
- “Pascal = HBM2”;
- “Turing = just ray tracing”;
- “Ampere = one SM design”;
- “Hopper is an RTX 30→40 linear successor”;
- “Blackwell = every product dual-die”;
- “native FP4 support = every 4-bit quant uses native FP4”.

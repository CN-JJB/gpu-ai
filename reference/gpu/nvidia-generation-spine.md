# NVIDIA Architecture Generation Spine — 速查

## Timeline

| architecture | year | central lesson |
|---|---:|---|
| Tesla / G80 era | 2006 | unified programmable GPU + SIMT/CUDA foundation |
| Fermi | 2010 | compute-first caches, reliability, concurrency |
| Kepler | 2012 | wide SMX + more concurrency / Hyper-Q / dynamic parallelism |
| Maxwell | 2014 | SMM partition efficiency + dedicated shared memory |
| Pascal | 2016 | product-family split; HBM2/NVLink/UM on GP100; FP16/INT8 divergence |
| Volta | 2017 | Tensor Cores + Independent Thread Scheduling |
| Turing | 2018 | Tensor inference + FP/INT concurrency enters RTX |
| Ampere | 2020 | BF16/TF32 + async global→shared pipelines |
| Hopper | 2022 | FP8 + TMA + thread-block clusters |
| Ada | 2022 | fourth-gen Tensor + large L2 + RTX efficiency |
| Blackwell | 2024 | fifth-gen Tensor + FP4-class AI; datacenter/RTX branches |

## The four recurring questions

For every generation ask:

### 1. Execution
```
SM shape?
warp schedulers?
FP/INT paths?
new synchronization?
```

### 2. Memory
```
registers?
shared memory?
L1/L2?
HBM/GDDR?
async copy?
```

### 3. Specialized math
```
FP16?
INT8?
Tensor Core?
BF16/TF32?
FP8?
FP4?
```

### 4. Software
```
compute capability?
CUDA feature?
runtime/library support?
current driver support?
```

## Tesla → Kepler

### Tesla/G80
- unified shader/compute pool
- SIMT/warp/SM
- CUDA foundation
- explicit shared memory

### Fermi
- L1 + unified L2 cache hierarchy
- configurable shared/L1
- ECC / stronger HPC reliability
- concurrent kernels
- stronger IEEE/FMA/FP64

### Kepler
- wider SMX
- more TLP + ILP required
- 4 warp schedulers
- warp shuffle
- Hyper-Q (GK110)
- Dynamic Parallelism (GK110)

## Maxwell → Pascal

### Maxwell
- SMM scheduler-owned partitions
- simpler core mapping
- reduced arithmetic latency
- dedicated shared memory
- unified L1/texture
- fast shared atomics
- up to 32 blocks/SM

### Pascal
Do not collapse variants:

**GP100**
- HBM2
- NVLink
- high FP16
- strong FP64
- page-faulting Unified Memory

**GP10x**
- GDDR path
- different FP16 ratios
- INT8 DP4A on relevant variants

## Volta → Turing

### Volta
- first Tensor Cores
- dedicated FP32 + INT32
- Independent Thread Scheduling
- 128 KB combined L1/texture/shared backing
- explicit warp synchronization semantics

### Turing
- second-gen Tensor inference formats
- RT Core
- concurrent FP32 + INT32
- Independent Thread Scheduling in RTX
- unified 96 KB L1/shared resource

## Ampere → Ada

### Ampere
- 3rd-gen Tensor Core
- BF16 / TF32
- async global→shared copy
- split arrive/wait barriers
- GA100 large L2/residency controls
- GA10x cc8.6 doubles FP32 ops/cycle relative to cc8.0 layout

### Ada
- 4th-gen Tensor
- FP8 ecosystem
- third-gen RT
- SER
- AD102 96 MB L2
- AV1 encode

LLM-important:
- Tensor formats
- cache
- efficiency

Mostly graphics-important:
- SER / RT upgrades

## Hopper → Blackwell

### Hopper
- datacenter branch
- 4th-gen Tensor
- FP8 Transformer Engine
- TMA
- thread-block clusters
- distributed shared memory
- HBM/NVLink scale-up focus

### Blackwell
Two branches:
- datacenter Blackwell
- RTX Blackwell

Shared direction:
- 5th-gen Tensor
- lower precision
- more AI-specific orchestration

RTX Blackwell:
- FP4
- GDDR7 generation
- 128 KB L1/shared in documented SM
- 4th-gen RT

Never infer datacenter multi-die/NVLink topology from the RTX architecture name.

## Local LLM reading rule

Architecture can explain:
```
what kernels can exist
```

But performance still needs:
```
exact SKU
+ VRAM
+ bandwidth
+ runtime
+ quant kernel
+ PP/TG
+ current software support
```

## Most important anti-pattern

Never rank cards by:

```
CUDA core count
or
AI TOPS
or
architecture year
```

alone.

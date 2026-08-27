# NVIDIA Generation / CUDA Support Snapshot — 2026-08-27

Purpose: dynamic support and buyer-risk snapshot for the stable Tesla→Blackwell architecture lessons.

Stable architecture history lives in:
- `research/gpu/0008-nvidia-architecture-generation-spine.md`
- `reference/gpu/nvidia-generation-spine.md`
- `lessons/14-nvidia-architecture/`

## Current official architecture / CUDA matrix

Source:
https://docs.nvidia.com/datacenter/tesla/drivers/cuda-toolkit-driver-and-architecture-matrix.html

| architecture | compute capability | last/current CUDA Toolkit | last/current driver |
|---|---|---|---|
| Fermi | 2.0 | CUDA 8.0 | R390 |
| Kepler | 3.0 / 3.2 | CUDA 10.2 | R470 |
| Kepler | 3.5 / 3.7 | CUDA 11.x | R470 |
| Maxwell | 5.0 / 5.2 / 5.3 | CUDA 12.x | R580 |
| Pascal | 6.0 / 6.1 | CUDA 12.x | R580 |
| Volta | 7.0 | CUDA 12.x | R580 |
| Turing | 7.5 | ongoing | ongoing |
| Ampere | 8.0 / 8.6 | ongoing | ongoing |
| Ada | 8.9 | ongoing | ongoing |
| Hopper | 9.0 | ongoing | ongoing |
| Blackwell | current 10.x / 12.x entries | ongoing | ongoing |

Tesla / compute capability 1.x is older than the current support matrix and should be treated as historical/legacy.

## CUDA 13 cutoff

Current CUDA 13 documentation states Maxwell, Pascal and Volta are feature-complete and CUDA 13 removed:
- offline compilation targeting them;
- current CUDA library support for them.

CUDA 12.x remains the build line for these architectures.

Practical consequence:

```
Maxwell/Pascal/Volta may still run an intentionally pinned stack
but
"install latest CUDA" is no longer a valid default recipe
```

This is a software-longevity/TCO cost for used hardware.

## Turing boundary

As of this snapshot, Turing 7.5 remains on the current/ongoing line.

This makes Turing a useful *current* used-card boundary, but it is dynamic knowledge and must be revalidated before a purchase.

## Current compute-capability discovery

Current CUDA Programming Guide recommends:

```bash
nvidia-smi --query-gpu=name,compute_cap
```

Runtime alternatives include CUDA Runtime/Driver APIs and NVML.

Experiment 24 uses nvidia-smi because it has the lowest dependency burden.

## Architecture-family traps

### Pascal

Do not infer from the family name alone:
- HBM2;
- NVLink;
- GP100-class FP16;
- DP4A INT8.

GP100 and GP10x intentionally differ.

### Ampere

Do not merge:
- GA100 / cc8.0;
- GA10x / cc8.6.

Official tuning docs describe different FP32 throughput organization.

### Hopper vs Ada

They are parallel 2022-era market branches:
- Hopper: datacenter/HPC/AI;
- Ada: RTX/workstation/inference/graphics.

### Blackwell

Current family contains datacenter Blackwell and RTX Blackwell.

Some datacenter products use multi-die/package designs and high-bandwidth scale-up fabric.
RTX Blackwell follows a separate RTX/GDDR product path.

Never infer:
```
Blackwell name
→ dual die / HBM / NVLink
```
for a consumer card.

## RTX Blackwell current details

Source:
https://images.nvidia.com/aem-dam/Solutions/geforce/blackwell/nvidia-rtx-blackwell-gpu-architecture.pdf

Current whitepaper documents:
- fifth-generation Tensor Cores;
- FP4;
- fourth-generation RT Cores;
- documented SM with 128 KB L1 data cache/shared memory;
- GDDR7 memory subsystem.

Course boundary:

```
hardware FP4 support
!=
arbitrary 4-bit model format automatically uses FP4 Tensor Cores
```

Backend packed format and kernel compatibility still decide execution.

## Ada current details

Sources:
- https://www.nvidia.com/en-us/geforce/ada-lovelace-architecture/
- NVIDIA Ada architecture whitepaper.

Full AD102 documents:
- 96 MB L2;
- fourth-generation Tensor Cores;
- FP8-era RTX path;
- third-generation RT Core;
- Shader Execution Reordering;
- AV1 encode.

Do not generalize full-AD102 exact counts to every Ada chip.

## Stable-vs-dynamic buying rule

Stable:
```
architecture sets possible mechanisms
```

Dynamic:
```
driver/toolkit
+ backend
+ kernel support
+ model ecosystem
+ used price
```

Purchase recommendation requires both.

## Revalidation triggers

Re-check when:
- a new CUDA major version releases;
- R580 reaches end of lifecycle;
- Turing moves to legacy support;
- new Blackwell compute-capability entries appear;
- a new NVIDIA architecture appears;
- llama.cpp/PyTorch/TensorRT drop an architecture independently of CUDA.

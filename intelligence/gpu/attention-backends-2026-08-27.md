# Attention Backend Snapshot — 2026-08-27

Purpose: dynamic backend/hardware snapshot for Slice 12.

## PyTorch current SDPA

Current PyTorch documentation for:

```
torch.nn.functional.scaled_dot_product_attention
```

describes CUDA-side optimized implementations including:
- FlashAttention-2;
- Memory-Efficient Attention;
- a C++ math implementation.

Current API attempts to choose an implementation automatically.

Fine-grained selection uses:

```python
from torch.nn.attention import SDPBackend, sdpa_kernel
```

Current docs explicitly mark `sdpa_kernel` as beta / subject to change.

Important:
- fused implementations have input/hardware limitations;
- forcing an unavailable backend should produce warning/error;
- exact dispatch is dynamic.

## NVIDIA cuDNN

Current cuDNN SDPA documentation says its SDPA operation uses the FlashAttention-2 algorithm.

The current support matrix in the retrieved docs is tied to cuDNN 9.18.1 and lists hardware/toolkit constraints such as Ampere-or-newer for that operation.

Do not generalize this into:
```
all NVIDIA GPUs support all FlashAttention paths
```

PyTorch, cuDNN, external flash-attn, llama.cpp and other runtimes can have different kernels/support.

## llama.cpp current flag

Pinned llama.cpp snapshot:
```
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current llama-bench interface includes:

```
-fa, --flash-attn <on|off|auto>
```

default: auto.

The flag is a runtime control, not proof that the active kernel is literally the original paper implementation. Record exact build and backend.

## AMD ROCm ecosystem

Current ROCm Composable Kernel documentation includes GPU implementations of the FlashAttention algorithm.

Current AMD ROCm AI ecosystem documentation for a specific vLLM/ROCm stack also publishes Flash Attention packages/wheels.

This validates:
```
FlashAttention-style optimized attention exists in the AMD ROCm ecosystem
```

It does **not** validate universal support across every RDNA/CDNA GPU, OS, PyTorch wheel or dtype.

Consumer AMD compatibility remains dynamic intelligence and must be tested on the exact stack.

## Stable vs dynamic boundary

Stable:
- exact attention;
- tiling;
- online softmax;
- reduced HBM materialization;
- block/warp scheduling.

Dynamic:
- backend enum/API;
- GPU support;
- dtype/head-dim constraints;
- causal/varlen support;
- backend selection heuristics;
- kernel version;
- performance.

## Revalidation triggers

Re-check when:
- PyTorch changes SDPA backend API;
- backend names/dispatch change;
- cuDNN support matrix changes;
- llama.cpp flash-attn controls change;
- ROCm packaged attention kernels change;
- new GPU architectures add different attention engines/data movement.

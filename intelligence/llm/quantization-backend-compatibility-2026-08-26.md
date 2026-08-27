---
snapshot_date: 2026-08-26
type: dynamic-intelligence
topic: quantization-backend-compatibility
---

# Quantization Backend Compatibility Snapshot — 2026-08-26

## Why this file exists

量化兼容性变化太快，不能写进稳定 Lesson 当永久事实。本 snapshot 用于证明：

```text
quantization support
= backend-specific
+ hardware-specific
+ version-specific
```

部署前必须重新查 current docs。

## Hugging Face Transformers

Source:
https://huggingface.co/docs/transformers/quantization/overview

Current overview exposes method × platform matrix covering CPU、CUDA、ROCm、Metal/Apple Silicon、Intel GPU、torch.compile、bits 与 serialization/integration。

Teaching observation：不同 method 的 platform support 明显不同；同一个“4-bit”不能当平台兼容标签。

At snapshot time the overview shows AWQ with ROCm support, while bitsandbytes ROCm/Metal support is represented differently/partially. Do not copy this into stable Lesson.

## vLLM

Source:
https://docs.vllm.ai/en/latest/features/quantization/

Current vLLM page has its own implementation × hardware matrix。

At snapshot time：
- AWQ/GPTQ rows do not show AMD GPU support in vLLM's matrix；
- some llm-compressor FP8 paths show AMD GPU support；
- GGUF row shows AMD GPU support；
- support differs across NVIDIA generations, AMD, Intel and CPUs。

The page explicitly warns that the matrix is subject to change。

### Teaching conclusion

```text
Transformers integration != vLLM kernel implementation
```

“AWQ supports ROCm” without naming backend is incomplete。

## vLLM GGUF

Source:
https://docs.vllm.ai/en/latest/features/quantization/gguf/

At snapshot time：
- GGUF support is described as highly experimental / under-optimized；
- support moved to an out-of-tree GGUF plugin；
- feature interactions may be limited。

```text
vLLM can load a GGUF path
!= GGUF is equally mature in vLLM and llama.cpp
```

## llama.cpp

Sources:
https://github.com/ggml-org/llama.cpp/blob/master/README.md
https://github.com/ggml-org/llama.cpp/wiki/Feature-matrix

At snapshot time upstream documents backends including：
- Metal → Apple Silicon
- CUDA → NVIDIA GPU
- HIP → AMD GPU
- CPU/Vulkan/SYCL/others

The feature matrix separately tracks K-quants/I-quants/KV-cache quants/backend capabilities。

GGUF hardware support comes from the chosen backend and quant kernels。

## ExLlamaV2

Source:
https://github.com/turboderp-org/exllamav2

EXL2 is an ecosystem-specific mixed-bitrate quantized representation。Compatibility/performance should be checked against current ExLlamaV2 release、target hardware generation and frontend/runtime integration。

Do not translate “EXL2 model exists” into generic AMD/Apple support。

## Deployment checklist

Before claiming compatibility：
1. backend exact name + version
2. GPU/CPU exact architecture
3. model architecture
4. serialized representation
5. quant method
6. exact quant type / group size
7. loader support
8. kernel support
9. known limitations / open issues
10. tiny correctness + performance test

## Freshness rule

This file is stale by design after ecosystem changes。

For a real purchase/deployment decision：
- re-fetch official docs；
- create/update a newer snapshot；
- preserve this historical evidence rather than silently turning it into timeless Lesson text。

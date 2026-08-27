---
date: 2026-08-26
type: course-build-record
---

# Quantization / format / backend vertical slice completed

第六个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → Example Evidence → Dynamic Intelligence snapshot → Resources update → Learning update。

## Built artifacts

- research/llm/0002-quantization-formats-backends.md
- reference/llm/quantization-format-backend-map.md
- lessons/06-llm-quantization/01-bits-formats-backends.html
- labs/experiments/09-effective-bpw-metadata/
- examples/evidence/experiment-06-effective-bpw.md
- intelligence/llm/quantization-backend-compatibility-2026-08-26.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### “4-bit” is not one layer

The slice separates numerical representation、quantization method、serialized representation/container、runtime/kernel/hardware compatibility。

### Container is not quantization

Safetensors stores typed tensor metadata/data。GGUF stores metadata and per-tensor ggml types。Neither name alone states a whole-model bit rate。

### Algorithm is not file extension

GPTQ and AWQ are post-training quantization methods。A loader/runtime still needs serialization metadata、operators、target kernels and hardware support。

### Effective bpw is concrete

```text
bpw ≈ qbits + (scale_bits + zero_bits)/group_size
```

4-bit + FP16 scale：
- group32 = 4.5 bpw
- group64 = 4.25
- group128 = 4.125

95% at 4.25 bpw + 5% FP16：
```text
whole = 4.8375 bpw
```

This connects directly to Slice 05 VRAM budgeting。

### Dynamic compatibility belongs in intelligence

Current Transformers and vLLM official docs provide different support matrices for some same-name methods/platforms。

The durable statement is：
```text
support = backend + version + hardware + representation
```

### Apple migration is explicit

llama.cpp current upstream exposes Metal/Apple Silicon alongside CUDA/NVIDIA and HIP/AMD。

GGUF is not an Apple/NVIDIA/AMD format；hardware support arises from runtime backend and kernels。

## L0 experiment

Experiment 09 deterministically demonstrates that nominal 4-bit does not imply 4.000 whole-model bpw。

It deliberately does not emulate named AWQ/GPTQ/GGUF/EXL2 details。

## Skill workflow

- teach：one ambiguity (“4-bit model”) → transferable four-layer investigation model。
- research：HF、GPTQ/AWQ papers、llama.cpp upstream、vLLM、ExLlamaV2。
- intelligence separation：dynamic compatibility kept out of stable Lesson。
- no grill/to-spec；frozen v1 remains valid。

## Next

Complete the first real local-LLM deployment milestone with llama.cpp/GGUF + CPU fallback + CUDA/HIP/Metal migration paths and reproducible Evidence。

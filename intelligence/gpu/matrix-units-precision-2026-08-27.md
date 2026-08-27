# Matrix Units / Precision Snapshot — 2026-08-27

## NVIDIA current architecture map

### Volta
First Tensor Core generation in the stable course map:
- FP16-oriented matrix acceleration;
- FP16 or FP32 accumulation modes in documented HMMA evolution.

### Turing
Second-generation Tensor Core era:
- expands inference-oriented integer/sub-byte matrix modes such as INT8/INT4.

### Ampere
Official current Ampere tuning guide calls these third-generation Tensor Cores.

Documented additions include:
- BF16;
- TF32;
- FP64 Tensor Core;
- broader integer matrix instruction shapes.

Current official TF32 description:
- FP32-like exponent/range;
- reduced input precision;
- FP32 accumulator in documented WMMA path.

### Hopper
Current NVIDIA material identifies:
- fourth-generation Tensor Cores;
- FP8;
- Transformer Engine;
- TMA and newer scheduling/data-movement architecture.

### Blackwell
Current NVIDIA Blackwell product/Transformer Engine docs identify:
- fifth-generation Tensor Cores;
- FP4-class support such as NVFP4 in current TE;
- current product AI performance numbers may explicitly use precision+sparsity footnotes.

Exact SKU throughput is intentionally not copied into stable Lesson.

## NVIDIA FP8 current TE

Current Transformer Engine 2.18 docs describe:
- E4M3;
- E5M2;
- scaling recipes;
- amax/scale overhead;
- newer Blackwell MXFP8/NVFP4 modes.

This is strong evidence that low precision is a full data-format + scaling + kernel system, not just a smaller C type.

## PyTorch current FP32 matmul precision

Current PyTorch docs expose:

```
torch.set_float32_matmul_precision(
  "highest" | "high" | "medium"
)
```

The setting changes internal float32 matmul computation strategy without changing output dtype.

Current CUDA docs/PyTorch notes connect faster modes on supported NVIDIA GPUs with TF32 or other reduced-precision internal computation.

Experiment 22 records this setting explicitly.

## AMD current matrix core map

Current HIP docs describe CDNA MFMA:
- specialized matrix acceleration;
- tile-level matrix FMA;
- example `v_mfma_f32_16x16x4f16`;
- FP16 inputs accumulating to FP32.

Current ROCm precision-support docs show matrix-core type support by:
- CDNA1/2/3/4;
- RDNA2/3/4.

Notable current trend:
- FP8 support appears in newer CDNA/RDNA generations;
- exact type support is generation-specific.

Do not turn the current table into a timeless guarantee; keep it here in intelligence.

## Consumer-vs-datacenter warning

A precision appearing in an architecture family does not guarantee:
- every SKU exposes the same peak;
- every backend kernel supports it;
- every local LLM quant format maps to it.

Always verify exact GPU + runtime + kernel.

## TOPS footnote rule

When collecting market intelligence, record the full condition:

```
value
+ datatype
+ dense/sparse
+ clock assumption
+ source date
```

Never store just:
```
"AI = 1000 TOPS"
```
without its footnote semantics.

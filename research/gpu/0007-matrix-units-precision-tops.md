# Research Note 0009 — Matrix Units、Precision、Accumulator 与“广告 TOPS”

日期：2026-08-27

## Research question

为什么 GPU 规格表会同时出现：

- FP32 TFLOPS；
- FP16/BF16 Tensor performance；
- TF32；
- FP8；
- INT8；
- INT4 / FP4；
- 稀疏 TOPS；

但一个 4-bit 本地 LLM 并不能简单拿“INT4/FP4 TOPS”去预测 tokens/s？

需要把四层拆开：

```
storage format
→ kernel input datatype
→ matrix instruction datatype
→ accumulator/output datatype
```

再加一层：

```
theoretical peak
→ achieved utilization
→ Roofline / memory bound
→ end-to-end performance
```

## Primary sources

### 1. NVIDIA Ampere Tuning Guide

https://docs.nvidia.com/cuda/ampere-tuning-guide/

Official table tracks Tensor Core evolution across Volta/Turing/Ampere.

Stable architecture points:
- Volta: Tensor Core FP16 matrix operations；
- Turing: expands matrix integer modes including INT8 / sub-byte；
- Ampere: third-generation Tensor Cores add BF16, TF32 and FP64 Tensor Core modes.

Ampere documentation also makes the accumulator distinction explicit:
- BF16 matrix inputs → FP32 accumulator；
- TF32 inputs → FP32 accumulator；
- INT8 matrix inputs → INT32 accumulator.

### 2. CUDA Programming Guide — WMMA alternate floating point

https://docs.nvidia.com/cuda/cuda-programming-guide/

Current CUDA guide states:
- BF16 has FP32-like exponent range with reduced precision；
- TF32 keeps FP32-like range with reduced precision and uses FP32 accumulator in WMMA；
- matrix input type and accumulator type are separate choices/constraints.

### 3. NVIDIA Hopper / Transformer Engine

https://docs.nvidia.com/deeplearning/transformer-engine/

Current NVIDIA Transformer Engine docs:
- FP8 support on Hopper/Ada/Blackwell；
- FP8 uses scaling/quantization recipes；
- E4M3 and E5M2 trade precision vs dynamic range；
- Blackwell adds newer low-precision formats such as NVFP4/MXFP8 in current TE.

Hopper official material identifies fourth-generation Tensor Cores and FP8.

### 4. NVIDIA Blackwell current product / TE docs

Current NVIDIA Blackwell products describe fifth-generation Tensor Cores and FP4 support.

Important evidence lesson:
some advertised AI TOPS footnotes specify:
- precision;
- sparsity.

Therefore a single “AI TOPS” number is not precision-neutral.

### 5. AMD HIP / ROCm matrix hardware

https://rocm.docs.amd.com/projects/HIP/en/latest/understand/hardware_implementation.html

Current HIP docs describe CDNA matrix fused multiply-add (MFMA) units:
- specialized matrix hardware；
- matrix tile operations；
- FP16/BF16/INT8/FP32 families depending architecture；
- example FP16 matrix inputs accumulating to FP32.

ROCm precision-support tables show matrix-core datatype support varies strongly by CDNA/RDNA generation.

## Stable findings

### F1 — Matrix unit ≠ ordinary scalar/vector ALU

Ordinary ALU view:

```
many independent element operations
```

Matrix unit view:

```
matrix tile A × tile B + accumulator tile
```

A single matrix instruction represents many multiply-accumulate operations over a tile.

The efficiency comes from:
- dense regular structure；
- reuse；
- amortized instruction/control overhead；
- specialized datapaths.

### F2 — Input precision and accumulation precision are different

Example pattern:

```
FP16/BF16 input
→ matrix multiply
→ FP32 accumulation
```

or:

```
INT8 input
→ integer matrix multiply
→ INT32 accumulation
```

Reason:
many low-precision products are summed together, so accumulation often needs more range/precision.

Therefore “FP16 Tensor Core” does not mean every internal value stays FP16.

### F3 — Storage bit-width is yet another layer

A GGUF Q4 weight may be stored near 4 bits/weight plus metadata/scales.

But a runtime can implement it in many ways:

```
Q4 storage
→ dequantize tile to FP16/BF16
→ FP16/BF16 matrix instruction
→ FP32-ish accumulation
```

or on some backend/hardware:

```
low-bit storage
→ native low-bit matrix path
→ wider accumulator
```

Thus:

```
4-bit model file
!= guaranteed native INT4/FP4 arithmetic
```

This connects directly to Slice 06 quantization/container/backend separation.

### F4 — FP8 is not “just smaller FP16”

FP8 formats require careful range management.

Current NVIDIA TE documents E4M3 and E5M2:
- E4M3: more precision, less range；
- E5M2: more range, less precision.

Practical FP8 execution often needs:
- scale factors；
- amax handling；
- casts；
- possibly transpose/layout handling；
- higher-precision accumulation.

Low precision can add overhead as well as remove work.

### F5 — TF32 is a compute mode, not a storage-format replacement for FP32 files

Ampere Tensor Cores can use TF32-style reduced input precision with FP32 range and FP32 accumulation.

Stable lesson:
```
storage dtype
and
matrix math precision
can differ
```

Do not teach TF32 as “19-bit model weights on disk”.

### F6 — Theoretical peak only applies to a particular mode

A GPU can have different peaks for:
- FP32 vector math；
- FP16/BF16 matrix math；
- INT8；
- FP8；
- FP4；
- sparse vs dense.

These are not interchangeable.

If a product page says:
```
AI TOPS
```

you must ask:
1. which datatype?
2. dense or structured sparsity?
3. boost clock?
4. matrix unit path?
5. what counting convention?

### F7 — Peak matrix throughput requires compatible shapes

Matrix hardware operates on tiles.

Poor shapes can cause:
- padding；
- wasted lanes；
- small-GEMM launch overhead；
- insufficient parallel tiles；
- low occupancy；
- conversion/dequant overhead dominating.

Therefore:

```
peak TOPS
is an upper roof
not an automatic application rate
```

### F8 — Decode is a classic place where huge matrix TOPS can mislead

LLM prefill often forms large GEMMs:
```
many tokens × hidden
```

Decode often behaves more like:
```
one/few tokens × huge weight matrix
```

The second case has:
- much lower batch dimension；
- lower matrix-unit utilization；
- very high weight-byte traffic per generated token.

So a GPU with enormous low-precision peak compute can still be decode memory-bandwidth-bound.

### F9 — Quantization can improve decode even without native low-bit matrix arithmetic

If weights shrink from ~16-bit to ~4-bit storage:

```
weight bytes per token ↓
```

That can increase decode tokens/s simply by reducing VRAM traffic.

Even if the kernel dequantizes to FP16 before matrix math.

This is a critical distinction:

```
quantization speedup
can come from bandwidth reduction
without
native INT4 tensor-core saturation
```

### F10 — Native low-bit arithmetic can add another speedup layer

When hardware/backend truly supports:
- native low-bit matrix multiply；
- efficient packed layout；
- fast scale application；
- sufficient shape utilization；

then compute throughput may also rise.

Total benefit can then combine:

```
less memory traffic
+
faster matrix arithmetic
```

But both must be verified.

### F11 — Accumulator choice affects numerical behavior

Lower input precision:
- increases quantization/rounding error；
- may reduce dynamic range.

Wider accumulation:
- reduces summation error/range problems；
- does not restore information already lost in input quantization.

So:

```
FP16 input + FP32 accumulate
!= FP32 input
```

### F12 — NVIDIA generational mental map

Stable high-level map:

| generation | matrix-unit lesson |
|---|---|
| Volta | first Tensor Cores; FP16-focused matrix acceleration |
| Turing | broader inference integer/sub-byte matrix modes |
| Ampere | 3rd-gen; BF16, TF32, FP64 Tensor Core additions |
| Hopper | 4th-gen; FP8 + Transformer Engine era |
| Blackwell | 5th-gen; current FP4-class acceleration expands low-precision frontier |

Exact SKU throughput belongs in intelligence.

### F13 — AMD mapping uses different names but same transferable questions

AMD CDNA/ROCm exposes MFMA matrix hardware.

Transferable model:

```
what matrix instruction?
what input datatype?
what accumulator?
what tile?
what library/kernel selects it?
what achieved utilization?
```

Do not force NVIDIA Tensor Core terminology onto AMD hardware.

### F14 — Apple must be treated separately

Apple GPU + Neural Engine + unified-memory SoC should not be collapsed into one generic “TOPS” number.

A later Apple-specific slice should distinguish:
- GPU matrix/Metal execution；
- Neural Engine；
- memory bandwidth；
- framework dispatch.

Do not compare ANE TOPS directly with NVIDIA Tensor Core TOPS as if they were the same execution target.

## L0 experiment

Use synthetic peaks only.

Compare:
- FP32 path；
- FP16 matrix path；
- INT8 matrix path；
- native INT4 path；
- Q4 weight-only path that dequantizes into FP16 compute.

Two workload profiles:

### Prefill-like
- high arithmetic intensity；
- good tile utilization.

### Decode-like
- low arithmetic intensity；
- poor small-M matrix utilization.

Model:

```
achieved_compute
= min(
    peak_compute × utilization,
    memory_bandwidth × arithmetic_intensity
  )

effective_after_overhead
= achieved_compute / (1 + conversion_overhead)
```

This demonstrates why advertised matrix TOPS matter much more for compute-heavy GEMM than memory-bound decode.

## Claims to avoid

- “4-bit model = INT4 Tensor Core.”
- “FP8 always twice as fast as FP16.”
- “TOPS can be compared across precision modes without footnotes.”
- “FP16 input means FP16 accumulation.”
- “Quantization speedup proves native low-bit arithmetic.”
- “Tensor Core count alone predicts LLM tokens/s.”

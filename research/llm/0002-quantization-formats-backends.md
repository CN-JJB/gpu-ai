# Research Note 0002 — “4-bit 模型”到底是什么：Datatype、Quantization、Format 与 Backend

日期：2026-08-26

## Research question

当模型仓库写着 FP16、INT8、AWQ、GPTQ、GGUF、Q4_K_M、EXL2、bitsandbytes 时，这些词分别描述哪一层？

为什么“同样叫 4-bit”：
- 文件大小不同；
- 质量不同；
- GPU/CPU/Apple/AMD 支持不同；
- backend 能否加载不同；
- 实际速度也不同？

如何把这些变化很快的生态事实拆成稳定知识 + 动态兼容情报？

## Scope

本切片建立四层模型：

1. numerical datatype / execution precision
2. quantization algorithm / scheme
3. checkpoint/container/serialized representation
4. runtime/backend/kernel compatibility

不把 2026-08-26 的兼容矩阵写死进稳定 Lesson。当前 backend compatibility snapshot 放入 `intelligence/`，并明确带日期和来源。

## Primary sources

1. Hugging Face Transformers — Quantization overview  
   https://huggingface.co/docs/transformers/quantization/overview  
   quantization 降低 model memory / compute cost；full/half precision 与 int8/int4 是不同 numerical representations；不同 quantization methods 的 hardware/support matrix 不同。

2. Hugging Face Transformers — Quantization API  
   https://huggingface.co/docs/transformers/main_classes/quantization  
   Transformers 将 AWQ、GPTQ、bitsandbytes 等作为不同 quantization integrations；weight dtype 与 activation dtype 可以不同；W4A16 是 weights/activations 两个维度的 scheme。

3. GPTQ paper  
   https://arxiv.org/abs/2210.17323  
   GPTQ 是 post-training weight quantization 方法，核心是怎样选择低-bit weight representation 以控制误差，而不是文件容器。

4. AWQ paper  
   https://arxiv.org/abs/2306.00978  
   AWQ 是 activation-aware weight-only quantization 方法，利用 activation statistics 识别重要 channels。

5. Hugging Face Transformers — AWQ  
   https://huggingface.co/docs/transformers/quantization/awq  
   AWQ model 可通过 quantization metadata 被 loader 识别；runtime 仍需对应 integration。

6. Hugging Face Safetensors — Metadata parsing  
   https://huggingface.co/docs/safetensors/metadata_parsing  
   safetensors 是 tensor serialization/container；header 记录 dtype、shape、data offsets；container 本身不等于某种 quantization algorithm。

7. llama.cpp — GGUF implementation  
   https://github.com/ggml-org/llama.cpp/blob/master/ggml/include/gguf.h  
   GGUF 包含 metadata key/value、tensor name/shape、per-tensor ggml type 与 aligned data blob。因此 GGUF 是 container/metadata format，也可承载量化 tensor。

8. llama.cpp — models / quantize  
   https://github.com/ggml-org/llama.cpp/blob/master/docs/models.md  
   https://github.com/ggml-org/llama.cpp/blob/master/tools/quantize/quantize.cpp  
   llama.cpp 运行模型要求 GGUF；source model 可转换再量化；quantized artifact 可以使用不同 tensor types，而非每个 tensor 都完全相同。

9. llama.cpp — backend support  
   https://github.com/ggml-org/llama.cpp/blob/master/README.md  
   current upstream 列出 Metal/Apple Silicon、CUDA/NVIDIA、HIP/AMD 等 backends。GGUF 能在哪种硬件上跑来自 runtime backend/kernel，而不是文件名本身。

10. ExLlamaV2 — EXL2  
    https://github.com/turboderp-org/exllamav2  
    EXL2 是 ExLlamaV2 ecosystem 的 low-bit representation；支持 2–8 bit 范围，并可混合不同 quantization levels 去满足 target average bitrate。

11. Hugging Face TGI — Quantization  
    https://huggingface.co/docs/text-generation-inference/conceptual/quantization  
    GPTQ/AWQ/EXL2 等可以是 pre-quantized weights；bitsandbytes 等也可以 on-the-fly quantize。

12. vLLM — Quantization  
    https://docs.vllm.ai/en/latest/features/quantization/  
    quantization support 是 backend + hardware + implementation 的矩阵；current docs 明确提示 compatibility 会继续变化。

13. vLLM — GGUF  
    https://docs.vllm.ai/en/latest/features/quantization/gguf/  
    current vLLM GGUF support 标为 experimental / under-optimized，并通过 out-of-tree plugin 提供。

## Findings

### F1 — “4-bit”至少可能描述三件不同的事

用户说“4-bit 模型”，可能指：

1. tensor value 的 nominal weight code width；
2. 整个 checkpoint 的 average/effective bpw；
3. 某 runtime 使用的 low-bit compute/storage path。

这三者不能互换。

### F2 — Datatype/precision 描述“数怎么表示/算”

例如 FP32、FP16、BF16、FP8、INT8、INT4-like packed representation。

现代 inference 可以 mixed precision。W4A16 通常表达：
- weights 低 bit；
- activations 仍 16-bit。

accumulator 也可能是另一种 precision。因此“4-bit model”不代表所有 arithmetic 都在 4-bit 完成。

### F3 — Quantization algorithm 描述“怎样从高精度权重得到低精度表示”

GPTQ、AWQ、RTN 等解决：
- scale / quantization grid 如何选；
- 哪些 weight/channel 更重要；
- 是否需要 calibration；
- 如何控制 quantization error。

这和最终用什么 file container 是两个问题。

### F4 — Container/serialization 描述“文件怎么组织”

**Safetensors**
- tensor header + dtype + shape + offsets；
- 可承载不同 tensor dtypes；
- 本身不等于 GPTQ/AWQ/FP16。

**GGUF**
- metadata + tensor descriptors + per-tensor ggml type + data blob；
- 可以承载 F16/F32 与多种 quantized ggml tensor types；
- “GGUF”本身不告诉你文件到底 Q4、Q5 还是 F16。

所以：`container != quantization level`。

### F5 — 有些生态名词跨越多个层

例如 EXL2：
- 是 ExLlamaV2 的 quantized model representation/format；
- 与其 loader/kernel ecosystem 强耦合；
- 支持 mixed bitrate。

四层模型是调查工具，不是说所有项目名都严格只属于一层。正确做法是继续问：它描述的是算法、serialized representation、kernel layout、loader contract，还是几个层一起？

### F6 — Effective bpw 来自 metadata + exceptions，不只是 nominal bits

最简 group quantization 教学模型：

每 G 个 weights：
- G × q bits 的 codes
- 一个 s-bit scale
- 可选 z-bit zero point

则 quantized region：

```text
effective_bpw ≈ q + (s + z) / G
```

例如 q=4、FP16 scale、没有 zero：
- group 32 → 4.5 bpw
- group 64 → 4.25 bpw
- group 128 → 4.125 bpw

即使所有权重都有“4-bit code”，overall bpw 也不是 4。

### F7 — 少量未量化 tensor 会继续抬高 whole-model bpw

若：
- 95% parameters 使用 group64 4-bit + FP16 scale → 4.25 bpw
- 5% parameters 保持 FP16 → 16 bpw

overall：
```text
0.95 × 4.25 + 0.05 × 16 = 4.8375 bpw
```

这就是上一切片为什么使用 `effective_bpw`。

### F8 — Real quant formats 比教学公式复杂很多

现实还可能有 per-channel/per-group scales、asymmetric zero-points、double quantization、codebooks、importance matrices、mixed bits、tensor-specific quant types、padding/alignment、special output/embedding tensors 与 backend repacking。

所以 L0 公式只解释“为什么 nominal bits != effective bpw”。

### F9 — Backend compatibility 是单独一层

一个 artifact 只有在 runtime 具备 parser/loader、operator implementation、target hardware kernel、required datatype/instruction support 与 tested integration 时，才算“可用”。

```text
file exists
!= backend can load
!= backend runs correctly
!= backend runs efficiently
```

### F10 — 同名 quantization 在不同 backend 上兼容性可以不同

2026-08-26 的官方文档就是现成反例：Hugging Face Transformers quantization overview 与 vLLM quantization matrix 对某些 methods/platforms 给出的支持状态并不相同。

这不是谁“错了”，而是两个 backend/integration 不是同一个软件栈。易变事实进入 dynamic intelligence snapshot。

### F11 — GGUF 也不是“到处都一样快”

llama.cpp 把 GGUF 作为原生模型 format，并为 CUDA/HIP/Metal 等提供 kernels。

vLLM current docs 也有 GGUF path，但标记 experimental / under-optimized，并迁移到 plugin。

```text
same container + different runtime
= different maturity/performance/features
```

### F12 — Apple 特别适合证明 format/backend 分层

llama.cpp current upstream 把 Apple Silicon / Metal 列为 backend。

一个 GGUF quant 在 Metal 上运行，不是因为“GGUF 是 Apple 格式”，而是：
```text
GGUF parser
+ ggml tensor types
+ llama.cpp Metal kernels
+ Apple GPU backend
```

NVIDIA/AMD 同理。

### F13 — 选择 quantization 不应该从“几 bit”开始

更好的调查顺序：

1. target backend 是什么？
2. target hardware 是什么？
3. backend current version 支持哪些 representations/kernels？
4. model architecture 是否被支持？
5. capacity 需要压到多少？
6. target workload 是 decode/prefill/concurrency 哪种？
7. quality loss 可接受多少？
8. 再在满足约束的 quant options 中比较 effective bpw / speed / quality。

## Stable four-layer model

```text
Numerical representation
    ↓
Quantization method / scheme
    ↓
Serialized checkpoint / container
    ↓
Runtime loader + kernel + hardware support
```

现实项目可能跨层，但调查时要逐层问清。

## Claims to avoid

- “GGUF 就是 4-bit。”
- “Safetensors 就是 FP16。”
- “AWQ 是一种文件后缀。”
- “GPTQ/AWQ 都是 4-bit，所以速度一样。”
- “W4A16 表示整个模型计算都是 INT4。”
- “某格式能加载就一定有高效 kernel。”
- “vLLM 支持某格式，所以 llama.cpp 也一定支持。”
- “NVIDIA 能跑的 quant 在 AMD/Apple 上一定能跑。”
- “4-bit 权重精确等于 4 bpw。”

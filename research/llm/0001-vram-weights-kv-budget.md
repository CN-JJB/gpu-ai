# Research Note 0001 — 本地 LLM 显存预算：Weights、KV Cache、Context 与 Concurrency

日期：2026-08-26

## Research question

在下载模型或购买 GPU 之前，怎样从模型参数量与 `config.json` 先做一个可解释的 VRAM baseline？

需要回答：

- 权重最低大约占多少空间？
- nominal 4-bit / 8-bit 为什么不等于真实 checkpoint 或 runtime 显存？
- KV cache 为什么随 context length 与 concurrency 增长？
- MHA / GQA / MQA 为什么会显著改变 KV cache？
- 为什么“权重刚好塞进去”仍然可能 OOM？
- paged/static/quantized/sliding-window KV cache、runtime buffers 与 offload 会怎样让实际值偏离公式？

## Scope

本切片只建立 **capacity budgeting baseline**。

不把某个 GGUF/AWQ/GPTQ/EXL2 格式的实际 bits-per-weight、某推理后端的 allocator 行为或当前模型文件大小写成稳定规则；这些进入后续 quantization/backend slice 与 dynamic intelligence。

默认讨论 decoder-only Transformer inference。

## Primary sources

### 1. Hugging Face Transformers — Caching

https://huggingface.co/docs/transformers/en/cache_explanation

支撑：

- autoregressive generation 一次预测一个 token；
- KV cache 保存之前 tokens 的 key/value，避免每一步重新计算全部过去 K/V；
- cache 是逐层保存；
- basic key/value cache tensor shape 为
  `[batch_size, num_heads, seq_len, head_dim]`；
- DynamicCache 的 sequence dimension 随新 token 增长。

### 2. Hugging Face Transformers — Cache strategies

https://huggingface.co/docs/transformers/en/kv_cache

支撑：

- Dynamic Cache 随 sequence 增长；
- Static Cache 会预分配更大的固定空间；
- Quantized Cache 用较低 cache memory；
- sliding-window/chunked-attention layers 的 cache 可在窗口/块达到上限后停止增长；
- cache implementation 会影响真实 memory usage。

### 3. Hugging Face Transformers — LlamaConfig

https://huggingface.co/docs/transformers/model_doc/llama

支撑：

- `num_hidden_layers`
- `num_attention_heads`
- `num_key_value_heads`
- `head_dim`

官方定义：

- `num_key_value_heads == num_attention_heads` → MHA；
- `num_key_value_heads == 1` → MQA；
- 中间值 → GQA；
- `head_dim` 未显式给出时，LlamaConfig 默认 `hidden_size // num_attention_heads`。

### 4. Hugging Face Safetensors — Metadata parsing

https://huggingface.co/docs/safetensors/metadata_parsing

支撑：

- safetensors header 可提供 tensor dtype、shape、data offsets；
- 可以只解析 metadata 来统计不同 dtype 的参数数量；
- 实际 checkpoint 可能是 mixed dtype，也可能分 shard；
- “模型有 N 参数”并不足以推出一个精确文件大小。

### 5. NVIDIA TensorRT-LLM — Memory Usage

https://nvidia.github.io/TensorRT-LLM/reference/memory.html

支撑：

inference GPU memory 的主要类别包括：

- weights；
- internal activation tensors；
- I/O tensors，其中 KV cache 是主要 footprint 之一；
- runtime/decoder buffers。

TensorRT-LLM 的 weights memory 还会依赖 precision 与 parallelization。

其 C++ runtime 会维护 paged KV cache pool；实际 cache allocation 可以由 free-memory fraction / token budget 等 runtime 策略决定，而不只是“当前 token 数 × 一个公式”。

### 6. NVIDIA TensorRT-LLM — KV cache system

https://nvidia.github.io/TensorRT-LLM/features/kvcache.html

支撑：

- KV cache 由 block pool 管理；
- 支持 MHA/MQA/GQA；
- cache dtype 可配置；
- paged KV allocation、window 等会影响 runtime footprint。

### 7. AMD ROCm Infera — PD disaggregation / KV cache

https://rocm.docs.amd.com/projects/infera/en/main/features/pd_disaggregation.html

https://rocm.docs.amd.com/projects/infera/en/latest/

支撑：

- prefill 构建 KV；
- decode 消费并继续增长/使用 KV；
- KV 可以在 GPU 之间传输；
- AMD inference serving 同样需要把 KV cache 当成独立的容量与数据移动对象；
- Infera 还提供 GPU→RAM/NVMe/network 的 KV offload/tiering。

## Findings

### F1 — 第一层权重预算只有一个非常简单的下界

若：

- parameter count = P
- effective storage = b bits / parameter

则：

```text
weight_bytes_baseline = P × b / 8
```

例如 7B parameters：

- 16 bit → 14,000,000,000 bytes ≈ 13.04 GiB
- 8 bit → 7,000,000,000 bytes ≈ 6.52 GiB
- 4 bit → 3,500,000,000 bytes ≈ 3.26 GiB

但这是 **parameter payload baseline**，不是“真实运行必占”。

### F2 — Nominal bits-per-weight 不是 effective bits-per-weight

真实量化格式可能额外保存：

- per-group scales；
- zero points；
- codebooks；
- packing/alignment；
- tensor metadata；
- 某些未量化 tensors；
- embeddings / output head 的不同 dtype；
- backend-specific converted weights。

因此一个“4-bit model”的 effective bpw 可以高于 4。

课程使用 `effective_bits_per_weight` 作为预算输入，而不是把 label 当真实大小。

### F3 — File size、weight payload 与 VRAM allocation 是三个不同数字

**Checkpoint file size**
- serialization metadata；
- shards；
- dtype packing；
- format headers；
- optional extra tensors。

**Weight payload baseline**
- 参数 × effective bpw。

**Runtime VRAM**
- weights 的 backend layout；
- alignment / converted kernels；
- activations；
- KV；
- allocator workspace；
- graph/capture buffers；
- temporary scratch；
- backend preallocation。

所以：
`download size != weight payload != runtime VRAM`。

### F4 — KV baseline 可以从 attention config 推出来

Hugging Face 的基本 cache shape：

```text
K: [batch, kv_heads, sequence, head_dim]
V: [batch, kv_heads, sequence, head_dim]
```

对一个标准 attention layer：

```text
KV bytes
= 2
× batch
× sequence
× num_kv_heads
× head_dim
× bytes_per_cache_element
```

若所有 L layers 都缓存：

```text
KV_total
= 2
× layers
× batch
× sequence
× num_kv_heads
× head_dim
× bytes_per_element
```

于是每 sequence、每新增一个 token 的 baseline：

```text
KV_bytes_per_token
= 2
× layers
× num_kv_heads
× head_dim
× bytes_per_element
```

这个公式是本切片最重要的可迁移工具。

### F5 — MHA/GQA/MQA 的 KV 差异来自 num_kv_heads

若 query heads = 32、head_dim = 128：

**MHA**
```text
num_kv_heads = 32
```

**GQA example**
```text
num_kv_heads = 8
```

**MQA**
```text
num_kv_heads = 1
```

在其他条件相同时，KV baseline 正比于 `num_kv_heads`。

所以 GQA/MQA 的一个系统价值就是显著降低 KV state footprint 与 traffic。

### F6 — 对普通 MHA，公式可以进一步简化

当：

```text
head_dim = hidden_size / num_attention_heads
num_kv_heads = num_attention_heads
```

则：

```text
num_kv_heads × head_dim = hidden_size
```

所以：

```text
MHA KV bytes/token
= 2 × layers × hidden_size × bytes_per_element
```

而 GQA 相对 MHA 大约再乘：

```text
num_kv_heads / num_attention_heads
```

前提是各层配置一致。

### F7 — Context length 与 concurrency 都是线性乘数

对普通 full-attention DynamicCache baseline：

```text
KV total ∝ context tokens × active sequences
```

所以“模型单用户 4K context 能跑”不代表：

- 32K context 能跑；
- 8 个并发 request 能跑；
- server 的 max batch / max seq 配置能跑。

### F8 — 一个 7B-like 抽象 GQA 例子可以把数量级讲清

不是某个真实 checkpoint，只取：

- 7B parameters
- effective weight bpw = 4.5
- 32 layers
- 32 query heads
- 8 KV heads
- head_dim = 128
- KV dtype = 16 bit

权重 baseline：

```text
7e9 × 4.5 / 8
≈ 3.667 GiB
```

KV：

```text
2 × 32 × 8 × 128 × 2 bytes
= 131072 bytes/token
= 128 KiB/token/sequence
```

4K context：

```text
128 KiB × 4096
= 512 MiB / sequence
```

4 concurrent sequences：

```text
2 GiB KV
```

如果另留 1.5 GiB runtime reserve：

```text
3.667 GiB weights
+ 2 GiB KV
+ 1.5 GiB reserve
= 7.167 GiB
```

这已经非常接近 8 GiB 卡的容量边缘。

而 concurrency=8：

```text
3.667 + 4 + 1.5
= 9.167 GiB
```

baseline 已超过 8 GiB。

### F9 — 同一个抽象 attention config，MHA/GQA/MQA 的差距很大

32 layers、head_dim 128、FP16 KV、4096 tokens：

**MHA / 32 KV heads**
- 512 KiB/token
- 2 GiB / sequence

**GQA / 8 KV heads**
- 128 KiB/token
- 512 MiB / sequence

**MQA / 1 KV head**
- 16 KiB/token
- 64 MiB / sequence

这不是“GQA 一定更快”的完整论证，但足以说明：
attention architecture 会改变本地 LLM 的显存容量和 decode traffic。

### F10 — “max context”不一定意味着 KV 一直线性长到 max context

现代模型可能混合：

- full attention；
- sliding-window attention；
- chunked attention；
- heterogeneous per-layer attention config。

Hugging Face cache docs 明确指出 sliding-window/chunked layers 的 cache 可在窗口达到上限后停止增长。

因此对这些模型，不能把统一 full-attention 公式机械乘所有层。

### F11 — Static / paged cache 让“正在使用多少”与“已经预留多少”分开

Dynamic cache：
- 通常随已使用 sequence 增长。

Static cache：
- 可以按更大 max length 预分配；
- 当前只用 1K token，也可能保留接近 max setting 的 cache memory。

Paged cache：
- runtime 预先管理 block pool；
- request 按 block/token 使用；
- 还可能为 throughput 主动保留大量 free VRAM。

TensorRT-LLM 文档就是现实例子：runtime 可能把剩余 GPU memory 的大部分留给 KV pool。

因此：
**理论 KV used bytes != runtime KV pool reserved bytes**。

### F12 — Headroom 必须是一等公民

若预算结果：

```text
estimated_total = 7.9 GiB
GPU = 8 GiB
```

不能输出“能跑”。

还存在：

- runtime workspace；
- temporary activations；
- allocator fragmentation；
- CUDA/ROCm context；
- display/desktop usage；
- backend graph capture；
- quant metadata；
- model conversion；
- other processes。

课程 calculator 必须输出 headroom，而不是只有 fit/no-fit。

### F13 — Offload 解决 capacity，不免费解决 performance

weights 或 KV 可放到：

- host RAM；
- NVMe；
- remote node；
- another GPU。

它能把“完全放不下”变成“可以运行”。

但数据跨：

- PCIe；
- interconnect；
- network；
- SSD

都会形成新的 bandwidth/latency roof。

这正好连接上一片 Roofline。

## Stable capacity model

```text
VRAM estimate
≈ weight payload
+ KV cache
+ runtime reserve
```

其中：

```text
weight payload
≈ params × effective_bpw / 8
```

```text
KV
≈ 2
× layers
× active_sequences
× cached_tokens
× kv_heads
× head_dim
× cache_bytes_per_element
```

最后必须加：

```text
headroom = VRAM capacity - estimated total
```

并注明：
这是 preflight estimate，不是 runtime guarantee。

## Investigation workflow for a real model

1. 读 model card。
2. 读 `config.json`。
3. 记录：
   - layers
   - hidden_size
   - attention heads
   - KV heads
   - head_dim
   - max position / sliding-window settings
4. 从 safetensors metadata 或官方仓库 metadata 确认：
   - parameter count
   - dtype mix
5. 确认下载的是哪种量化/转换格式。
6. 查目标 backend：
   - weight layout
   - KV dtype
   - paged/static policy
   - graph/workspace reservation
   - offload
7. 先计算 baseline。
8. 再用真实 runtime measurement 验证。

## Claims to avoid

- “7B FP16 就一定占 14 GB VRAM。”
- “4-bit 就精确等于 0.5 byte/parameter。”
- “模型文件 5 GB 就只需要 5 GB 显存。”
- “context 翻倍只影响速度，不影响显存。”
- “GQA/MQA 只影响算法，不影响 KV memory。”
- “KV cache 只有生成 token 才占，prompt 不占。”
- “算出来 7.9 GiB，所以 8 GiB 卡一定能跑。”
- “offload 只是把容量加起来，性能完全不受影响。”

# Research Note 0008 — Attention 的 IO 问题、Online Softmax 与 FlashAttention

日期：2026-08-27

## Research question

为什么标准 dense attention 的数学式看起来只有两次矩阵乘：

```
S = QK^T / sqrt(d)
P = softmax(S)
O = PV
```

但长上下文时，真正拖慢 GPU 的不只是 FLOPs，还包括：

- `S` / `P` 这类 N×N 中间结果；
- HBM ↔ on-chip SRAM/shared-memory 的往返；
- softmax 的逐行归约与数值稳定；
- thread-block / warp 的工作划分？

本切片建立：

```
attention math
→ naive materialization
→ HBM traffic
→ tiling
→ online softmax
→ fused IO-aware attention
→ GPU work partition
```

并把 Slice 03 的 tiling/reuse、Slice 04 的 Roofline 与 LLM prefill 连接起来。

## Scope

Stable:
- exact dense scaled dot-product attention；
- quadratic score matrix；
- tiling；
- online stable softmax；
- IO-aware fusion；
- FlashAttention family 的核心思想；
- prefill vs decode 差异。

Dynamic:
- PyTorch/CUDA/cuDNN backend dispatch；
- exact hardware support；
- backend names/flags；
- FlashAttention version-specific kernels。

## Primary sources

### 1. FlashAttention paper

Tri Dao et al. — *FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness*

https://arxiv.org/abs/2205.14135

Paper's stable contribution:
- exact attention, not an approximation；
- explicitly models reads/writes between GPU HBM and on-chip SRAM；
- uses tiling to reduce HBM accesses；
- avoids materializing the full attention matrix in HBM；
- analyzes IO complexity.

Do not turn the paper's historical benchmark numbers into current GPU claims.

### 2. FlashAttention-2

Tri Dao — *FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning*

https://arxiv.org/abs/2307.08691

Stable contribution:
- fewer non-matmul FLOPs；
- more parallelism across thread blocks, including within one head；
- improved work partition across warps；
- less shared-memory communication.

This directly connects the algorithm to the GPU execution model from Slice 02/03.

### 3. NVIDIA Transformer Engine attention docs

https://docs.nvidia.com/deeplearning/transformer-engine/user-guide/examples/attention/attention.html

Current NVIDIA docs explain the flash family in terms of:
- tiling based on shared memory/register constraints；
- avoiding large global-memory intermediates；
- recomputation tradeoff in backward.

Useful cross-check:
```
extra compute can be worth it
if it saves expensive memory traffic
```

### 4. PyTorch scaled_dot_product_attention

https://docs.pytorch.org/docs/main/generated/torch.nn.functional.scaled_dot_product_attention.html

Current PyTorch docs expose optimized CUDA implementations and backend selection. These are implementation intelligence, not stable algorithm semantics.

## Findings

### F1 — Dense attention compute is still quadratic

For sequence length N and head dimension d:

```
QK^T: O(N^2 d)
PV:   O(N^2 d_v)
```

FlashAttention does **not** magically turn exact dense attention into subquadratic compute.

Its main stable win is:

```
same mathematical attention
with much less expensive memory IO / intermediate materialization
```

### F2 — Naive materialization creates an N×N memory problem

A straightforward implementation may conceptually form:

```
S = QK^T
P = softmax(S)
```

Each is N×N per head.

If fp16/bf16-like storage is 2 bytes/value:

```
one N×N matrix bytes = N^2 × 2
```

At N=4096:
- one matrix = 32 MiB/head；
- two matrices = 64 MiB/head；
- across 32 heads = 2 GiB of quadratic intermediate footprint.

At N=8192:
- two matrices = 256 MiB/head；
- across 32 heads = 8 GiB.

This is a teaching materialization model. Real fused/non-fused frameworks may store different intermediates.

### F3 — HBM traffic can dominate even when FLOPs look large

Naive attention can repeatedly:
- write score/probability intermediates to HBM；
- read them back for softmax / `PV`；
- synchronize between kernels.

This lowers effective arithmetic intensity of the end-to-end attention operation.

The key Roofline extension:

```
more FLOPs is not automatically slower
if extra FLOPs eliminate much more HBM traffic
```

This explains why recomputation/fusion can win.

### F4 — Tiling changes where the intermediate lives

Instead of:

```
all QK scores
→ HBM
→ softmax
→ HBM
→ PV
```

IO-aware attention does:

```
Q tile + K/V tile
→ on-chip SRAM/shared memory/registers
→ local scores
→ online normalization
→ accumulate output
→ discard local score tile
```

The full N×N score/probability matrix never needs to exist in HBM.

### F5 — Ordinary softmax looks globally dependent

For one row:

```
softmax(x_i) = exp(x_i) / sum_j exp(x_j)
```

For numerical stability:

```
softmax(x_i)
= exp(x_i - m) / sum_j exp(x_j - m)

m = max_j x_j
```

At first glance, you need the max and sum across the whole row before producing normalized values.

This seems incompatible with small tiles.

### F6 — Online softmax makes blockwise processing exact

Maintain running row statistics:

```
m = running maximum
l = running exp-sum under that maximum
```

When a new score block arrives:

```
m_new = max(m_old, max(block))
l_new =
  exp(m_old - m_new) * l_old
  + sum(exp(block - m_new))
```

The previous contribution can be rescaled into the new normalization frame.

The output accumulator can be rescaled in the same way:

```
acc_new =
  exp(m_old - m_new) * acc_old
  + sum(exp(score - m_new) * V)
```

Finally:

```
O = acc / l
```

Therefore:
- tiles can be processed incrementally；
- numerical stability is preserved；
- no full attention row must be materialized.

### F7 — FlashAttention is fusion + tiling + online normalization, not one magic instruction

Stable mental model:

```
GEMM-like tiles
+ online softmax state
+ on-chip reuse
+ fused accumulation
+ careful scheduling
```

Hardware-specific implementations then map this onto:
- tensor/matrix units；
- registers；
- shared memory / SRAM；
- thread blocks；
- warps；
- async copy / specialized memory movement where supported.

### F8 — FlashAttention-2 shows algorithm and GPU scheduling are inseparable

The second paper identifies that even an IO-efficient algorithm can leave performance on the table because of:
- poor thread-block parallelism；
- warp partitioning；
- excess non-matmul work；
- unnecessary shared-memory traffic.

That connects directly to:
- Slice 02 latency hiding / occupancy；
- Slice 03 shared memory / bank / reuse；
- Slice 04 arithmetic intensity.

### F9 — Prefill and decode are different attention shapes

Prefill:
```
many query tokens × many key/value tokens
```

Large attention tiles and N×N structure make fused IO-aware attention especially relevant.

Decode:
```
usually one/few new query tokens
× long cached K/V history
```

The problem shifts strongly toward:
- reading KV cache；
- GQA/MQA；
- paged KV；
- decode-specific kernels.

Do not claim:
```
FlashAttention speedup in prefill
= same speedup in decode
```

### F10 — GQA/MQA and FlashAttention solve different traffic

GQA/MQA reduce how much K/V state exists and must be read.

FlashAttention-style algorithms reduce how attention computation moves/materializes intermediate data.

They can stack, but they are not substitutes.

### F11 — Exact dense attention still has long-context cost

Avoiding N×N intermediate storage does not remove the N² dot products for full dense prefill.

So long context still increases compute sharply.

Stable distinction:

```
quadratic compute
!=
quadratic materialized HBM memory
```

FlashAttention can make memory scaling much friendlier while compute remains quadratic.

## L0 experiment design

Two checks:

### A. Correctness

Implement:
- naive full attention；
- tiled online attention.

Use tiny deterministic Q/K/V.

Verify:

```
max_abs_error ≈ floating-point rounding only
```

### B. Materialization model

For sequence:
- 1024；
- 2048；
- 4096；
- 8192；
- 16384。

Show the footprint of one/two N×N fp16-like intermediate matrices, per head and across 32 heads.

This is not a FlashAttention memory benchmark; it isolates the quadratic intermediate the fused algorithm avoids materializing.

## Real experiment design

Optional PyTorch CUDA path:

Compare:
- SDPA math backend；
- FlashAttention backend when available；
- auto dispatch.

Record:
- exact PyTorch/CUDA/GPU；
- shape；
- dtype；
- causal；
- backend availability；
- latency；
- peak allocated memory.

Do not fabricate results; unsupported backend is valid Evidence.

## Claims to avoid

- “FlashAttention makes attention O(N).”
- “FlashAttention is approximate.”
- “FlashAttention is just Tensor Cores.”
- “It only saves VRAM, not bandwidth.”
- “It always speeds decode by the same amount.”
- “GQA and FlashAttention are the same optimization.”
- “Any fused attention kernel is literally the original FlashAttention implementation.”

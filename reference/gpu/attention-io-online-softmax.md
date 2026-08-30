# Attention IO / Online Softmax / FlashAttention 速查

<figure>
  <img src="../../assets/diagrams/attention-io-naive-vs-tiled.svg" alt="Attention IO / Online Softmax / FlashAttention 速查 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Attention IO / Online Softmax / FlashAttention 速查 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


## 数学不变

```
Attention(Q,K,V)
= softmax(QK^T / sqrt(d)) V
```

FlashAttention-style exact kernels改变的是：

```
data movement + materialization + scheduling
```

不是 attention 的目标数学结果。

## Naive problem

Conceptually:

```
QK^T
→ write N×N scores to HBM
→ softmax
→ write/read N×N probabilities
→ PV
```

Quadratic intermediate：

```
bytes ≈ matrices × N^2 × bytes_per_value
```

fp16-like, 2 matrices:

| N | per head | 32 heads |
|---:|---:|---:|
| 1024 | 4 MiB | 0.125 GiB |
| 2048 | 16 MiB | 0.5 GiB |
| 4096 | 64 MiB | 2 GiB |
| 8192 | 256 MiB | 8 GiB |
| 16384 | 1 GiB | 32 GiB |

These are conceptual materialized intermediates, not actual runtime peak-memory claims.

## IO-aware tiled path

```
load Q tile
for each K/V tile:
    compute score tile
    update online softmax stats
    update output accumulator
discard score tile
write final output
```

Full N×N probability matrix need not reach HBM.

## Online stable softmax state

Per row maintain：

```
m = running max
l = running exp sum
a = running weighted V accumulator
```

New block:

```
m' = max(m, max(s))

alpha = exp(m - m')

l' = alpha*l + sum(exp(s - m'))

a' = alpha*a + sum(exp(s - m') * V_block)
```

Final：

```
O = a / l
```

## Why recomputation/fusion can be faster

GPU memory hierarchy is asymmetric.

Sometimes：

```
extra arithmetic
<
saved HBM read/write cost
```

So fewer global-memory round trips can beat “compute once then store everything”.

## FlashAttention vs FlashAttention-2

FlashAttention:
- IO-aware tiling；
- online softmax；
- exact attention；
- fewer HBM accesses。

FlashAttention-2:
- better block-level parallelism；
- better warp work partition；
- fewer non-matmul FLOPs；
- less shared-memory communication。

## Prefill vs Decode

Prefill：
- many Q；
- large QK；
- strong relevance to tiled dense attention。

Decode：
- few Q；
- long KV history；
- often KV bandwidth / cache layout dominates。

Never infer decode speedup from prefill speedup.

## Related but different

GQA/MQA:
```
reduce KV heads / KV bytes
```

Paged KV:
```
manage KV allocation/reuse
```

FlashAttention:
```
reduce attention intermediate IO/materialization
```

Continuous batching:
```
increase active request utilization
```

Different layers of the system stack.

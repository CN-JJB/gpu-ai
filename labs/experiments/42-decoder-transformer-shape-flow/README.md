# Experiment 42 — Decoder Transformer Shape Flow

硬件等级：L0

## Goal

Use a tiny synthetic decoder config to make prefill/decode tensor shapes and KV growth concrete.

Default toy model:

```
B = 1
layers = 2
hidden d = 16
query heads Hq = 4
KV heads Hkv = 2
head_dim Dh = 4
FFN d_ff = 32
KV element bytes = 2
prompt T = 8
```

## Run

```bash
python3 simulate.py
```

## Expected concepts

### Prefill

```
X      [1,8,16]
Q      [1,4,8,4]
K/V    [1,2,8,4]
scores [1,4,8,8] conceptual
```

### Decode after prompt

New token:

```
X      [1,1,16]
Q      [1,4,1,4]
K/Vnew [1,2,1,4]
```

After append, cache length becomes 9:

```
K/V cache [1,2,9,4]
scores    [1,4,1,9] conceptual
```

## KV

Per token across all layers:

```
2 × 2 layers × 2 KV heads × 4 head_dim × 2 bytes
= 64 bytes/token
```

At 8-token prompt:

```
512 bytes
```

After one decode token:

```
576 bytes
```

Tiny numbers are intentional. The formula scales to real models.

## Important

The script reports conceptual score elements.

It does not claim a FlashAttention backend materializes those full score tensors.


## Why this experiment

Decoder-only Transformer 很容易被公式淹没。这个实验把它缩成极小 shape，让你能一眼看到 prefill 与 decode 的差别，以及 KV 为什么随 token 增长。

## Hypothesis

Prefill 一次处理 T 个 token，因此 Q/K/V 带 T 维；decode 只处理新 token，但 attention 仍要读取已有 KV cache，因此 score 长度随历史 context 增长。

## Fixed variables

B、layers、hidden、Hq/Hkv、head_dim、FFN、KV bytes 不变；只比较 prompt prefill 和 append 一个 decode token。

## What to observe

1. Prefill 的 X/Q/K/V shape。
2. Decode 时新 Q/K/V 只有 length=1。
3. cache length 从 8 → 9。
4. KV bytes/token 公式中每个因子的意义。
5. conceptual score matrix 与真实 FlashAttention materialization 的区别。

## Troubleshooting

- Hq 与 Hkv 不要混。
- KV 要同时计 K 和 V，所以有 ×2。
- per-token KV 还要乘 layers。
- score shape 只是数学概念，不代表 backend 一定把完整矩阵写入显存。

## Evidence to save

保存输出，并手工画一张 prefill/decode shape flow 图。

## What this proves

你能从 decoder config 推导核心 tensor shape 与 KV 增长。

## What this does NOT prove

它不代表真实 kernel、显存 allocator 或性能。

## No-hardware path

完整 L0。

## Transfer question

为什么 decode 每步 Q 只有一个 token，却仍会随着 context 变长而越来越依赖历史 KV？

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

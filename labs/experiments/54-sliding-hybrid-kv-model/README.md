# Experiment 54 — Full vs Sliding vs Hybrid KV Model

硬件等级：L0

## Default

```
layers = 32
full layers = 8
local layers = 24
window = 4096
Hkv = 8
Dh = 128
KV = FP16
```

Evaluate:
- context 32768
- context 131072

## Run

```bash
python3 compare.py
```

## Expected

At 32k:
- all full = 4 GiB
- all local = 0.5 GiB
- hybrid = 1.375 GiB

At 128k:
- all full = 16 GiB
- all local = 0.5 GiB
- hybrid = 4.375 GiB

The model also prints cached position-layer counts.

## Scope

This assumes:
- same Hkv/Dh in every layer;
- rolling local KV exactly W positions;
- no backend padding;
- no compressed KV.

It is a structural model, not runtime VRAM.


## Why this experiment

“128k context”不自动意味着每一层都保存 128k 的完整 KV。现代模型可能混合 full attention、sliding/local attention 或其他结构。本实验训练你按层算，而不是套一个统一公式。

## Hypothesis

当 context 远大于 local window 时，local 层 KV 会趋于固定，而 full 层仍随 context 线性增长；因此 hybrid KV 的增长斜率介于两者之间。

## Fixed variables

保持 layers、Hkv、Dh、KV dtype 和 window 不变，只比较 context 与 attention layout。

## What to observe

1. 32k → 128k 时 all-full 应约 4×。
2. all-local 在 context 超过 window 后基本不再随 context 增长。
3. hybrid 仍增长，因为其中 full layers 没有 window 截断。
4. 用 cached position-layer count 解释 GiB 数字，而不是只抄结果。

## Troubleshooting

- 先检查 full layers + local layers = total layers。
- 不要把 query heads 当 KV heads。
- window 小于 context 时 local cache 才被截断。
- 真实模型若有 per-layer 差异，必须逐层读取 config/实现。

## Evidence to save

保存两种 context 的输出，并画一张 context → KV 小表，分别列 full/local/hybrid。

## What this proves

你能从 attention layout 推导 KV 增长趋势。

## What this does NOT prove

它不等于 runtime VRAM；没有包括 allocator、padding、workspace、compressed/latent KV 等实现细节。

## No-hardware path

完整 L0 实验。

## Transfer question

如果 hybrid 模型只有 4 层 full attention、其余 28 层 local，context 再翻倍时，哪部分 KV 仍会继续线性增长？

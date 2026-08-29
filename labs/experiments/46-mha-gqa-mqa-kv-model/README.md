# Experiment 46 — MHA / GQA / MQA KV Cost Model

硬件等级：L0

## Default model

```
layers = 32
hidden = 4096
query heads = 32
head_dim = 128
KV bits = 16
context = 32768
```

Compare:
- MHA Hkv=32
- GQA Hkv=8
- MQA Hkv=1

## Run

```bash
python3 compare.py
```

## Expected

| type | KV/token | KV @ 32k |
|---|---:|---:|
| MHA | 512 KiB | 16 GiB |
| GQA-8 | 128 KiB | 4 GiB |
| MQA | 16 KiB | 0.5 GiB |

The script also prints rough Q/K/V/O projection parameter counts.

## Important

This is a homogeneous full-KV teaching model.

Architectures with:
- sliding attention;
- per-layer KV differences;
- latent attention;
- compressed KV;
- hybrid attention;

require a model-specific calculation.


## Why this experiment

MHA、GQA、MQA 的区别不仅是论文术语，它会直接改变 KV cache 的每 token 成本，从而影响 context 与 serving concurrency。

## Hypothesis

在 hidden size、query heads、layers、dtype、context 固定时，KV heads 越少，KV/token 越小；因此 GQA/MQA 的 KV budget 显著低于 MHA。

## Fixed variables

只改变 Hkv。layers、head_dim、context、KV bits 全部保持不变。

## What to observe

1. MHA → GQA-8 → MQA 的 KV/token 比例。
2. KV@32k 是否与 Hkv 线性缩放。
3. Q projection 参数为何不随 Hkv 同比例下降，而 K/V projection 会变化。
4. 为什么这会影响多用户 serving 的显存压力。

## Troubleshooting

- query heads 不等于 KV heads。
- head_dim 应与 hidden/query_heads 一致。
- 真实模型若使用 sliding/hybrid/latent attention，不能直接套 homogeneous full-KV 结果。

## Evidence to save

保存 compare.py 输出，并自己推导一次 KV/token 公式，写出每个因子的单位。

## What this proves

你能从 Hkv 推导 full-attention KV cache 的结构成本。

## What this does NOT prove

它不证明真实 runtime VRAM 或性能；没有包含 allocator、padding、KV quant、windowed/latent cache。

## No-hardware path

完整 L0 实验。

## Transfer question

两个 7B 模型参数量接近，一个 Hkv=32、一个 Hkv=8，为什么长 context 下显存需求可能差很多？

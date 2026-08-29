# Experiment 49 — Compare Real Dense Model FFN / Attention Structure

硬件等级：L0

## Goal

Compare downloaded Hugging Face-style `config.json` files using:
- hidden size;
- intermediate size;
- Hq/Hkv/head_dim;
- dense gated-FFN weight baseline;
- attention projection baseline;
- FFN/attention ratio;
- effective weight-storage proxy.

## Run

```bash
python3 compare_configs.py \
  model-a/config.json \
  model-b/config.json \
  --weight-bits 4.5
```

## Why this matters

Two models with similar total parameter count can allocate their weights differently between:
- attention;
- FFN;
- embeddings;
- experts/other modules.

That changes:
- quantization impact;
- weight traffic;
- kernel shapes.

## Warning

If the config exposes MoE/expert fields, the script marks:

```
MOE-CAVEAT
```

and does not treat `3*d*d_ff` as the full model's FFN parameter count.

MoE is the next slice.


## Why this experiment

总参数量相近，不代表权重都分布在同样的模块里。Dense 模型里，FFN 往往占据大量权重和内存流量；attention 与 FFN 的结构比例会影响量化、kernel shape 和 decode/prefill 行为。

## Hypothesis

两个真实 config 即使总参数量接近，只要 intermediate size、Hq/Hkv 或层数不同，FFN/attention weight baseline 和 storage proxy 就会不同。

## Fixed variables

比较时固定 weight-bits。只让真实 config 里的结构字段变化。

## What to observe

1. hidden、intermediate、layers 的差异。
2. 每层 FFN baseline 与 attention projection baseline。
3. FFN/attention ratio。
4. weight-bits 改变时 storage proxy 如何变化。
5. MOE-CAVEAT 出现时为什么不能继续用 dense 总量逻辑。

## Troubleshooting

- intermediate size 缺失时不要猜。
- MoE config 不能用 3*d*d_ff 当完整 FFN 参数量。
- storage proxy 不等于 runtime VRAM；还有 embedding、norm、workspace 等。

## Evidence to save

保存两个原始 config、来源/revision、命令、输出，并写一句“哪一项结构差异最可能改变 weight traffic”。

## What this proves

你能从真实 config 比较 dense FFN/attention 结构，而不是只看总参数量标签。

## What this does NOT prove

它不证明真实 TG、PP、质量或 kernel efficiency。

## No-hardware path

完整 L0，只需要 config 文件。

## Transfer question

两个 8B 模型中，一个 intermediate size 明显更大，你为什么会预期它在 FFN 权重流量和量化收益上与另一个不同？

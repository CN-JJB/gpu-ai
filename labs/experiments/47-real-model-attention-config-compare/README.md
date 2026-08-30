# Experiment 47 — Compare Real Model Attention Configs

硬件等级：L0

<figure>
  <img src="../../../assets/diagrams/mha-gqa-mqa.svg" alt="真实 attention config 比较要从 query heads 与 KV heads 的关系解释容量差异，而不是只比较模型参数量。">
  <figcaption>真实 attention config 比较要从 query heads 与 KV heads 的关系解释容量差异，而不是只比较模型参数量。</figcaption>
</figure>

## Goal

Compare real downloaded Hugging Face-style `config.json` files by:
- layers;
- Hq;
- Hkv;
- head_dim;
- head grouping;
- KV bytes/token;
- KV total at one chosen context.

## Run

```bash
python3 compare_configs.py \
  model-a/config.json \
  model-b/config.json \
  --context 32768 \
  --kv-bits 16
```

## Why this matters

Two models can both be called:
```
8B
```

yet have different:
- layers;
- Hkv;
- head_dim;
- context KV cost.

This tool compares architecture, not quality.

## Warnings

If a config contains:
- sliding window;
- MoE;
- layer types;
- unusual attention;
- missing head dimensions;

the output marks caveats.

Do not interpret the table as a complete runtime-memory predictor.


## Why this experiment

同为“8B”的模型，attention 结构可能完全不同。这个实验用真实下载的 config.json，让你从 marketing-size 走向结构化硬件推理。

## Hypothesis

如果两个模型 layers/Hkv/head_dim 不同，在相同 context 与 KV dtype 下，它们的 KV bytes/token 和总 KV 会不同，即使总参数量标签相近。

## Fixed variables

比较时固定 context 和 kv-bits。只让 config.json 中真实 architecture fields 不同。

## What to observe

1. Hq、Hkv、head_dim 和 grouping。
2. KV bytes/token 的来源。
3. 选定 context 下的 KV total。
4. 工具标出的 caveats 是否说明 homogeneous full-attention 公式不完整。

## Troubleshooting

- 缺字段时保留 UNKNOWN，不要人为补默认值。
- 如果有 sliding window / layer types / unusual attention，不要强行用一条公式覆盖全部层。
- config 是 architecture evidence，不是 runtime memory telemetry。

## Evidence to save

保存两个原始 config、文件来源/revision、命令和输出表，并写出“哪一个字段造成最大 KV 差异”。

## What this proves

你能从真实模型配置比较 attention/KV 结构。

## What this does NOT prove

它不比较模型质量，也不证明 runtime VRAM、PP/TG 或 backend compatibility。

## No-hardware path

只需要真实 config 文件，不需要 GPU。

## Transfer question

如果模型 B 的 Hkv 更少但有大量 full-attention layers，而模型 A 使用 hybrid sliding attention，为什么仅比较 Hkv 仍然可能得出错误 KV 结论？

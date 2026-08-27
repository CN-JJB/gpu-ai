# Experiment 47 — Compare Real Model Attention Configs

硬件等级：L0

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

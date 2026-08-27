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

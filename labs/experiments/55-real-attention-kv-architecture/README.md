# Experiment 55 — Inspect Real Attention/KV Architecture

硬件等级：L0

## Goal

Inspect a real `config.json` for evidence that the homogeneous full-attention KV formula may be incomplete.

The tool checks common fields for:
- sliding window;
- explicit layer types;
- Hq/Hkv/Dh;
- DeepSeek-style MLA dimensions.

## Run

```bash
python3 inspect_attention.py config.json --context 32768 --kv-bits 16
```

Optional:

```bash
--assume-all-sliding
```

Only use that flag after architecture documentation confirms every attention layer uses the configured sliding window.

Optional DeepSeek-family proxy:

```bash
--deepseek-mla-proxy
```

Only use after confirming the model uses the matching MLA cache formulation.

## Principle

The tool prefers:

```
UNKNOWN
```

over silently applying the wrong formula.

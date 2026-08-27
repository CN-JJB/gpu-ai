# Experiment 51 — Inspect a Real MoE config.json

硬件等级：L0

## Goal

Inspect a real Hugging Face-style MoE config and separate:

- routed expert count;
- top-k;
- shared experts;
- hidden size;
- expert intermediate size;
- per-expert dense weight baseline;
- total routed expert storage/layer;
- active routed expert storage/token/layer;
- architecture caveats.

## Run

```bash
python3 inspect_moe_config.py /path/to/config.json --weight-bits 4.5
```

## Supported common field aliases

The script recognizes common names such as:

Routed experts:
- `num_local_experts`
- `n_routed_experts`
- `num_experts`

Top-k:
- `num_experts_per_tok`
- `num_selected_experts`

Expert FFN:
- `moe_intermediate_size`
- fallback `intermediate_size`

Shared experts:
- `n_shared_experts`
- `num_shared_experts`

## Important

Field aliases do not make architectures identical.

If the config exposes:
- shared expert width;
- dense-first layers;
- MoE frequency;
- expert-specific projection structure;
- unusual routing;

read the model implementation/paper before extrapolating full-model totals.

The script intentionally reports per-layer baselines first.

# Experiment 43 — Inspect a Real Model config.json

硬件等级：L0

## Goal

Take a real Hugging Face-style `config.json` and turn model architecture fields into local-inference consequences.

## Run

```bash
python3 inspect_model_config.py /path/to/config.json
```

Optional KV context estimate:

```bash
python3 inspect_model_config.py config.json \
  --context 32768 \
  --kv-bits 16 \
  --sequences 1
```

## Script reads common fields

- model_type
- architectures
- vocab_size
- hidden_size
- intermediate_size
- num_hidden_layers
- num_attention_heads
- num_key_value_heads
- head_dim
- hidden_act
- rms_norm_eps
- rope_theta
- rope_scaling
- max_position_embeddings
- sliding_window
- tie_word_embeddings

It also looks for common MoE/expert fields and warns instead of pretending the dense baseline applies.

## Interpretation

The goal is not to support every config schema perfectly.

The goal is to turn:

```
"this is a 14B model"
```

into:

```
layers
hidden size
Q heads
KV heads
head dim
FFN size
position/norm/activation features
→ shapes
→ KV
→ likely kernel needs
```

## No model download required

You may use any already downloaded config.

Do not hardcode one model URL into the course.

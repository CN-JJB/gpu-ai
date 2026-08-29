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


## Why this experiment

模型名和参数量只是入口。真正做本地部署时，你需要从 config.json 读出层数、hidden、heads、FFN、位置编码和特殊结构，才能形成内存与 kernel 假设。

## Hypothesis

同一个“14B”标签无法唯一决定 KV、FFN shape 或长上下文行为；config fields 才能给出更具体的结构证据。

## Fixed variables

一次只检查一个 exact config/revision。可选 context/KV 参数必须显式记录。

## What to observe

1. hidden/layers/intermediate。
2. Hq/Hkv/head_dim。
3. RMSNorm、RoPE、activation 等结构字段。
4. sliding window / MoE caveat。
5. context 输入如何转换成 KV proxy。

## Troubleshooting

- config schema 不统一，缺失字段时保留 UNKNOWN。
- head_dim 可能显式给出，也可能由 hidden/Hq 推导；要记录来源。
- max_position_embeddings 不等于 runtime 一定能高质量使用全部 context。
- config facts 不等于 backend support。

## Evidence to save

保存原始 config、来源/revision、命令和输出摘要。

## What this proves

你会把真实 config 转成结构化本地推理问题。

## What this does NOT prove

它不证明模型质量、真实 VRAM、速度或兼容性。

## No-hardware path

完整 L0。

## Transfer question

两个模型都写 32k max position，但一个有 sliding_window、一个全局 attention，你为什么不能假设它们 KV 增长相同？

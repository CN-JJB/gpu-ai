# Learning / Build Record — 2026-08-27 MHA / MQA / GQA

## Slice

26 — Query heads vs KV heads, MHA/MQA/GQA, projection widths and KV/decode consequences.

## Production output

Research:
- `research/llm/0009-mha-mqa-gqa.md`

Reference:
- `reference/llm/mha-mqa-gqa-kv.md`

Lesson:
- `lessons/26-attention-heads/01-mha-mqa-gqa.html`

Labs:
- `labs/experiments/46-mha-gqa-mqa-kv-model/`
- `labs/experiments/47-real-model-attention-config-compare/`

Evidence:
- `examples/evidence/experiment-26-mha-mqa-gqa.md`

## Verified L0 result

For the default 32-layer / 32-Q-head / Dh128 example:
- MHA 32k FP16 KV = 16 GiB;
- GQA-8 = 4 GiB;
- MQA = 0.5 GiB.

Projection-count arithmetic also verified.

## Stable skill

Learner can now inspect:
```
num_attention_heads
num_key_value_heads
head_dim
layers
```

and calculate long-context/concurrency KV cost without relying on model-size labels.

## Next

SwiGLU / FFN:
- why the MLP can dominate dense model parameters;
- gate/up/down matrices;
- activation/gating;
- prefill vs decode matrix shapes;
- quantization/weight-streaming implications.

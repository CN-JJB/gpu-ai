# Learning / Build Record — 2026-08-27 Decoder-only Transformer Dataflow

## Slice

24 — Decoder-only Transformer anatomy: token → block → logits, with prefill/decode tensor shapes.

## Production output

Research:
- `research/llm/0007-decoder-only-transformer-dataflow.md`

Reference:
- `reference/llm/decoder-only-block-shapes.md`

Lesson:
- `lessons/24-transformer-anatomy/01-decoder-only-prefill-decode.html`

Labs:
- `labs/experiments/42-decoder-transformer-shape-flow/`
- `labs/experiments/43-real-model-config-anatomy/`

Evidence:
- `examples/evidence/experiment-24-decoder-transformer-dataflow.md`

## Stable skill

Learner can translate model config fields into:

```
tensor shapes
→ KV size
→ PP/TG workload character
→ likely hardware bottleneck
```

## L0 result

Experiment 42 default arithmetic verified:
- score elements 256 prefill / 36 one-token decode after append;
- KV 64 bytes/token;
- 512 → 576 bytes as sequence grows 8 → 9;
- attention/MLP toy parameter baselines verified.

## Real path

Experiment 43 uses a real `config.json` and flags architecture features that invalidate the homogeneous baseline.

## Next

Split modern decoder block mechanisms:

1. RMSNorm + pre-norm residual path;
2. RoPE position rotation;
3. MHA/MQA/GQA and KV consequences;
4. SwiGLU/FFN;
5. MoE.

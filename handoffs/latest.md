# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–25 are implemented.

Latest model-architecture sequence:

### Slice 24
Decoder-only dataflow:
```
prefill [B,T,d]
vs
decode [B,1,d] + KV
```

### Slice 25
```
RMSNorm
→ pre-norm residual
→ RoPE Q/K rotations
→ position-aware KV identity
```

Key files:
- `research/llm/0008-rmsnorm-residual-rope.md`
- `reference/llm/rmsnorm-residual-rope.md`
- `lessons/25-rmsnorm-rope/`
- `labs/experiments/44-rmsnorm-scale-model/`
- `labs/experiments/45-rope-relative-position-model/`

Verified:
- RMSNorm does not force zero mean;
- positive rescaling produces near-identical normalized vector;
- base RoPE common shift preserves relative-position dot relation;
- rotation preserves vector norm.

## Active next slice — MHA / MQA / GQA

Build:

```
Hq query heads
vs
Hkv key/value heads
→ Q/K/V projection widths
→ grouped query mapping
→ KV bytes/token
→ decode bandwidth
→ quality/speed design tradeoff
```

Primary sources:
- original MHA Transformer;
- MQA: Fast Transformer Decoding / One Write-Head;
- GQA paper;
- Llama 2 as production/model-family example.

## After

- SwiGLU / FFN
- MoE
- model architecture comparison project

Never infer architecture only from parameter count.

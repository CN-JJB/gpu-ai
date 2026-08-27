# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Frozen constraints

Core ability stack:
**会理解 → 会调查 → 会选择 → 会实践 → 会改造**

Never fabricate benchmark, market, transaction or model-runtime data.

## Completed frontier

Slices 01–24 are implemented.

Latest completed model-architecture slice:

**24 — Decoder-only Transformer Dataflow**

```
token ids
→ embedding
→ decoder blocks
→ final norm
→ LM head
→ logits
```

The core split:

```
Prefill:
[B,T,d]
→ large matrix regime
→ build KV

Decode:
[B,1,d]
+ historical KV
→ serial autoregressive regime
→ append KV
```

Key files:
- `research/llm/0007-decoder-only-transformer-dataflow.md`
- `reference/llm/decoder-only-block-shapes.md`
- `lessons/24-transformer-anatomy/`
- `labs/experiments/42-decoder-transformer-shape-flow/`
- `labs/experiments/43-real-model-config-anatomy/`

Experiment 42 synthetic arithmetic was verified.
Experiment 43 inspects real model config and warns on non-homogeneous architecture features.

## Active next slice — RMSNorm / residual / RoPE

Build:

```
pre-norm residual block
→ RMSNorm math
→ scale vector
→ Q/K projection
→ position-dependent RoPE rotation
→ cached K position identity
→ context extension / rope scaling boundary
```

Stable concepts first.
Current runtime/model-specific RoPE scaling schemes should be kept separate when they are architecture/config specific.

## After

- MHA / MQA / GQA
- SwiGLU / FFN
- MoE

Tie each to:
- parameter count;
- KV;
- PP/TG;
- kernel behavior.

## Matt Pocock skills

High-frequency:
- `teach`
- `research`

Use verifiable exercises and explicit provenance.

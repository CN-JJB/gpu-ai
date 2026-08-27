# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–26 are implemented.

Latest LLM architecture spine:

### Slice 24
Decoder-only prefill/decode dataflow.

### Slice 25
RMSNorm / residual / RoPE.

### Slice 26
MHA / MQA / GQA.

Key Slice 26 result:

```
KV bytes/token
=
2 × layers × Hkv × head_dim × bytes
```

Default teaching example:

```
32 layers
32 Q heads
Dh=128
FP16
32k context

MHA Hkv32 → 16 GiB
GQA Hkv8  → 4 GiB
MQA Hkv1  → 0.5 GiB
```

Key files:
- `research/llm/0009-mha-mqa-gqa.md`
- `reference/llm/mha-mqa-gqa-kv.md`
- `lessons/26-attention-heads/`
- `labs/experiments/46-mha-gqa-mqa-kv-model/`
- `labs/experiments/47-real-model-attention-config-compare/`

## Active next slice — SwiGLU / FFN

Build:

```
hidden d
→ gate projection d→d_ff
→ up projection d→d_ff
→ SiLU(gate) × up
→ down projection d_ff→d
→ residual
```

Teach:
- roughly 3 d d_ff dense gated-MLP weights/layer;
- comparison with attention projection weights;
- PP vs TG shape differences;
- weight-streaming implications;
- why quantization affects FFN traffic heavily.

## After

MoE:
```
router
→ top-k experts
→ active vs total parameters
→ expert weight traffic
→ batching/routing imbalance
```

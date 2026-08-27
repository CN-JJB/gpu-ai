# Learning / Build Record — 2026-08-27 Modern KV Architectures

## Slice

30 — Sliding/local attention, hybrid full+local layers and compressed/latent KV families.

## Production output

Research:
- `research/llm/0013-modern-kv-attention-architectures.md`

Reference:
- `reference/llm/sliding-hybrid-latent-kv.md`

Lesson:
- `lessons/30-modern-kv/01-sliding-hybrid-latent.html`

Labs:
- `labs/experiments/54-sliding-hybrid-kv-model/`
- `labs/experiments/55-real-attention-kv-architecture/`

Evidence:
- `examples/evidence/experiment-30-modern-kv-architectures.md`

## Verified L0 result

32k:
```
full 4 GiB
local 0.5 GiB
hybrid 1.375 GiB
```

128k:
```
full 16 GiB
local 0.5 GiB
hybrid 4.375 GiB
```

for the declared synthetic 8-full/24-local configuration.

## Stable skill

Learner now upgrades KV reasoning from:

```
one formula
```

to:

```
per-layer cached positions
×
per-layer cached state width
```

with model-specific evidence.

## Next

Tokenizer / chat-template / special-token / logits-sampling boundary:
- same weights + different prompt serialization can change model behavior;
- token count changes context/KV/PP;
- chat template is runtime/model interface, not cosmetic UI formatting.

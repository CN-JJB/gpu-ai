# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–29 are implemented.
Experiments 01–53 are indexed.

## Model architecture spine

```
24 Decoder-only dataflow
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / dense FFN
28 MoE
29 Model Architecture Dossier
```

## Slice 29 core rule

Architecture inspection produces three evidence classes:

```
KNOWN
DERIVED
MUST MEASURE
```

Capacity lower-bound verdict:

```
lower bound > usable memory
→ FAIL-WITHOUT-OFFLOAD

lower bound <= usable memory
→ POSSIBLE-NOT-PROVEN
```

Never call the second case PASS without real runtime evidence.

## Active next slice

Modern attention/context architectures:

```
full attention
vs
sliding/local attention
vs
hybrid layer patterns
vs
compressed/latent KV families
```

Teach why:

```
2 × L × Hkv × Dh × bytes × context
```

is a homogeneous full-attention baseline, not a universal exact KV formula.

Need:
- local window formula;
- mixed full/local layer formula;
- architecture caveats;
- real config inspector extension.

Do not generalize DeepSeek MLA implementation to all compressed-KV architectures.

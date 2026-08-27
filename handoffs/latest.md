# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–30 are implemented.

Latest model architecture chain:

```
24 decoder-only dataflow
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / dense FFN
28 MoE
29 Model Architecture Dossier
30 Sliding / Hybrid / Latent KV
```

## Slice 30 core

General cache accounting:

```
Σ_l
(
cached positions_l
× cached state width_l
× bytes
)
```

Ordinary full attention is a special case.

Verified synthetic hybrid:

```
32 layers
8 full
24 local
W=4096
Hkv=8
Dh=128
FP16

32k:
full 4 GiB
local 0.5 GiB
hybrid 1.375 GiB

128k:
full 16 GiB
local 0.5 GiB
hybrid 4.375 GiB
```

DeepSeek-style MLA proxy is opt-in and architecture-specific.

## Active next slice — Tokenization / Chat Template / Sampling Boundary

Build:

```
raw user text
→ chat template serialization
→ special tokens
→ tokenizer
→ token IDs
→ model logits
→ sampling policy
→ next token
→ text decode
```

Teach:
- chat template is part of workload/model interface;
- prompt token count changes PP/KV/context;
- exact prompt serialization must be preserved for benchmarking;
- logits are not sampled text;
- deterministic/greedy vs stochastic sampling;
- same random seed may still differ across runtimes/numerics.

Then connect to serving TTFT and reproducible benchmarks.

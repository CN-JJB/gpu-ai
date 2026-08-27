# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–32 are implemented.
Experiments 01–59 exist.

Latest model/system chain:

```
24 decoder-only dataflow
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / dense FFN
28 MoE
29 Model Architecture Dossier
30 Sliding / Hybrid / Latent KV
31 Tokenizer / Chat Template / Sampling
32 Quality Gate
```

## Slice 32 core

For a fixed tokenizer/corpus/evaluation:

```
NLL = -ln p(correct token)
CE = mean(NLL)
PPL = exp(CE)
```

Lower PPL means better next-token fit **only on the same evaluation setup**.

Do not use PPL as:
- a universal chat-quality score;
- a direct comparison across different tokenizers;
- the only regression gate.

Pair it with target-task fixtures.

## Verified L0 toy

```
baseline PPL = 3.363585661
candidate PPL = 3.808736185
ratio = 1.132344043×
```

Synthetic only.

## Active next slice — Benchmark / Workload Manifest

Create one machine-readable experiment identity:

```
hardware
+ runtime/build
+ model artifact SHA
+ architecture dossier
+ prompt/token artifact
+ sampler
+ PP/TG config
+ quality corpus/fixtures
+ telemetry mode
```

Then:
- hash the manifest;
- validate baseline vs candidate;
- reject undeclared identity changes;
- allow exactly one declared experimental variable;
- index all raw Evidence files.

This should supersede ad-hoc command screenshots and strengthen Experiment 40 rather than duplicate it.

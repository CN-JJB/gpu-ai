# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–28 are implemented.

Current LLM architecture spine:

```
24 decoder-only prefill/decode dataflow
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / dense FFN
28 Mixture of Experts
```

## Slice 28 core rule

Never merge:

```
total params
active params/token
resident weight memory
actual weight bytes moved
```

Default synthetic expert model verified:

```
d=4096
expert_ffn=14336
8 experts
top-2
32 MoE layers
4.5 bpw

one expert        94.5 MiB
all experts/layer 756 MiB
top-2/layer       189 MiB
all expert storage across layers 23.625 GiB
```

Balanced routing can improve expert-parallel utilization while touching more unique weights.
Skewed routing can improve idealized reuse while creating severe device imbalance.

## Active next slice — Model Architecture Dossier

Build one integration project:

```
real config.json
→ model identity
→ decoder dimensions
→ Hq/Hkv/Dh
→ KV bytes/token/context/concurrency
→ dense FFN structure
→ MoE structure if present
→ weight-storage proxies
→ architecture-specific caveats
→ PP/TG bottleneck hypotheses
→ hardware questions
```

Critical language:
- estimates/proxies are not measured VRAM;
- hypotheses are not benchmarks;
- model-specific fields override generic formulas.

This should become the model-side counterpart to Slice 18 hardware candidate dossier.

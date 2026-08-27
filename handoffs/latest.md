# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–27 are implemented.

Latest LLM architecture spine:

```
24 decoder-only dataflow
25 RMSNorm / residual / RoPE
26 MHA / MQA / GQA
27 SwiGLU / dense FFN
```

## Slice 27 key result

Default dense teaching example:

```
d=4096
d_ff=11008

SwiGLU FFN:
135,266,304 weights/layer

classic MHA Q/K/V/O:
67,108,864 weights/layer

ratio:
2.015625×
```

FFN storage proxy:
- FP16: 258 MiB/layer
- 4.5 bpw: 72.5625 MiB/layer

Key files:
- `research/llm/0010-swiglu-dense-ffn.md`
- `reference/llm/swiglu-ffn-weight-traffic.md`
- `lessons/27-swiglu-ffn/`
- `labs/experiments/48-dense-swiglu-ffn-model/`
- `labs/experiments/49-real-model-ffn-structure-compare/`

## Active next slice — Mixture of Experts

Build:

```
hidden
→ router logits
→ top-k expert choice
→ selected expert FFNs
→ weighted combine
→ residual
```

Teach these distinctions:

```
total parameters
!= active parameters/token
!= resident memory
!= bytes actually moved/token
```

Also cover:
- expert reuse within prefill/batch;
- routing imbalance;
- capacity/load balancing;
- expert placement across GPUs;
- interconnect cost;
- why MoE can have huge total weights but lower active FLOPs;
- why local decode can still be memory-heavy.

Do not use one vendor/model's MoE implementation as universal.

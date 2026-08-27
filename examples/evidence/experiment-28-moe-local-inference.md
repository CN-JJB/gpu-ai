# Evidence — Experiment 28: Mixture of Experts Local-Inference Accounting

状态：stable MoE lesson complete; L0 total/active/resident/reuse model verified; real config inspector ready.

## Claim

> MoE active parameters are not the same quantity as model size, resident GPU memory or actual bytes moved per token. Local inference must separately reason about expert storage, routing, batching/reuse and interconnect/offload.

## Primary evidence

### Switch Transformer
https://arxiv.org/abs/2101.03961

Sparse activation allows parameter count to scale without activating every expert for each token, while routing, communication and load balancing remain core systems concerns.

### Mixtral of Experts
https://arxiv.org/abs/2401.04088

Concrete top-2 sparse decoder example:
- 8 FFN experts/layer;
- 2 selected experts/token.

### DeepSeekMoE
https://arxiv.org/abs/2401.06066

Adds finer routed experts and shared experts.

### DeepSeek-V3
https://arxiv.org/abs/2412.19437

Reports:
```
671B total parameters
37B activated per token
```

The course uses this only to illustrate that total and active parameters are distinct; it does not infer resident memory from the 37B figure.

## Four quantities

```
total params
active params/token
resident weight memory
actual weight bytes moved
```

must remain separate.

## Experiment 50 verification

Default synthetic teaching model:

```
d=4096
expert d_ff=14336
N=8
top-k=2
L_moe=32
4.5 bpw
batch=16
```

Verified:

```
one expert weights
= 176,160,768

one expert storage
= 94.5 MiB

all routed experts/layer
= 756 MiB

selected top-2/layer
= 189 MiB

all routed expert storage across 32 layers
= 23.625 GiB

top-2 no-reuse selected-expert proxy across 32 layers/token
= 5.90625 GiB
```

These are expert-only formula proxies, not a full model or measured memory traffic.

## Balanced route

```
[4,4,4,4,4,4,4,4]
```

Verified:
- 8 unique experts;
- expert max/avg load = 1.0×;
- four-device assignments = [8,8,8,8];
- device max/avg = 1.0×;
- ideal unique-expert weight proxy = 47.25 MiB/token/layer.

## Skewed route

```
[16,16,0,0,0,0,0,0]
```

Verified:
- 2 unique experts;
- expert max/avg = 4.0×;
- device assignments = [32,0,0,0];
- device max/avg = 4.0×;
- ideal unique-expert weight proxy = 11.8125 MiB/token/layer.

Therefore:

```
better ideal weight reuse
!=
better expert-parallel load balance
```

## Experiment 51

The real config inspector recognizes common aliases for:
- routed expert count;
- top-k;
- shared experts;
- expert intermediate size.

It reports per-layer common SwiGLU-like baselines and surfaces architecture fields such as:
- first dense layers;
- MoE frequency;
- routing/scoring settings;
- shared expert width.

It explicitly refuses to equate a per-layer baseline with full-model accounting when architecture-specific details exist.

## Local deployment consequence

All experts GPU-resident:

```
VRAM needs total expert storage
```

not just active top-k.

If experts are offloaded/distributed:

```
routing
→ PCIe/P2P/interconnect
→ expert compute
→ return/combine
```

can become the new bottleneck.

## Learner should reject

- active params = model file size;
- top-k experts are the only experts that need to exist in memory;
- fewer active params guarantees faster TG;
- expert weights are always reread independently for each prefill token;
- perfect load balance always minimizes memory traffic;
- MoE expert parallelism is identical to tensor parallel all-reduce;
- shared experts can be ignored.

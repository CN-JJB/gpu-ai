# Learning / Build Record — 2026-08-27 Mixture of Experts

## Slice

28 — MoE routing, total vs active parameters, resident storage, expert batching/reuse and multi-GPU communication.

## Production output

Research:
- `research/llm/0011-mixture-of-experts-local-inference.md`

Reference:
- `reference/llm/moe-total-active-resident-traffic.md`

Lesson:
- `lessons/28-moe/01-router-active-resident-traffic.html`

Labs:
- `labs/experiments/50-moe-active-weight-reuse-model/`
- `labs/experiments/51-real-moe-config-inspector/`

Evidence:
- `examples/evidence/experiment-28-moe-local-inference.md`

## Verified L0 result

Default 8-expert/top-2 synthetic model:
- one expert 94.5 MiB at 4.5 bpw;
- all experts/layer 756 MiB;
- selected top-2/layer 189 MiB;
- 32-layer expert storage 23.625 GiB;
- no-reuse selected expert proxy 5.90625 GiB/token.

Routing example verified:
- balanced gives 1.0× device imbalance;
- skewed gives 4.0× device imbalance while touching fewer unique experts.

## Stable skill

Learner can now explain:

```
large total sparse model
→ only some experts compute/token
→ but all experts may still need residence
→ batching changes weight reuse
→ expert parallelism adds token dispatch/interconnect
```

## Next

Integrate Slices 24–28 into a model architecture dossier:

```
config.json
→ dense/MoE anatomy
→ KV
→ weight structure
→ active/resident distinction
→ expected PP/TG pressure
→ hardware-fit questions
```

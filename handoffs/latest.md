# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–33 are implemented.
Experiments 01–61 exist.

## Slice 33

Unified benchmark identity:

```
fixed
+ variant
+ audit
```

Only one declared path under `variant.*` may change.

Examples:

```
variant.execution.flash_attention
```

for a leaf A/B, or:

```
variant.model
```

for a quantization block where artifact SHA/bytes/quant necessarily co-vary.

Validator synthetic self-check:
- legal Q8→Q4 model block: PASS;
- same change + hidden prompt-token hash mutation: FAIL.

Experiment 61 is now the stricter manifest path; Experiment 40 remains the beginner controlled-A/B introduction.

## Active next slice — Serving Workload / SLO

Build:

```
request arrival
+ prompt length
+ output length
+ concurrency
→ queue wait
→ TTFT
→ token cadence / ITL
→ E2E
→ request throughput
→ aggregate token throughput
→ percentiles / SLO
```

Need to teach:
- averages hide tails;
- p95/p99 are order statistics, not magic guarantees;
- long prompts can hurt short-request TTFT through shared batching/queueing;
- throughput-optimal concurrency may violate latency SLO;
- workload distributions must be part of manifest identity.

Reuse Slice 08 continuous batching and Slice 09 cache concepts rather than duplicating them.

# Evidence — Experiment 18: Cross-Vendor Used-Hardware Decision Framework

状态：stable decision framework complete; L0 scenario model and real candidate dossier are ready.

## Claim

> A useful local-LLM hardware decision must apply workload-specific hard gates before ranking performance. Capacity, software support, bandwidth, compute, interconnect, TCO and secondhand risk are separate dimensions; no universal score can rank all NVIDIA/AMD/Apple/Intel candidates.

## Stable decision chain

```
workload identity
→ fit gate
→ software gate
→ bottleneck/roof classification
→ comparable benchmark evidence
→ TCO
→ used-hardware risk
→ BUY / BUY IF PRICE≤X / KEEP / SKIP / NEEDS EVIDENCE
```

## Hard Gate A — Fit

Discrete GPU:

```
weights + KV + workspace + runtime headroom
<= usable VRAM
```

Apple/iGPU/shared-memory systems:

```
runtime footprint
<= safe working-set budget
```

Multi-GPU:

```
per-device allocation
+ sharding
+ communication buffers
+ headroom
```

not simply `sum(VRAM)`.

## Hard Gate B — Software

Support states:

- official-current;
- official-pinned;
- community-enabled;
- runtime-visible-only;
- unsupported.

A candidate cannot be rescued by high theoretical compute if the target backend/kernel path is unacceptable for the learner's scenario.

## Performance roofs

Decode:

```
TG rough roof
≈ usable memory bandwidth
 / bytes streamed per generated token
```

Prefill:

```
PP roof
≈ min(
  actual matrix compute path,
  bandwidth × arithmetic intensity
)
```

Multi-device/offload:

```
+ communication / effective link bandwidth
+ synchronization
+ imbalance
```

## Experiment 31 — scenario dependence

Synthetic candidates deliberately represent different tradeoffs.

Verified hard-gate behavior:

### Interactive scenario
Required memory:
```
18 GiB
```

- Candidate A: FAIL capacity
- Candidate B: PASS
- Candidate C: PASS
- Candidate D: FAIL software

Only B/C are ranked.

### Long-context scenario
Required memory:
```
22 GiB
```

- Candidate A: FAIL capacity
- Candidate B: PASS
- Candidate C: PASS
- Candidate D: FAIL software

The weighting changes toward memory margin/risk, so the ranking changes relative to the interactive case.

Pedagogical result:

```
same hardware candidates
+ different workload
→ different rational decision
```

No synthetic result is a real hardware recommendation.

## Experiment 32 — real candidate dossier

The untouched template intentionally lacks critical fields.

Expected status:

```
NEEDS EVIDENCE
```

The evaluator refuses to invent:
- exact model;
- usable memory;
- price;
- workload footprint;
- software support;
- benchmark;
- condition.

When data is supplied, it can produce:
- SKIP / CHANGE WORKLOAD;
- NEEDS SOFTWARE DECISION;
- NEEDS EVIDENCE;
- READY FOR SCENARIO DECISION.

It deliberately never auto-outputs BUY.

## Evidence quality

- E3: official/current or local raw evidence;
- E2: reproducible/reputable external evidence;
- E1: weak anecdote/seller claim;
- E0: unknown.

Decision confidence is limited by weak critical claims.

## Learner should reject

- “24 GB automatically beats 16 GB”;
- “newest architecture is best”;
- “TOPS predicts llama.cpp tokens/s”;
- “two GPUs equal one larger GPU”;
- “installed unified memory equals free GPU memory”;
- “official driver support proves optimized local-LLM support”;
- “seller condition claims are sufficient”;
- “one benchmark from another model/quant proves my workload”;
- “one universal score ranks all hardware”.

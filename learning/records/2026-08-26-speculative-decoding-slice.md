---
date: 2026-08-26
type: course-build-record
---

# Speculative Decoding vertical slice completed

第十个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → optional real server Experiment → Evidence → Dynamic Intelligence → Resources update → Learning update。

## Built artifacts

- research/llm/0006-speculative-decoding.md
- reference/llm/speculative-decoding-acceptance-overhead.md
- lessons/10-speculative-decoding/01-draft-verify-acceptance.html
- labs/experiments/15-speculative-acceptance-overhead-model/
- labs/experiments/16-llama-server-speculative-probe/
- examples/evidence/experiment-10-speculative-decoding.md
- intelligence/llm/speculative-decoding-2026-08-26.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### The proposer is not the authority

Stable chain：

~~~text
cheap proposal
→ target batched verification
→ accept/correct
→ advance target sequence
~~~

Theoretical speculative decoding/sampling keeps target semantics/distribution through verification and rejection/correction rules.

### Speculation attacks serial decode

Baseline new-token generation requires repeated serial target calls.

The performance opportunity comes from verifying multiple proposed positions in a more parallel target call.

This connects directly to earlier Roofline/decode reasoning.

### Acceptance is necessary but not sufficient

High accepted-token ratio does not guarantee wall speedup.

Total economics include：

- proposer cost
- verification cost
- correction/sampling
- draft memory/KV
- placement/offload
- target baseline utilization
- concurrency

### Draft length is a tuning variable

L0 shows low acceptance makes long draft suffixes mostly wasted work.

Default synthetic cost model：

At p=0.30：
- D1 → 1.083×
- D2 → 1.053×
- D4 → 0.914×
- D8 → 0.700×

At p=0.60：
- D2 is near the optimum in this model
- D8 loses much of the benefit

At p=0.90：
- longer drafts continue to amortize verification
- D8 reaches a synthetic 3.003× ceiling

These are concept units, not real runtime claims.

### Memory matters

Two-model draft can add：

- draft weights
- draft KV
- runtime buffers

and can force target placement/offload changes.

For local low-VRAM systems, this can erase algorithmic gains.

### Draftless speculation is a useful first lab

llama.cpp current n-gram methods avoid requiring a second model.

This lowers the hardware/compatibility barrier and exposes workload dependence.

### Low-batch bias is explicit

Current vLLM/TensorRT-LLM docs emphasize low/medium-QPS or low-batch speculative opportunities.

This prevents the course from multiplying a single-user speedup into a high-concurrency serving claim.

## Correctness language

Original papers support target-distribution-preserving speculative algorithms.

The Lesson explicitly distinguishes that from byte-identical output across stochastic runtime runs, where floating-point/batching/nondeterminism can change exact tokens.

## Real experiment

Experiment 16 supports：

### Path A
target-only baseline vs n-gram speculation

Records current server metric deltas：

- predicted tokens/time
- decode calls
- draft tokens
- accepted tokens
- speculative verification rounds

and compares repetitive vs novel prompts.

### Path B
optional compatible draft model

Adds Evidence for：

- draft artifact/hash
- tokenizer compatibility
- draft placement
- extra memory
- target placement change

The lab also points to current upstream SPEED-Bench for formal baseline/spec category-level comparison.

No real performance numbers are fabricated.

## Dynamic snapshot

Pinned llama.cpp upstream：

d7a2074112d27649303fa107eb8c94db1ee435f3

Current spec types/metrics/flags plus vLLM/TensorRT-LLM implementation notes are stored in intelligence rather than stable Lesson.

## Skill workflow

- teach：real “small model guesses?” misconception → proposal/verify/cost model → retrieval/transfer.
- research：original papers + llama.cpp + vLLM + TensorRT-LLM.
- scaffold-exercises discipline：deterministic acceptance/overhead L0 plus bounded real A/B.
- intelligence separation：rapidly evolving proposer families/flags kept dated.
- no grill/to-spec：v1 scope remains frozen.
- domain-modeling not triggered：no new repository-wide vocabulary boundary needed.

## Next

Single-node multi-GPU/interconnect：

capacity aggregation
→ model/layer split
→ tensor split
→ communication
→ topology
→ scaling efficiency.

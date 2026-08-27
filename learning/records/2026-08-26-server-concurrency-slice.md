---
date: 2026-08-26
type: course-build-record
---

# llama-server concurrency / continuous batching vertical slice completed

第八个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → optional real server Experiment → Evidence → Dynamic Intelligence snapshot → Resources update → Learning update。

## Built artifacts

- research/llm/0004-server-slots-continuous-batching.md
- reference/llm/server-concurrency-batching-metrics.md
- lessons/08-local-serving/01-slots-batching-ttft.html
- labs/experiments/11-server-slots-continuous-batching/README.md
- labs/experiments/11-server-slots-continuous-batching/simulate.py
- labs/experiments/11-server-slots-continuous-batching/EXPECTED.md
- labs/experiments/12-llama-server-concurrency-probe/README.md
- labs/experiments/12-llama-server-concurrency-probe/load_probe.py
- labs/experiments/12-llama-server-concurrency-probe/RESULT-TEMPLATE.md
- labs/experiments/12-llama-server-concurrency-probe/EXPECTED.md
- examples/evidence/experiment-08-server-concurrency.md
- intelligence/llm/llama-server-concurrency-2026-08-26.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Primary-source snapshot

Research pinned current llama.cpp master at:

d7a2074112d27649303fa107eb8c94db1ee435f3

Current upstream confirms:
- parallel multi-user server slots；
- continuous batching；
- OpenAI-compatible streaming；
- /slots；
- /metrics；
- request processing/deferred metrics；
- busy slots per decode metric；
- official concurrent server benchmarks。

Dynamic spellings/defaults are kept in intelligence, not stable Lesson.

## Core teaching model

The slice establishes:

~~~text
clients
→ queue
→ slots
→ prompt processing
→ dynamic active decode set
→ continuous batching
→ streamed output
~~~

with a parallel resource path:

~~~text
active sequences × context
→ KV pressure
~~~

This connects:
- Slice 04 Roofline/decode bandwidth；
- Slice 05 KV capacity；
- Slice 07 single-request PP/TG；
into one serving model.

## Metric separation

Stable Lesson now requires separate treatment of:

- TTFT
- ITL
- E2E latency
- request throughput
- aggregate token throughput
- server prompt/decode throughput

The real probe deliberately labels SSE inter-event timing as:

~~~text
stream-gap proxy
~~~

rather than exact ITL because one HTTP/SSE delta is not guaranteed to equal one model token.

## L0 validation — equal-length burst

Synthetic model:

- 8 requests
- 32 tokens each
- all arrive at t=0
- step_time(batch)=1+0.22×(batch−1)

Results:

| slots | aggregate tok/u | avg first-token wait proxy |
|---:|---:|---:|
| 1 | 1.000 | 113.00 |
| 2 | 1.639 | 59.78 |
| 4 | 2.410 | 28.22 |
| 8 | 3.150 | 2.54 |
| 16 | 3.150 | 2.54 |

This demonstrates simultaneously:

- queue reduction；
- sublinear throughput scaling；
- larger active-step cost；
- no benefit from slots beyond available requests。

## L0 validation — continuous admission

Mixed output lengths:

8, 32, 8, 32, 8, 32

slots=2。

Static groups:

- makespan 101.28
- aggregate 1.185

Continuous admission:

- makespan 82.56
- aggregate 1.453

The gain comes from filling a freed slot while another long request remains active.

No real llama-server performance multiplier is inferred from these synthetic units.

## Real experiment design

Experiment 12 fixes one dedicated llama-server and sweeps:

client concurrency 1 / 2 / 4 / 8

with total requests fixed at 8.

The lightweight standard-library Python probe:

- sends streaming OpenAI-compatible chat requests；
- records first non-empty SSE delta as TTFT proxy；
- records E2E latency；
- records stream-event cadence proxy；
- polls /metrics during the run；
- computes server prompt/decode throughput from counter deltas；
- computes wall aggregate output throughput；
- records peak processing/deferred and busy-slots evidence；
- saves raw JSON。

Prompt caching is disabled for this slice so repeated-prefix reuse remains a separate variable for the next slice.

## No fake Evidence

The build environment does not run a real model/server benchmark.

Experiment 12 contains:
- methodology；
- client code；
- structural expected outcomes；
- result template；

but no invented CPU/GPU latency or throughput numbers.

## Skill workflow

- teach：real multi-user symptom → minimal server model → retrieval/transfer check。
- research：canonical llama.cpp server docs/source first。
- scaffold-exercises discipline：L0 has deterministic expected output；real lab has explicit variables and raw Evidence。
- intelligence separation：current flags/metrics pinned by date + upstream commit。
- no grill/to-spec：v1 requirements remain frozen and current slice has no unresolved requirement branch。
- domain-modeling not triggered：terms fit existing stable/dynamic project language。

## Next

Continue the Course Map serving path:

Paged/Unified KV
→ Prefix/Prompt Cache
→ repeated-prefix reuse
→ cache capacity/eviction
→ TTFT effect

Then enter speculative decoding before multi-GPU/interconnect.

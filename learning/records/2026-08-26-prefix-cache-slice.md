---
date: 2026-08-26
type: course-build-record
---

# Prefix / Paged KV cache vertical slice completed

第九个 bounded slice 完成：

Research → Reference → HTML Lesson → L0 Experiment → optional real server Experiment → Evidence → Dynamic Intelligence → Resources update → Learning update。

## Built artifacts

- research/llm/0005-prefix-paged-kv-cache.md
- reference/llm/prefix-paged-kv-cache.md
- lessons/09-kv-cache/01-prefix-paged-kv.html
- labs/experiments/13-prefix-cache-capacity-model/
- labs/experiments/14-llama-server-prefix-cache-probe/
- examples/evidence/experiment-09-prefix-cache.md
- intelligence/llm/prefix-kv-cache-2026-08-26.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Research conclusions

### Ordinary KV and prefix KV reuse are different

Ordinary cache avoids recomputing earlier K/V during the same autoregressive request.

Prefix cache allows a later request sharing an already-computed prompt prefix to reuse that state.

### Prefix cache is primarily a prefill optimization

Stable causal chain：

~~~text
matching long prefix
→ reuse prompt KV
→ prompt_n / prompt work ↓
→ TTFT opportunity ↓
~~~

New output tokens still require decode.

This boundary is independently supported by current vLLM official APC documentation.

### Paged/unified/prefix terminology is separated

- paged/block KV: memory allocation/reference abstraction
- prefix cache: reuse policy/opportunity
- llama.cpp unified KV: current runtime-specific shared KV manager/buffer

The course does not call them synonyms.

### Finite capacity means eviction

vLLM and TensorRT-LLM current docs both provide finite block-pool/reuse examples with LRU-like eviction.

Stable Lesson preserves only：

~~~text
finite reusable cache
→ memory competition
→ eviction policy
~~~

without claiming every runtime must use LRU forever.

### Hit rate is not enough

The course prioritizes：
- reused tokens
- processed prompt tokens
- prompt_ms
- TTFT
- cache memory cost

over raw hit count.

### Concurrency changes warm-cache behavior

Current TensorRT-LLM docs note same-prefix requests launched together may not all benefit before reusable state has been produced.

Therefore Experiment 14 focuses on cold vs warm sequential first.

## L0 validation

Synthetic requests：

A, B, A, C, A, B

Each：
- 1024 shared-prefix tokens
- 64 unique-suffix tokens
- 128 output tokens

Results：

- capacity 0 → 0 hits, 6528 prompt tokens processed
- capacity 1 → 0 hits despite cache enabled
- capacity 2 → 2 hits, 2048 prompt tokens saved
- capacity 3 → 3 hits, 3072 prompt tokens saved

All cases：
- 768 new decode tokens

This is the key prefill-vs-decode Evidence.

## Real experiment design

Experiment 14 uses a current llama-server dedicated slot and two independent pairs：

Pair A：
- cold exact
- warm exact
- near-miss
- records cache_n / prompt_n / prompt_ms / predicted_ms

Pair B：
- separate cold/warm streaming prompt
- records TTFT and stream-gap proxy

Separate prompt IDs prevent the timing-pair requests from pre-warming the TTFT pair.

Optional controls：
- prompt cache disabled
- finite cache / eviction stress

No real performance numbers are fabricated.

## Dynamic implementation snapshot

Pinned llama.cpp upstream：

d7a2074112d27649303fa107eb8c94db1ee435f3

Current llama-server cache flags/timing fields, vLLM block/cache-salt design and TensorRT-LLM reuse/eviction details are stored in dated intelligence.

## Skill workflow

- teach：real repeated-document/system-prompt problem → minimal cache model → retrieval/transfer.
- research：llama.cpp + vLLM + TensorRT-LLM official sources first.
- scaffold-exercises discipline：deterministic L0 and bounded real probe.
- intelligence separation：current cache flags/policies are dated, not timeless Lesson truth.
- no grill/to-spec：v1 remains frozen.
- domain-modeling not triggered：existing stable/dynamic terminology is sufficient.

## Next

Speculative Decoding：
proposal/draft → target verify → acceptance → speedup vs overhead → memory/config trade-off.

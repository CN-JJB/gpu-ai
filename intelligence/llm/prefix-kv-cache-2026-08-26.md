---
snapshot_date: 2026-08-26
type: dynamic-intelligence
topic: prefix-kv-cache
llama_cpp_upstream_commit: d7a2074112d27649303fa107eb8c94db1ee435f3
---

# Prefix / Prompt KV Cache Snapshot — 2026-08-26

## Why this file exists

Prefix-cache interface、block management、eviction 与 isolation policy 会变化。

Stable Lesson 保存：

- repeated-prefix prefill reuse；
- prefill vs decode boundary；
- finite capacity；
- eviction；
- paged/unified/prefix-cache terminology separation。

本文件保存 current implementation evidence。

## llama.cpp current snapshot

Source：

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Pinned upstream commit：

d7a2074112d27649303fa107eb8c94db1ee435f3

Current server docs expose：

~~~text
--cache-prompt / --no-cache-prompt
--cache-reuse N
--cache-ram N
--ctx-checkpoints
--checkpoint-min-step
--kv-unified / --no-kv-unified
--cache-idle-slots
~~~

Current defaults/semantics are implementation details and must be rechecked with --help.

### Current response timing evidence

Current OpenAI-compatible chat response example includes：

~~~text
timings.cache_n
timings.prompt_n
timings.prompt_ms
timings.prompt_per_second
timings.predicted_n
timings.predicted_ms
timings.predicted_per_second
~~~

Current docs describe：

- cache_n = prompt tokens reused from cache
- prompt_n = prompt tokens actually processed

This is the main Evidence path for Experiment 14.

## vLLM Automatic Prefix Caching

Source：

https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html

Current official stable statement：

- existing prefix KV can be reused across requests；
- repeated long-document queries and multi-round conversations are important use cases；
- reused prefix avoids redundant prompt/prefill computation；
- it does not reduce the cost of generating new output tokens；
- requests without shared prefix receive no APC benefit。

This is treated as stable concept-level evidence.

## vLLM prefix-cache design

Source：

https://docs.vllm.ai/en/latest/design/prefix_caching/

Current design includes：

- fixed KV blocks/pages；
- hash-based prefix identity；
- finite block pool；
- free queue / LRU-style eviction path；
- reusable blocks becoming eviction candidates when unreferenced；
- cache_salt support for reuse-domain / multi-tenant isolation。

Do not copy internal data structures into stable cross-backend definitions.

## TensorRT-LLM KV cache reuse

Source：

https://nvidia.github.io/TensorRT-LLM/advanced/kv-cache-reuse.html

Current docs state：

- requests with same prompt prefix can reuse KV pages；
- this can reduce first-token latency；
- system prompts / multi-turn histories are key examples；
- reusable blocks can be evicted when memory is required；
- current policy is LRU-like；
- concurrent same-prefix requests may start before an earlier request has produced reusable cache state。

The last point matters for cold-vs-warm-concurrent benchmarks.

## TensorRT-LLM KV Cache System

Source：

https://nvidia.github.io/TensorRT-LLM/features/kvcache.html

Current system exposes a finite KV block pool with request allocation and reuse/offload-related management.

Teaching use：

~~~text
paged/block memory management
!= automatic prefix hit
~~~

## Terminology rule

Do not collapse：

~~~text
ordinary KV cache
prefix/prompt cache
paged/block KV
llama.cpp unified KV
~~~

into one concept.

They overlap in purpose but are not synonyms or identical implementations.

## Freshness rule

Before a future real deployment：

1. record runtime version/commit；
2. check current llama-server --help or target backend docs；
3. check current cache/timing fields；
4. create a new dated intelligence snapshot if semantics changed；
5. preserve this snapshot as historical Evidence。

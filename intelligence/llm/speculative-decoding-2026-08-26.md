---
snapshot_date: 2026-08-26
type: dynamic-intelligence
topic: speculative-decoding
llama_cpp_upstream_commit: d7a2074112d27649303fa107eb8c94db1ee435f3
---

# Speculative Decoding Snapshot — 2026-08-26

## Purpose

Speculation methods、flags、model compatibility and metrics are rapidly evolving.

Stable Lesson keeps：

- proposal
- target verification
- acceptance/correction
- accepted progress vs overhead
- memory / batching interactions

This file preserves current interface evidence.

## llama.cpp current snapshot

Source：

https://github.com/ggml-org/llama.cpp/blob/master/docs/speculative.md

Pinned commit：

d7a2074112d27649303fa107eb8c94db1ee435f3

Current speculative families listed include：

- draft-simple
- draft-eagle3
- draft-dflash
- draft-dspark
- draft-mtp
- ngram-cache
- ngram-simple
- ngram-map-k
- ngram-map-k4v
- ngram-mod

This list is dynamic and must not become a timeless Lesson table.

### Current draft controls

Current docs expose concepts/flags for：

- draft model path/HF repo
- max/min draft tokens
- draft probability/confidence controls
- draft device/GPU layers
- draft CPU threads
- draft KV types
- n-gram-specific lengths/matching controls

Exact names/defaults must be rechecked with current --help.

### Current statistics

Current docs print examples such as：

~~~text
draft acceptance rate
accepted / generated
# gen drafts
# acc drafts
# gen tokens
# acc tokens
~~~

Current server /metrics documentation includes：

~~~text
llamacpp:spec_decode_num_draft_tokens_total
llamacpp:spec_decode_num_accepted_tokens_total
llamacpp:spec_decode_num_drafts_total
llamacpp:spec_decode_num_accepted_tokens_per_pos_total
~~~

Experiment 16 uses the first three counters.

## llama.cpp n-gram current note

Current ngram-mod docs describe a small fixed-size hash pool shared across server slots and recommend it for repetition-heavy workloads such as code iteration/summarization/repeated reasoning structure.

Teaching rule：

~~~text
history proposer performance is workload-dependent
~~~

not：

~~~text
ngram always speeds up decode
~~~

## vLLM current snapshot

Source：

https://docs.vllm.ai/en/latest/features/speculative_decoding/

Current docs position speculative decoding for medium-to-low QPS, memory-bound workloads and discuss lossless verifier/rejection-sampling behavior.

Current page also lists multiple proposer methods and known feature/version interactions.

All compatibility details belong in dynamic intelligence.

## vLLM Speculators

Source：

https://docs.vllm.ai/projects/speculators/en/latest/user_guide/algorithms/

Current families include：

- EAGLE-3
- P-EAGLE
- DFlash
- DSpark
- MTP

These show that proposer architecture is evolving beyond a simple standalone tiny model.

## TensorRT-LLM current snapshot

Source：

https://nvidia.github.io/TensorRT-LLM/1.3.0rc20/features/speculative-decoding.html

Current docs describe：

- lightweight proposer
- target single-forward verification
- low-batch speedup emphasis
- draft/target compatibility requirements
- multiple speculative algorithms

Current latest examples also include MTP/EAGLE3/NGRAM paths.

## Original algorithmic guarantee

Primary papers：

- https://arxiv.org/abs/2211.17192
- https://arxiv.org/abs/2302.01318

They establish exact/target-distribution-preserving speculative decoding/sampling through verification and correction.

Practical runtime outputs can still differ token-for-token due to stochasticity/numerics/batching.

## Benchmark snapshot

llama.cpp SPEED-Bench currently reports：

- avg prompt t/s
- avg predicted t/s
- avg latency
- accept_rate

and can compare baseline vs speculative JSON.

This is the preferred next step after Experiment 16 smoke validation.

## Freshness rule

Before future deployment：

1. record llama.cpp/vLLM/TensorRT-LLM version；
2. inspect current speculative docs/flags；
3. verify proposer/target compatibility；
4. re-check metrics；
5. create a new dated intelligence snapshot if changed；
6. preserve this file for historical reproducibility。

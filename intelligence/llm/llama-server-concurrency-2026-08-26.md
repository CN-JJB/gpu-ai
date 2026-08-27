---
snapshot_date: 2026-08-26
type: dynamic-intelligence
topic: llama-server-concurrency
upstream_commit: d7a2074112d27649303fa107eb8c94db1ee435f3
---

# llama-server Concurrency / Metrics Snapshot — 2026-08-26

## Purpose

llama-server flags、metrics、cache behavior 与 API 会演进。

稳定 Lesson 保存概念：

- slots
- queue
- continuous batching
- TTFT / latency / throughput
- KV pressure

本文件保存 current upstream interface snapshot。

Source commit：

d7a2074112d27649303fa107eb8c94db1ee435f3

## Current server features

Source：

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md

Current README lists：

- OpenAI-compatible chat completions/responses/embeddings；
- parallel decoding with multi-user support；
- continuous batching；
- monitoring endpoints；
- streaming mode。

## Current server-slot flags

At this snapshot：

~~~text
-np, --parallel N
~~~

means number of server slots。

~~~text
-cb, --cont-batching
-nocb, --no-cont-batching
~~~

controls continuous/dynamic batching；current default is enabled。

Do not treat this spelling/default as timeless。

## Current cache/context-related flags relevant to this slice

Current docs include：

- --ctx-size
- --cache-type-k
- --cache-type-v
- --kv-offload
- --kv-unified
- --cache-prompt
- --cache-reuse
- --cache-ram
- context checkpoints

At this snapshot：

~~~text
--kv-unified
~~~

uses a single unified KV buffer across sequences and is enabled by default when slot count is auto。

Teaching consequence：

do not infer real KV allocation as a simple permanent slots × per-slot-context formula。

## Current monitoring endpoints

### /slots

GET /slots is enabled by default unless disabled。

Current response exposes per-slot state including：

- id
- task
- n_ctx
- is_processing
- generation/sampling state

### /metrics

Requires --metrics。

Current documented metrics：

~~~text
llamacpp:prompt_tokens_total
llamacpp:prompt_seconds_total
llamacpp:prompt_tokens_seconds

llamacpp:tokens_predicted_total
llamacpp:tokens_predicted_seconds_total
llamacpp:predicted_tokens_seconds

llamacpp:requests_processing
llamacpp:requests_deferred
llamacpp:n_tokens_max
llamacpp:n_decode_total
llamacpp:n_busy_slots_per_decode
~~~

Speculative-decoding metrics also exist but are outside this slice。

## Current OpenAI-compatible API

POST /v1/chat/completions supports synchronous and streaming modes。

Current docs note supported chat templates are required for optimal behavior。

## Official server benchmark

Source：

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/README.md

Current upstream benchmark example uses：

- llama-server
- continuous batching
- metrics
- parallel slots
- configurable concurrent users via k6
- OpenAI chat completions

It records completion/prompt token metrics and compares client/server metrics。

## SPEED-Bench client

Source：

https://github.com/ggml-org/llama.cpp/blob/master/tools/server/bench/speed-bench/README.md

Current client can：

- select concurrency
- save raw JSON
- report avg prompt t/s
- report avg predicted t/s
- report average client latency

Current source also reads response usage/timings separately from wall latency。

## Experiment 12 design decision

The course does not require k6/datasets for the first concurrency lab。

Instead it uses a Python-standard-library localhost probe that：

- sends OpenAI-compatible streaming requests；
- measures first non-empty SSE delta；
- measures response latency；
- polls /metrics；
- saves raw JSON。

This keeps hardware/software prerequisites lower。

For serious serving benchmarks, move to upstream k6/SPEED-Bench or another controlled load generator later。

## Freshness rule

Before using Experiment 12 in a future session：

~~~bash
llama-server --version
llama-server --help
~~~

Then check current：

- server README
- /metrics names
- /slots schema

If changed, create a new dated snapshot rather than silently rewriting historical Evidence。

---
date: 2026-08-26
type: course-build-record
---

# First reproducible local LLM deployment slice completed

第七个 bounded slice 完成：

Research → Reference → HTML Lesson → Real-run Lab → Environment collector → Expected structural outcomes → Evidence template → Dynamic CLI snapshot → Resources update → Learning update。

## Built artifacts

- research/llm/0003-first-local-llm-deployment.md
- reference/llm/llama-cpp-first-run-checklist.md
- lessons/07-local-inference/01-first-local-llm.html
- labs/experiments/10-first-local-llm-run/README.md
- labs/experiments/10-first-local-llm-run/collect-env.sh
- labs/experiments/10-first-local-llm-run/EXPECTED.md
- examples/evidence/experiment-07-first-local-llm-template.md
- intelligence/llm/llama-cpp-cli-2026-08-26.md
- resources/RESOURCES.md
- learning/CURRENT.md

## Why llama.cpp first

The choice is pedagogical, not ideological.

One upstream runtime gives a common migration path across:
- CPU
- NVIDIA CUDA
- AMD HIP
- Apple Metal

while keeping GGUF artifacts, CLI, server and benchmark tooling in one ecosystem.

This makes CPU fallback a real course path rather than a separate toy.

## Four identities required before performance claims

Every first run now records:

1. runtime build/version
2. discovered/actual execution device
3. exact model artifact SHA256
4. execution configuration

This prevents “same model/same GPU” comparisons that actually used different quant files or backend builds.

## First success is separated from benchmark

Current llama.cpp has automatic device-memory fitting behavior.

The course allows this for first success because avoiding OOM is useful.

For A/B benchmark:
- actual context
- GPU layers
- threads
- KV type
- token counts

must be fixed and recorded.

This turns convenience into a controlled methodology rather than hidden confounder.

## PP/TG connect architecture to inference

llama-bench officially separates:

- prompt processing (PP)
- text generation (TG)

The course maps these approximately to:
- prefill-style
- decode-style

and explicitly records that llama-bench excludes tokenization/sampling time.

This preserves the distinction between backend throughput and full serving latency.

## CPU baseline is intentional

CPU-only completion verifies:
- artifact integrity
- loader/tokenizer
- runtime
- benchmark/evidence pipeline

GPU acceleration is then a migration/comparison, not a prerequisite.

## Evidence strategy

No fake benchmark numbers are stored.

Experiment 10 provides:
- collect-env.sh
- raw JSON requirement
- exact artifact hash
- a template marked `template-not-result`

A learner's real run becomes the first actual performance Evidence.

## Dynamic interface separation

Current CLI/build flags are recorded under:
`intelligence/llm/llama-cpp-cli-2026-08-26.md`

Stable Lesson teaches concepts such as:
- GPU layer offload
- auto-fit vs fixed config
- PP/TG
- context/KV

without treating current flag spelling as timeless.

## Next

Move from single-request CLI to:
server → concurrency → continuous batching → KV pressure → TTFT/inter-token latency/throughput → queueing.

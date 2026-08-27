# Current State

## Project phase

Phase 2 now spans GPU architecture/performance fundamentals through a reproducible local LLM service stack with capacity planning, quantization interpretation, concurrency, prefix KV reuse and speculative decode acceleration.

The course has now begun the single-node multi-GPU slice without treating “two GPUs = twice as fast” as a rule.

## Completed slices

### Slice 01 — GPU evolution
fixed-function → programmable → unified compute → matrix acceleration。

### Slice 02 — GPU execution model
thread → warp/wavefront → SM/CU → scheduler → latency hiding → occupancy。

### Slice 03 — On-chip memory + tiling
registers → shared/LDS → coalescing → reuse → arithmetic intensity。

### Slice 04 — Bandwidth + Roofline
capacity vs bandwidth vs compute → ridge point → memory-/compute-bound → prefill/decode。

### Slice 05 — Local LLM VRAM budget
weights → effective bpw → KV → context × concurrency → headroom/offload。

### Slice 06 — Quantization / format / backend
datatype → quant method → container/representation → runtime/kernel/hardware compatibility。

### Slice 07 — First reproducible local LLM
runtime/device/model identity → CPU baseline → GPU/hybrid offload → PP/TG benchmark。

### Slice 08 — Server concurrency / continuous batching
queue → slots → dynamic active set → TTFT/E2E/throughput → KV pressure。

### Slice 09 — Prefix / Paged KV reuse
ordinary KV → cross-request prefix reuse → prefill/TTFT → block/paged management → finite capacity/eviction/isolation。

### Slice 10 — Speculative Decoding
cheap proposer → draft tokens → target batched verification → accepted prefix/correction → acceptance vs overhead → low-batch speedup opportunity → draft memory/config cost。

Artifacts:
- research/llm/0006-speculative-decoding.md
- reference/llm/speculative-decoding-acceptance-overhead.md
- lessons/10-speculative-decoding/01-draft-verify-acceptance.html
- labs/experiments/15-speculative-acceptance-overhead-model/
- labs/experiments/16-llama-server-speculative-probe/
- examples/evidence/experiment-10-speculative-decoding.md
- intelligence/llm/speculative-decoding-2026-08-26.md
- resources/RESOURCES.md

## Validated knowledge

- speculative decoding targets serial new-token decode steps, not repeated prompt prefill.
- proposer/draft is not the authority; target verification and acceptance/correction determine final target semantics.
- greedy matching-prefix intuition is useful, but stochastic speculative sampling needs correct rejection/correction sampling.
- after a simple draft chain's first rejected token, later draft suffix is conditioned on the wrong history and cannot simply be kept.
- acceptance rate is important but does not by itself determine speedup.
- useful metric is accepted sequence progress relative to proposer + target verification + correction overhead.
- draft length has an optimum; low acceptance can make longer drafts slower than baseline.
- two-model speculation consumes extra weights/KV/runtime memory and can alter target offload/headroom.
- n-gram/history proposers avoid a second model but are strongly workload-dependent.
- modern proposer families include standalone draft models, MTP and target-aware learned/block proposers.
- speculative decoding has more opportunity at low/medium QPS or low batch where target decode is memory-bound/underutilized.
- continuous batching can reduce speculative headroom by already increasing target utilization.
- Prefix Cache, Continuous Batching and Speculative Decoding optimize different work and should be A/B tested independently before stacking.
- theoretical speculative algorithms are designed to preserve the target distribution; practical byte-identical output across stochastic/runtime runs is not the correctness criterion.

## Experiment status

L0 deterministic concept experiments verified:
- 01 unified resource pool
- 02 latency hiding
- 04 GEMM tile reuse
- 06 Roofline
- 08 VRAM budget
- 09 effective bpw
- 11 server slots / continuous batching
- 13 prefix-cache capacity / eviction
- 15 speculative acceptance / overhead

Real-run paths ready:
- 03 occupancy sensitivity
- 05 naive vs tiled GEMM
- 07 arithmetic-intensity sweep
- 10 first local LLM
- 12 server concurrency
- 14 cold/warm prefix cache
- 16 baseline vs speculative llama-server

Experiment 16 has a low-dependency n-gram path plus an optional compatible two-model draft path and current speculative metric counters. No real target/draft performance data is fabricated.

## Active Slice 11 — Single-node multi-GPU / interconnect

Research + reference 已完成：
- research/gpu/0005-multi-gpu-interconnect-scaling.md
- reference/gpu/multi-gpu-split-interconnect.md

当前继续完成 Lesson / Experiments / Evidence / Intelligence。

主线：

**one GPU limit → model/layer split vs tensor split → PCIe / NVLink / vendor interconnect → synchronization/data movement → capacity aggregation → throughput/latency → scaling efficiency**

目标是回答：

> 两张便宜 GPU 的显存为什么有时“能合起来放模型”，但速度不等于一张双倍显存/双倍算力的卡？什么时候 PCIe/互联会成为新的 Roofline？

重点把：
- Slice 04 bandwidth/Roofline；
- Slice 05 capacity/offload；
- Slice 07 llama.cpp split/offload；
- serving decode workload；

汇合成真实垃圾佬多卡判断。

## Next actions

1. Write the stable HTML Lesson for capacity aggregation, layer split, tensor split, P2P and interconnect roof.
2. Build L0 experiment 17: compute + communication + sync → scaling efficiency crossover.
3. Build real experiment 18: exact topology/P2P Evidence → one-GPU PP/TG baseline → two-GPU split PP/TG.
4. Add experiment-11 Evidence template and current topology/tool intelligence.
5. Update learning record after the slice is complete.
6. Keep current card prices/model compatibility in intelligence, not stable Lesson.

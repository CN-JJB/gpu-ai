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

### Slice 12 — Attention IO / Online Softmax / FlashAttention

attention math → N×N materialization → HBM IO → tiling → online stable softmax → fused exact attention → GPU work partition。

Artifacts:
- research/gpu/0006-attention-io-online-softmax-flashattention.md
- reference/gpu/attention-io-online-softmax.md
- lessons/12-attention-kernels/01-io-aware-flashattention.html
- labs/experiments/19-attention-online-softmax-io-model/
- labs/experiments/20-real-sdpa-backend-probe/
- examples/evidence/experiment-12-attention-io.md
- intelligence/gpu/attention-backends-2026-08-27.md
- learning/records/2026-08-27-attention-io-slice.md

L0 online-softmax correctness verified; real backend probe contains no fabricated GPU timings.

### Slice 13 — Matrix units / precision / TOPS

storage format → matrix input datatype → accumulator datatype → matrix peak → utilization → memory roof → LLM PP/TG。

Artifacts:
- research/gpu/0007-matrix-units-precision-tops.md
- reference/gpu/matrix-units-precision-tops.md
- lessons/13-matrix-units/01-precision-accumulator-tops.html
- labs/experiments/21-tops-vs-roofline-model/
- labs/experiments/22-real-matmul-shape-precision/
- examples/evidence/experiment-13-matrix-units-precision.md
- intelligence/gpu/matrix-units-precision-2026-08-27.md
- learning/records/2026-08-27-matrix-units-precision-slice.md

L0 synthetic Roofline verified; real shape/precision probe is ready with no fake INT4 path.

### Slice 14 — NVIDIA architecture generation spine

Tesla/G80 → Fermi → Kepler → Maxwell → Pascal → Volta → Turing → Ampere → Ada/Hopper → Blackwell。

Artifacts:
- research/gpu/0008-nvidia-architecture-generation-spine.md
- reference/gpu/nvidia-generation-spine.md
- lessons/14-nvidia-architecture/01-tesla-fermi-kepler.html
- lessons/14-nvidia-architecture/02-maxwell-pascal.html
- lessons/14-nvidia-architecture/03-volta-turing.html
- lessons/14-nvidia-architecture/04-ampere-ada.html
- lessons/14-nvidia-architecture/05-hopper-blackwell.html
- labs/experiments/23-nvidia-generation-feature-traps/
- labs/experiments/24-real-nvidia-capability-inventory/
- examples/evidence/experiment-14-nvidia-generation-spine.md
- intelligence/gpu/nvidia-generation-support-2026-08-27.md
- learning/records/2026-08-27-nvidia-architecture-spine.md

L0 lineage assertions verified 10/10. Real NVIDIA inventory path is ready. Current CUDA/driver lifespan stays in dynamic intelligence.

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

## Slice 11 — Single-node multi-GPU / interconnect — completed

Completed artifacts:
- research/gpu/0005-multi-gpu-interconnect-scaling.md
- reference/gpu/multi-gpu-split-interconnect.md
- lessons/11-multi-gpu/01-capacity-split-interconnect.html
- labs/experiments/17-multi-gpu-interconnect-roof-model/
- labs/experiments/18-real-multi-gpu-scaling/
- examples/evidence/experiment-11-multi-gpu-interconnect.md
- intelligence/gpu/multi-gpu-topology-2026-08-27.md
- learning/records/2026-08-27-multi-gpu-interconnect-slice.md

Stable lesson complete; real two-GPU benchmark path is ready but contains no fabricated hardware results.

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

1. Build the systematic AMD architecture spine using the same causal questions, not NVIDIA terminology.
2. Separate GCN/RDNA consumer lineage from CDNA datacenter/AI lineage.
3. Explain wavefront, CU/WGP, LDS, Infinity Cache/HBM and MFMA/matrix units.
4. Add current ROCm consumer/datacenter support as dynamic intelligence.
5. After AMD, build the Apple Silicon special section: unified memory, Metal GPU and ANE boundaries with local-LLM implications.

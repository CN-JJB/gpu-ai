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

### Slice 15 — AMD architecture generation spine

GCN/Vega → RDNA/CDNA split → RDNA2/CDNA2 → RDNA3/CDNA3 → RDNA4/CDNA4 → current CDNA5 frontier。

Artifacts:
- research/gpu/0009-amd-architecture-generation-spine.md
- reference/gpu/amd-generation-spine.md
- lessons/15-amd-architecture/01-gcn-vega.html
- lessons/15-amd-architecture/02-rdna-rdna2.html
- lessons/15-amd-architecture/03-cdna-cdna2-cdna3.html
- lessons/15-amd-architecture/04-rdna3-rdna4-cdna4-cdna5.html
- labs/experiments/25-amd-generation-terminology-traps/
- labs/experiments/26-real-amd-rocm-inventory/
- examples/evidence/experiment-15-amd-generation-spine.md
- intelligence/gpu/amd-rocm-generation-support-2026-08-27.md
- learning/records/2026-08-27-amd-architecture-spine.md

L0 terminology/lineage assertions verified 12/12. Real gfx-target/ROCm inventory path ready. ROCm support is kept dynamic and exact-SKU specific.

### Slice 16 — Apple Silicon / Unified Memory / Metal / Neural Engine

SoC → unified memory → Metal GPU SIMD/threadgroup → GPU vs Neural Engine → MLX → M1→M5 GPU evolution。

Artifacts:
- research/gpu/0010-apple-silicon-unified-memory-metal-ane.md
- reference/gpu/apple-silicon-unified-memory-metal.md
- lessons/16-apple-silicon/01-unified-memory-is-not-vram.html
- lessons/16-apple-silicon/02-metal-gpu-simd-threadgroup.html
- lessons/16-apple-silicon/03-m1-to-m5-gpu-ane-mlx.html
- labs/experiments/27-apple-unified-memory-budget-model/
- labs/experiments/28-real-apple-metal-mlx-inventory/
- examples/evidence/experiment-16-apple-silicon.md
- intelligence/gpu/apple-silicon-metal-mlx-2026-08-27.md
- learning/records/2026-08-27-apple-silicon-slice.md

L0 capacity/bandwidth roof verified. Real experiment directly queries Metal unified-memory and SIMD-group properties. M5 tensor-path integration remains dynamic intelligence.

### Slice 17 — Intel Xe / Arc / XMX / oneAPI

EU-era graphics → Xe-LP → Xe-HPG/Alchemist → Xe2/Battlemage；Vector Engine → Xe-Core → XMX；SYCL/oneAPI → Level Zero → local LLM backend。

Artifacts:
- research/gpu/0011-intel-xe-arc-xmx-oneapi.md
- reference/gpu/intel-xe-arc-xmx.md
- lessons/17-intel-xe/01-eu-xe-core-xmx.html
- lessons/17-intel-xe/02-arc-oneapi-llm.html
- labs/experiments/29-intel-xe-terminology-traps/
- labs/experiments/30-real-intel-xpu-sycl-inventory/
- examples/evidence/experiment-17-intel-xe.md
- intelligence/gpu/intel-oneapi-xpu-2026-08-27.md
- learning/records/2026-08-27-intel-xe-slice.md

L0 terminology checker verified 10/10. Real experiment checks SYCL/Level Zero, torch.xpu and llama.cpp visibility separately.

### Slice 18 — Cross-vendor used-hardware decision framework

Workload → Fit Gate → Software Gate → PP/TG/interconnect roofs → comparable Evidence → TCO → secondhand risk → action.

Artifacts:
- research/hardware/0001-cross-vendor-used-hardware-decision-framework.md
- reference/hardware/cross-vendor-decision-card.md
- lessons/18-hardware-decision/01-fit-support-roofs-tco.html
- labs/experiments/31-scenario-hardware-decision-model/
- labs/experiments/32-real-used-hardware-candidate-dossier/
- examples/evidence/experiment-18-cross-vendor-decision.md
- learning/records/2026-08-27-cross-vendor-hardware-decision.md

No universal score is used. Capacity/software are hard gates; ranking is scenario-specific.

### Slice 19 — China secondhand GPU market methodology

Raw listing → exact SKU/VRAM → condition/modification cohort → ASK/SOLD/QUOTE state → deduplicate/outlier cleanup → median/Q1-Q3 → evidence grade → candidate dossier。

Artifacts:
- research/market/0001-china-secondhand-gpu-market-methodology.md
- reference/market/china-secondhand-gpu-sampling-card.md
- lessons/19-secondhand-market/01-price-is-not-a-number.html
- labs/experiments/33-secondhand-market-normalization/
- labs/experiments/34-real-secondhand-market-snapshot/
- examples/evidence/experiment-19-china-secondhand-market.md
- intelligence/market/china-used-gpu-market-2026-08-27.md
- learning/records/2026-08-27-china-secondhand-gpu-market.md

Current snapshot intentionally does not claim a direct Xianyu sold median because the normalized item-level evidence is insufficient.

### Slice 20 — Used GPU transaction / acceptance verification

Seller evidence → unboxing/serial → identity → baseline errors → memory integrity → LLM workload → thermals → after-test errors → ACCEPT/DISPUTE。

Artifacts:
- research/hardware/0002-used-gpu-transaction-verification.md
- reference/hardware/used-gpu-acceptance-checklist.md
- lessons/20-used-gpu-verification/01-before-pay-after-arrival.html
- labs/experiments/35-seller-evidence-quality/
- labs/experiments/36-real-used-gpu-acceptance/
- examples/evidence/experiment-20-used-gpu-verification.md
- intelligence/hardware/used-gpu-acceptance-tools-2026-08-27.md
- learning/records/2026-08-27-used-gpu-verification.md

Default real acceptance collector is read-only/non-destructive. Seller evidence uses C0–C4; no single stress test is treated as complete health proof.

### Slice 21 — Max-buy-price / candidate watchlist

Hard gates → total ownership budget → non-GPU TCO/reserves → personal sticker ceiling → market/condition evidence → SKIP / NEEDS EVIDENCE / WATCH / BUY-CANDIDATE / KEEP。

Artifacts:
- research/market/0002-max-buy-price-watchlist.md
- reference/market/max-buy-price-watchlist-card.md
- lessons/21-watchlist/01-max-buy-price.html
- labs/experiments/37-max-buy-price-model/
- labs/experiments/38-real-candidate-watchlist/
- examples/evidence/experiment-21-max-buy-price-watchlist.md
- learning/records/2026-08-27-max-buy-price-watchlist.md

Watchlist never auto-purchases. Cheap candidates remain blocked by hard gates/evidence gates.

### Slice 22 — Capstone controlled optimization

Hardware profile → runtime/model identity → baseline PP/TG/telemetry → bottleneck hypothesis → ONE semantic variable → validated A/B → interpretation。

Artifacts:
- research/system/0001-capstone-measure-diagnose-optimize.md
- reference/system/capstone-bottleneck-decision-tree.md
- lessons/22-capstone/01-measure-diagnose-one-variable.html
- labs/experiments/39-capstone-bottleneck-diagnosis/
- labs/experiments/40-real-llm-capstone/
- examples/evidence/experiment-22-capstone-controlled-ab.md
- learning/records/2026-08-27-capstone-controlled-ab.md

L0 bottleneck diagnosis verified 7/7. Real manifest validator freezes identity and requires one semantic config difference. No real PP/TG values are fabricated.

### Slice 23 — Four-vendor capstone runbooks

NVIDIA CUDA / AMD ROCm-HIP / Apple Metal / Intel SYCL 使用同一 controlled-A/B 方法，但保留各自 device/memory/support 语义。

Artifacts:
- research/system/0002-vendor-capstone-runbooks.md
- reference/system/vendor-capstone-runbooks.md
- lessons/23-vendor-capstone/
- labs/experiments/41-vendor-capstone-preflight/
- examples/evidence/experiment-23-vendor-capstone-runbooks.md
- learning/records/2026-08-27-vendor-capstone-runbooks.md

Current llama.cpp build/device entry points were verified against pinned upstream before writing. All vendor paths reuse Experiment 40.

### Slice 24 — Decoder-only Transformer dataflow

Token IDs → embedding → repeated pre-norm decoder blocks → final norm → LM head/logits；Prefill [B,T,d] 与 one-token Decode [B,1,d] + historical KV 被拆成两种 shape/workload regime。

Artifacts:
- research/llm/0007-decoder-only-transformer-dataflow.md
- reference/llm/decoder-only-block-shapes.md
- lessons/24-transformer-anatomy/01-decoder-only-prefill-decode.html
- labs/experiments/42-decoder-transformer-shape-flow/
- labs/experiments/43-real-model-config-anatomy/
- examples/evidence/experiment-24-decoder-transformer-dataflow.md
- learning/records/2026-08-27-decoder-transformer-dataflow.md

L0 tensor/KV arithmetic verified. Real config inspector flags MoE/sliding/per-layer features instead of forcing a dense homogeneous baseline.

### Slice 25 — RMSNorm / residual / RoPE

RMSNorm scale control → pre-norm residual update path → position-dependent RoPE rotation on Q/K → KV position identity → context-scaling boundary。

Artifacts:
- research/llm/0008-rmsnorm-residual-rope.md
- reference/llm/rmsnorm-residual-rope.md
- lessons/25-rmsnorm-rope/01-rmsnorm-residual-rope.html
- labs/experiments/44-rmsnorm-scale-model/
- labs/experiments/45-rope-relative-position-model/
- examples/evidence/experiment-25-rmsnorm-residual-rope.md
- learning/records/2026-08-27-rmsnorm-residual-rope.md

L0 RMSNorm and RoPE numeric properties verified.

### Slice 26 — MHA / MQA / GQA

Hq query heads vs Hkv KV heads → projection widths → grouped sharing → KV bytes/token → long-context/concurrency/decode-bandwidth consequences。

Artifacts:
- research/llm/0009-mha-mqa-gqa.md
- reference/llm/mha-mqa-gqa-kv.md
- lessons/26-attention-heads/01-mha-mqa-gqa.html
- labs/experiments/46-mha-gqa-mqa-kv-model/
- labs/experiments/47-real-model-attention-config-compare/
- examples/evidence/experiment-26-mha-mqa-gqa.md
- learning/records/2026-08-27-mha-mqa-gqa.md

Default L0 model verified: MHA/GQA-8/MQA 32k FP16 KV = 16/4/0.5 GiB.

### Slice 27 — SwiGLU / dense FFN

Gate/up/down three-matrix gated FFN → intermediate_size → dense parameter/storage share → prefill large-GEMM vs decode small-row weight streaming。

Artifacts:
- research/llm/0010-swiglu-dense-ffn.md
- reference/llm/swiglu-ffn-weight-traffic.md
- lessons/27-swiglu-ffn/01-gate-up-down.html
- labs/experiments/48-dense-swiglu-ffn-model/
- labs/experiments/49-real-model-ffn-structure-compare/
- examples/evidence/experiment-27-swiglu-dense-ffn.md
- learning/records/2026-08-27-swiglu-dense-ffn.md

Default L0 arithmetic verified: FFN/attention projection ratio 2.015625× for d4096/d_ff11008 classic-MHA baseline.

### Slice 28 — Mixture of Experts

Router → top-k experts → active expert compute → total expert residence → batching/reuse → routing imbalance → expert-parallel interconnect。

Artifacts:
- research/llm/0011-mixture-of-experts-local-inference.md
- reference/llm/moe-total-active-resident-traffic.md
- lessons/28-moe/01-router-active-resident-traffic.html
- labs/experiments/50-moe-active-weight-reuse-model/
- labs/experiments/51-real-moe-config-inspector/
- examples/evidence/experiment-28-moe-local-inference.md
- learning/records/2026-08-27-moe-local-inference.md

Default L0 expert accounting and balanced/skewed routing examples verified.

### Slice 29 — Model Architecture Dossier

Real config/artifact → attention/KV/FFN/MoE structure → weight/artifact planning value → asymmetric lower-bound capacity verdict → PP/TG hypotheses → real benchmark handoff。

Artifacts:
- research/llm/0012-model-architecture-dossier.md
- reference/llm/model-architecture-dossier-card.md
- lessons/29-model-dossier/01-config-to-hardware-hypothesis.html
- labs/experiments/52-model-architecture-dossier-model/
- labs/experiments/53-real-model-architecture-dossier/
- examples/evidence/experiment-29-model-architecture-dossier.md
- learning/records/2026-08-27-model-architecture-dossier.md

Synthetic dense/MoE lower-bound cases checked. Formula fit is never upgraded to confirmed runtime fit.

### Slice 30 — Sliding / hybrid / latent KV

Homogeneous full KV → sliding/local rolling cache → hybrid per-layer sum → compressed/latent cached-state width → architecture-specific exactness。

Artifacts:
- research/llm/0013-modern-kv-attention-architectures.md
- reference/llm/sliding-hybrid-latent-kv.md
- lessons/30-modern-kv/01-sliding-hybrid-latent.html
- labs/experiments/54-sliding-hybrid-kv-model/
- labs/experiments/55-real-attention-kv-architecture/
- examples/evidence/experiment-30-modern-kv-architectures.md
- learning/records/2026-08-27-modern-kv-architectures.md

Default L0 full/local/hybrid KV arithmetic verified at 32k and 128k.

### Slice 31 — Tokenizer / chat template / sampling

Messages → model-specific Jinja/chat serialization → special-token policy → exact token IDs → logits → ordered sampler chain → output token/text。

Artifacts:
- research/llm/0014-tokenizer-chat-template-sampling.md
- reference/llm/prompt-tokenizer-sampling-identity.md
- lessons/31-tokenizer-sampling/01-template-token-logit-sampler.html
- labs/experiments/56-chat-template-special-token-model/
- labs/experiments/57-real-prompt-token-identity/
- examples/evidence/experiment-31-tokenizer-chat-template-sampling.md
- learning/records/2026-08-27-tokenizer-chat-template-sampling.md

Toy template/token-count and duplicate-BOS behavior verified. Real prompt path hashes messages/template/rendered/token IDs.

### Slice 32 — Quality Gate

Logits → correct-token probability → NLL → cross entropy → perplexity → target-task fixtures → performance/quality tradeoff。

Artifacts:
- research/llm/0015-quality-gate-perplexity.md
- reference/llm/quality-gate-card.md
- lessons/32-quality-gate/01-cross-entropy-perplexity.html
- labs/experiments/58-perplexity-math-model/
- labs/experiments/59-real-quality-gate/
- examples/evidence/experiment-32-quality-gate.md
- learning/records/2026-08-27-quality-gate.md

L0 CE/PPL arithmetic verified. Real quality lab contains no fabricated model scores.

### Slice 33 — Benchmark / Workload Manifest

Fixed protocol + semantic variant blocks + audit records → one declared experimental intervention → validator → hashed Evidence Packet。

Artifacts:
- reference/system/benchmark-workload-manifest.md
- lessons/33-benchmark-manifest/01-one-semantic-variable.html
- labs/experiments/60-benchmark-manifest-validator/
- labs/experiments/61-real-benchmark-evidence-packet/
- examples/evidence/experiment-33-benchmark-workload-manifest.md
- learning/records/2026-08-27-benchmark-workload-manifest.md

Synthetic quant-block PASS and hidden prompt-change FAIL paths were self-checked.

### Slice 34 — Serving Workload / SLO

Request arrivals + prompt/output lengths + slots/batching/cache → TTFT / ITL / E2E → request/token throughput → p50/p95/p99 → SLO。

Artifacts:
- research/llm/0016-serving-workload-slo.md
- reference/llm/serving-workload-slo.md
- lessons/34-serving-slo/01-ttft-itl-tail-throughput.html
- labs/experiments/62-serving-tail-latency-trace/
- labs/experiments/63-real-llama-server-serving-trace/
- examples/evidence/experiment-34-serving-workload-slo.md
- learning/records/2026-08-27-serving-workload-slo.md

Synthetic tail-latency/SLO arithmetic verified. Real collector syntax-checked.

### Slice 35 — Serving Capacity / Little's Law

Throughput λ + time W → average occupancy L, with explicit system/queue/active boundaries → peak comparison → KV planning caveats。

Artifacts:
- research/llm/0017-serving-capacity-littles-law.md
- reference/llm/serving-capacity-littles-law.md
- lessons/35-serving-capacity/01-littles-law-slots-kv.html
- labs/experiments/64-littles-law-trace-model/
- labs/experiments/65-real-serving-capacity/
- examples/evidence/experiment-35-serving-capacity-littles-law.md
- learning/records/2026-08-27-serving-capacity-littles-law.md

Synthetic system/active/queue Little's-Law identities and peak values verified.

### Slice 36 — Overload / Admission Control

Offered load > capacity → queue growth → bounded admission/rejection → retry amplification → backoff → SLO/resource-aware admission。

Artifacts:
- research/llm/0018-overload-admission-retry.md
- reference/llm/overload-admission-control.md
- lessons/36-overload-admission/01-queue-reject-retry.html
- labs/experiments/66-overload-retry-model/
- labs/experiments/67-real-overload-observation/
- examples/evidence/experiment-36-overload-admission-retry.md
- learning/records/2026-08-27-overload-admission-retry.md

Synthetic queue/retry scenarios verified. Real lab is bounded and restricted to owned/authorized systems.

### Slice 37 — Multi-Tenant Fairness

Request count → token/resource cost → per-tenant concurrency/quota → fairness under contention → work-conserving borrowing → per-tenant latency/resource report。

Artifacts:
- research/llm/0019-multitenant-fairness-quotas.md
- reference/llm/multitenant-fairness-quotas.md
- lessons/37-multitenant-fairness/01-slots-quotas-borrowing.html
- labs/experiments/68-multitenant-fairness-model/
- labs/experiments/69-real-tenant-serving-report/
- examples/evidence/experiment-37-multitenant-fairness.md
- learning/records/2026-08-27-multitenant-fairness.md

Synthetic FIFO/strict-cap/fair-borrowing scheduler values verified.

### Slice 38 — Service Exposure / Privacy / Auth

Loopback/LAN/wildcard scope → auth vs TLS vs CORS → endpoint/log privacy → host-action tool boundary → model-license separation。

Artifacts:
- research/llm/0020-service-exposure-privacy-auth.md
- reference/llm/service-exposure-privacy-auth.md
- lessons/38-service-exposure/01-bind-auth-tls-privacy.html
- labs/experiments/70-service-exposure-config-linter/
- labs/experiments/71-real-service-exposure-audit/
- examples/evidence/experiment-38-service-exposure-privacy-auth.md
- learning/records/2026-08-27-service-exposure-privacy-auth.md

Synthetic exposure findings verified. Real audit remains loopback-only/read-only and stores no secrets.

### Slice 39 — Operational Reliability / Recovery

Process liveness → listener → health readiness → smoke inference → warm steady state → restart identity/recovery。

Artifacts:
- research/llm/0021-operational-reliability-recovery.md
- reference/llm/operational-reliability-recovery.md
- lessons/39-operational-reliability/01-readiness-restart-recovery.html
- labs/experiments/72-lifecycle-readiness-model/
- labs/experiments/73-real-local-restart-readiness/
- examples/evidence/experiment-39-operational-reliability-recovery.md
- learning/records/2026-08-27-operational-reliability-recovery.md

Synthetic lifecycle timing verified. Real restart lab is forced-loopback and manages only its own child process.

### Slice 40 — Safe Upgrade / Rollback

Known-good release identity → predeclared gate policy → candidate readiness/performance/quality/SLO → ACCEPT or exact identity rollback → rollback readiness/smoke。

Artifacts:
- research/llm/0022-safe-upgrade-rollback.md
- reference/llm/safe-upgrade-rollback.md
- lessons/40-safe-upgrade/01-release-gates-rollback.html
- labs/experiments/74-release-gate-model/
- labs/experiments/75-real-release-gate-rollback/
- examples/evidence/experiment-40-safe-upgrade-rollback.md
- learning/records/2026-08-27-safe-upgrade-rollback.md

Synthetic ACCEPT/ROLLBACK paths verified. Real gate blocks missing/invalid numeric evidence.

### Slice 41 — Observability / Incident Diagnosis

Client latency/traffic/errors + server saturation + GPU telemetry + logs → shared timeline → hypothesis → controlled confirmation。

Artifacts:
- research/llm/0023-observability-incident-diagnosis.md
- reference/llm/observability-incident-diagnosis.md
- lessons/41-observability/01-symptom-timeline-hypothesis.html
- labs/experiments/76-incident-diagnosis-cases/
- labs/experiments/77-real-incident-evidence/
- examples/evidence/experiment-41-observability-incident-diagnosis.md
- learning/records/2026-08-27-observability-incident-diagnosis.md

Queue/thermal/high-stable-VRAM synthetic cases verified. Real collector is bounded/read-only/loopback-only.

### Slice 42 — Power / Energy Efficiency

Watts → joules over time → J/token / tokens/J → idle baseline → board vs wall power → electricity/TCO。

Artifacts:
- research/llm/0024-power-energy-efficiency.md
- reference/llm/power-energy-efficiency.md
- lessons/42-power-energy/01-watts-joules-per-token.html
- labs/experiments/78-power-energy-model/
- labs/experiments/79-real-nvidia-energy/
- examples/evidence/experiment-42-power-energy-efficiency.md
- learning/records/2026-08-27-power-energy-efficiency.md

Synthetic energy arithmetic and trapezoidal-integration sanity case verified. Real NVIDIA path remains read-only.

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

1. Build storage/model-loading slice.
2. Separate model artifact bytes, storage read bandwidth, OS page cache and GPU upload/load time.
3. Compare cold vs warm model startup without claiming disk bandwidth determines steady TG.
4. Teach mmap/page-fault intuition and why page cache can hide storage differences on repeat runs.
5. Add a read-only local file-read/model-startup evidence packet.

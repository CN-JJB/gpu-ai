# Visual & Comprehension Audit

Status: ACTIVE — post-freeze teaching maintenance

## Why this audit exists

The stable textbook already passed the substantive self-study contract. This pass asks a different question: **can the learner see the mechanism, not merely read it?**

The target learner remains a PC enthusiast with no assumed Linux, Python, CUDA, ML, electronics, or advanced-math prerequisite.

## Baseline — 2026-08-29

A connector scan of all 62 stable lesson HTML pages found:

- lesson HTML: 62
- <img>: 0
- <svg>: 0
- <figure>: 0
- interactive controls: 1 page (Lesson 01)
- shared visual components in assets/: one existing pipeline-balance simulator

This is not a claim that the lessons are textually poor. It is evidence that the visual explanation layer is much thinner than the written layer.

## Review rubric

Every lesson is reviewed on five axes:

1. **Explanation depth** — enough mechanism to predict cause/effect, not just definitions.
2. **Beginner legibility** — intuition before vendor vocabulary; hidden prerequisites recovered.
3. **Worked reasoning** — numbers, traces, command/output anatomy, or concrete scenarios.
4. **Visual necessity** — whether the concept is materially easier with a diagram, timeline, state view, plot, animation, or calculator.
5. **Evidence boundary** — visuals must distinguish conceptual models, documented architecture, and measured learner-owned evidence.

## Visual forms we will use

Prefer the smallest form that actually teaches the mechanism:

- static SVG for architecture, hierarchy, dataflow, topology, and comparison;
- interactive HTML/JS for parameter sweeps, queues, budgets, scheduling, and bottleneck transitions;
- timelines for latency, serving, upgrade, incident, and thermal behavior;
- state diagrams for cache, admission control, reliability, and evidence gates;
- plots for Roofline, tail latency, power/energy, and sustained-performance drift;
- official/primary-source visuals when they add historical or product-specific evidence and can be linked/attributed safely;
- self-authored diagrams when an official figure is too dense, unstable, or licensing/hotlinking would be fragile.

A decorative image does not satisfy this audit.

## Priority

### P0 — mechanism is inherently spatial, temporal, or quantitative

- 01–05: evolution, scheduler, memory hierarchy, Roofline, VRAM budget
- 08–13: batching, KV layout, speculative decode, multi-GPU, FlashAttention, matrix precision
- 24–30: Transformer dataflow, RoPE, MHA/GQA/MQA, SwiGLU, MoE, modern KV
- 34–45: SLO/queue/capacity/fairness/exposure/recovery/upgrade/observability/power/storage/RAM/thermal
- 46–49: used-GPU acceptance, PSU, whole-machine gates, graduation design review

### P1 — timeline/comparison/reference visuals strongly improve recall

- 14–17 architecture generations
- 18–23 hardware decision / market / vendor capstones
- 31–33 tokenizer, quality, benchmark identity

## Batch 01 detailed review

| Lesson | Depth | Beginner clarity | Main visual gap | Action |
|---|---|---|---|---|
| 01 GPU evolution | strong | strong | history is causal but mostly text; unified-pool simulator already useful | add self-authored evolution timeline SVG; retain simulator |
| 02 warp/scheduler | strong | good | latency hiding is temporal and hard to internalize from prose/table | add resident-group scheduler simulator with issue/idle timeline |
| 03 memory/tiling | strong | good | hierarchy and reuse are spatial; ASCII chains hide locality | add memory-hierarchy + reuse SVG |
| 04 Roofline | strong | good | core concept is literally a graph but page has no graph | add interactive Roofline explorer with AI/ridge/roof transition |
| 05 VRAM budget | strong | strong | formulas are useful but learner must mentally integrate many variables | add interactive budget calculator with weights/KV/reserve/headroom |

## Batch 02 detailed review — Lessons 06–13

| Lesson | Depth | Beginner clarity | Main visual/comprehension need | Accepted implementation |
|---|---|---|---|---|
| 06 Quantization | strong | strong | nominal bit-width, metadata overhead, mixed precision and backend support are easy to collapse into one label | interactive effective-bpw calculator; explicitly labels the model as a teaching approximation |
| 07 First local inference | strong | strong | learners need to distinguish build support, device discovery, placement, kernel execution and reproducible evidence | local-inference evidence-chain SVG |
| 08 Local serving | strong | good | queue/slot/continuous-batching behavior is temporal and difficult to infer from static prose | interactive static-vs-continuous admission timeline with slots and first-wait metrics |
| 09 Prefix/KV reuse | strong | good | cache capacity, working set, hit/miss and eviction are stateful | interactive LRU prefix-cache state trace |
| 10 Speculative decoding | strong | good | draft length × acceptance × round cost has a non-obvious optimum | interactive acceptance/draft explorer with expected progress and speedup ceiling |
| 11 Multi-GPU | strong | good | aggregate capacity and communication boundary must be spatially separated | multi-GPU split/interconnect SVG comparing layer split, tensor parallel and replicas |
| 12 Attention kernels | strong | good | exact attention vs HBM materialization is fundamentally an I/O/dataflow story | naive-vs-tiled attention I/O SVG with online-softmax state |
| 13 Matrix units | strong | good | model storage dtype, runtime operand dtype, matrix fast path and accumulator precision are frequently conflated | matrix-precision execution-path SVG |

### Batch 02 comprehension findings

- Lessons 06–13 are not thin on prose; the main problem was **mechanisms whose state changes over time or across memory/device boundaries**.
- The strongest additions are interactive where the learner benefits from sweeping a parameter and watching a state transition (06, 08, 09, 10), and static SVG where topology/dataflow is the key mental model (07, 11, 12, 13).
- Lesson 07 is not a P0 architecture topic, but the evidence-chain SVG materially improves the course's central epistemic rule: a successful text response does not by itself prove GPU acceleration.
- No external screenshot was required in this batch. Primary-source links remain the evidence layer; self-authored visuals are used for explanation so the course does not depend on unstable hotlinks or unclear image licensing.
- No teaching calculator or diagram is promoted to benchmark evidence. Real performance claims remain tied to learner-owned experiment artifacts.

## Safety and truth rules

- No generated or synthetic chart is presented as a real GPU benchmark.
- Interactive numbers are labeled teaching models or calculators.
- Architecture diagrams separate conceptual abstraction from vendor-documented block diagrams.
- Remote images are not hotlinked merely for decoration.
- Purchase/release decisions remain human-reviewed.
- Real benchmark rows remain learner-owned evidence.

## Progress

- [x] corpus baseline scan
- [x] Batch 01 manual review
- [x] Batch 01 visual implementation
- [x] Batch 01 link/readiness re-check
- [x] Batch 02 review and implementation — Lessons 06–13
- [x] Batch 02 link/readiness re-check
- [x] Batch 03 review and implementation — Lessons 14–23 architecture/vendor + hardware-decision group
- [x] Batch 04 review and implementation — Lessons 24–33 Transformer/model internals + benchmark identity
- [ ] Batch 05 review and implementation — Lessons 34–45 serving/operations/whole-machine behavior
- [ ] Batch 06 review and implementation — Lessons 46–49 used-GPU/PSU/integration/graduation gates
- [ ] final 62-page visual/comprehension closure audit

## Batch 01 implementation result

Implemented:

- Lesson 01: causal evolution timeline SVG + existing unified-pool simulator retained.
- Lesson 02: resident-group scheduler simulator with issue/idle cycle trace.
- Lesson 03: memory-hierarchy / tile-reuse SVG.
- Lesson 04: interactive two-roof Roofline explorer with ridge-point readout.
- Lesson 05: interactive weights + KV + reserve VRAM budget calculator.
- Global CSS: visual/interactive primitives, mobile-safe code blocks/tables, and constrained `.textbook-upgrade` layout.

Post-edit marker check for Lessons 01–05:

~~~text
Retrieval Practice = 5 / 5
完成证据 = 5 / 5
Primary Sources = 5 / 5
HTML close = 5 / 5
~~~

New assets are local first-party files. No synthetic result is presented as measured evidence.

## Batch 02 implementation result

Accepted as present in the stable course:

- Lesson 06: `assets/components/quant-bpw.js`
- Lesson 07: `assets/diagrams/local-inference-evidence-chain.svg`
- Lesson 08: `assets/components/serving-slots.js`
- Lesson 09: `assets/components/prefix-cache-lru.js`
- Lesson 10: `assets/components/speculative-explorer.js`
- Lesson 11: `assets/diagrams/multi-gpu-split-interconnect.svg`
- Lesson 12: `assets/diagrams/attention-io-naive-vs-tiled.svg`
- Lesson 13: `assets/diagrams/matrix-precision-path.svg`

## Batch 03 detailed review — Lessons 14–23

This group contains 23 HTML pages: NVIDIA 5, AMD 4, Apple 3, Intel 2, hardware decision 1, secondhand market 1, used-GPU verification 1, watchlist 1, measurement capstone 1, and vendor capstones 4.

| Group | Depth | Beginner clarity | Visual finding | Action |
|---|---|---|---|---|
| 14 NVIDIA architecture | strong | good | generation map was useful but reused across all five pages; the first principles of an SM were still mostly prose/ASCII | retain generation map; add a cross-generation SM execution/memory teaching lens |
| 15 AMD architecture | strong | good | branch map explained RDNA/CDNA history, but CU/WGP + wave + scalar/vector + VGPR/LDS resource interaction needed a local mechanism view | retain branch map; add AMD wave/CU/WGP resource teaching lens |
| 16 Apple Silicon | strong | strong | generation map was good for M1→M5, but "unified memory is not VRAM" needed a spatial capacity/data-path picture | add unified-memory LLM data-path/budget SVG |
| 17 Intel Xe | strong | good | naming hierarchy was already visual, but oneAPI/SYCL/Level Zero/application-backend layers were still easy to collapse | add SYCL → runtime → Level Zero → driver → Xe evidence-stack SVG |
| 18 Hardware decision | strong | strong | fit/support/roof/evidence/TCO are naturally gate-like | existing hardware-decision-gates SVG accepted |
| 19 Secondhand market | strong | strong | asking/transaction/condition/freshness only become comparable inside a cohort | existing market-observation-cohort SVG accepted |
| 20 Used-GPU verification | strong | strong | acceptance is procedural and sequential | existing used-gpu-acceptance-flow SVG accepted |
| 21 Watchlist | strong | strong | personal ceiling is quantitative and user-specific | existing interactive max-buy-price calculator accepted; no decorative figure added |
| 22 Measurement capstone | strong | strong | one-variable A/B identity is a comparison-structure problem | existing ab-one-variable-identity SVG accepted |
| 23 Vendor capstones | strong | strong | the same epistemic chain should remain consistent across CUDA/ROCm/Metal/SYCL | shared vendor-evidence-chain SVG accepted across all four pages |

### Batch 03 source check

The new second-layer diagrams were constrained against current primary documentation rather than copied from vendor artwork:

- NVIDIA CUDA Programming Guide: SM scheduling, execution resources, shared/L1 and memory hierarchy;
- AMD ROCm GPU specifications / hardware documentation: wavefront, CU, LDS, VGPR/SGPR and generation-specific memory resources;
- Apple Metal documentation: unified memory, SIMD-group/threadgroup organization and storage modes;
- Intel oneAPI documentation: SYCL device/backend flow, Unified Runtime/Level Zero and Xe/XMX execution path.

The diagrams deliberately omit generation-specific counts unless the lesson text binds them to a documented architecture/SKU. They are labeled as teaching abstractions, not literal floorplans.

## Batch 03 implementation result

Added:

- `assets/diagrams/nvidia-sm-execution-lens.svg`
- `assets/diagrams/amd-wave-cu-memory-lens.svg`
- `assets/diagrams/apple-unified-memory-data-path.svg`
- `assets/diagrams/intel-sycl-runtime-stack.svg`

Inserted into:

- Lesson 14.1 Tesla/Fermi/Kepler
- Lesson 15.1 GCN/Vega
- Lesson 16.1 Unified Memory
- Lesson 17.2 Arc/oneAPI/LLM

Accepted existing visual mechanisms for Lessons 18–23, including the Lesson 21 interactive price-ceiling calculator.

Post-edit marker check for all 23 HTML pages in Lessons 14–23:

~~~text
Retrieval Practice = 23 / 23
完成证据 = 23 / 23
Primary Sources = 23 / 23
HTML close = 23 / 23
visual or interactive teaching surface = 23 / 23
~~~

Lesson 21 intentionally has no static figure because its interactive calculator is the stronger teaching representation.

The next review batch is Lessons 24–33. Priority is dynamic Transformer/model-internal mechanisms: token flow, RoPE rotation, attention-head sharing, SwiGLU gating, MoE routing/load balance, modern KV layouts, tokenizer/sampling probability changes, quality gates and benchmark identity.


## Batch 04 detailed review — Lessons 24–33

| Lesson | Depth | Beginner clarity | Mechanism that must be seen | Accepted surface |
|---|---|---|---|---|
| 24 Transformer anatomy | strong | strong | prefill and decode traverse the same decoder blocks with very different token shapes / KV behavior | `transformer-prefill-decode.svg` |
| 25 RMSNorm / RoPE | strong | good | RoPE position/frequency is a rotation, not a text label or simple additive ID | interactive 2D RoPE rotation explorer |
| 26 MHA / GQA / MQA | strong | strong | query-head count and KV-head sharing must be spatially visible | `mha-gqa-mqa.svg` |
| 27 SwiGLU / FFN | strong | strong | gate/up/down projections and elementwise gating are a dataflow | `swiglu-flow.svg` |
| 28 MoE | strong | good | active experts, resident experts and cross-device traffic are different quantities | `moe-routing.svg` |
| 29 Model dossier | strong | strong | identity/config/artifact/runtime facts feed capacity/performance hypotheses, not conclusions | `model-dossier.svg` |
| 30 Modern KV | strong | good | hybrid local/full attention changes layer-token history scaling; latent KV changes representation | interactive hybrid-KV budget calculator |
| 31 Tokenizer / sampling | strong | strong | temperature reshapes a probability distribution; template/token identity precedes sampling | interactive temperature/softmax distribution |
| 32 Quality gate | strong | strong | performance improvement and quality admission are separate gates | `quality-gate.svg` |
| 33 Benchmark manifest | strong | strong | exact identity, frozen protocol, one semantic variable and raw audit links must stay separate | `benchmark-manifest.svg` |

### Batch 04 comprehension findings

- No new asset was necessary. The strongest teaching surface for every page already existed and matched the concept.
- The three interactive pages are correctly bounded:
  - RoPE is explicitly a 2D intuition slice rather than a literal full-dimensional implementation.
  - Hybrid KV compares history-position factors and explicitly excludes real per-layer head/dtype/allocator details.
  - Temperature holds logits fixed and visualizes only softmax reshaping; it does not pretend to model the entire sampler chain.
- Static diagrams are mechanism-specific rather than decorative: token flow, KV-head sharing, gated FFN flow, expert routing, evidence identity and admission gates.
- This batch demonstrates the preferred rule for the rest of the audit: **do not add a second visual merely because a page has only one; add another only when it teaches a distinct causal mechanism.**

Post-review marker check:

~~~text
visual or interactive teaching surface = 10 / 10
Retrieval Practice = 10 / 10
完成证据 = 10 / 10
Primary Sources = 10 / 10
HTML close = 10 / 10
~~~

The next review batch is Lessons 34–45: serving SLOs, capacity, overload/admission, fairness, exposure, reliability, upgrades, observability, power, storage, host memory and sustained thermal behavior.

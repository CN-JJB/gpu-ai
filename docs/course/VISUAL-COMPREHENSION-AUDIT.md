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
- [ ] Batch 02 review and implementation
- [ ] continue lesson-by-lesson until all 62 pages are reviewed


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

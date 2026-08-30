# Auxiliary Teaching Visual / Comprehension Audit

Status: **ACTIVE — Foundations complete; Experiment/Challenge closure in progress**

Date opened: 2026-08-29

## Scope

This audit extends the completed 62-page Lesson visual/comprehension closure to the auxiliary teaching surfaces that a learner actually follows while doing the course:

- `curriculum/foundations/00–05` — 6 Foundations
- `labs/experiments/01–93` — 93 Experiment README files
- `labs/challenges/01–12` — 12 Challenge README files

The stable Lesson audit remains closed unless a concrete learner-facing defect is found.

## Why this audit exists

A Lesson visual explains a mechanism. An Experiment or Challenge also needs to make execution, observation, decision boundaries, failure states, and Evidence capture easy to follow.

A text-only lab can still be correct while being harder for a beginner to execute safely and interpret correctly.

## Visual rules

A visual counts only when it carries teaching information.

Good uses:

- execution/data-flow diagram;
- experiment timeline;
- one-variable A/B layout;
- topology or memory placement;
- result interpretation / decision gate;
- failure / troubleshooting tree;
- Evidence packet flow;
- safety / stop-condition gate.

A decorative image does not count.

When an existing Lesson diagram explains the same mechanism, reuse it. Create a new asset only when the lab introduces a distinct execution, observation, safety, or decision mechanism.

Synthetic/example diagrams must never be presented as measured benchmark data.

## Baseline

Baseline audit was performed after Foundation visual additions at repository head:

`881156c22ea92322136064890ee8d0078fbd700c`

### Foundations

- 6 / 6 reviewed.
- 6 / 6 now have a local teaching visual.
- New assets:
  - `foundation-course-evidence-loop.svg`
  - `foundation-shell-audit-chain.svg`
  - `foundation-json-hash-evidence-layers.svg`
  - `foundation-units-roof-estimation.svg`
  - `foundation-claim-source-chain.svg`
  - `foundation-safety-escalation-gates.svg`

### Experiments

- 93 / 93 README files enumerated.
- Baseline formal image references: **0 / 93**.
- Baseline Mermaid teaching surfaces: **0 / 93**.
- Many files contain useful text arrows/code blocks, but these do not by themselves satisfy the visual closure goal.

### Challenges

- 12 / 12 README files enumerated.
- Baseline formal image references: **0 / 12**.
- Baseline Mermaid teaching surfaces: **0 / 12**.

## Closure target

For every Foundation, Experiment, and Challenge README:

1. at least one local teaching visual is present;
2. the visual is mechanism/procedure/decision relevant;
3. local visual references resolve;
4. image alt text is non-empty;
5. a caption explains what the learner should read from the visual;
6. safety-sensitive visuals remain conceptual and do not turn Challenge material into unsafe repair instructions;
7. existing Lesson assets are reused when they are the correct teaching surface.

## Work batches

### Batch A — Experiments 01–20

GPU execution, scheduling, memory, Roofline, VRAM, first local inference, serving slots/cache/speculation, multi-GPU, attention I/O.

### Batch B — Experiments 21–41

Precision roofs, vendor architecture/runtime inventory, hardware decisions, second-hand market, acceptance, capstones.

### Batch C — Experiments 42–61

Transformer/model anatomy, attention/KV, tokenizer identity, quality, benchmark manifest, Evidence packets.

### Batch D — Experiments 62–93

Serving latency/capacity, overload/fairness/exposure, lifecycle/release/incident, power/storage/memory/thermal, used-GPU acceptance, PSU/system/graduation.

### Batch E — Challenges 01–12

Compatibility archaeology, firmware/repair theory boundaries, kernel/source work, multi-node systems, adaptation/RAG/agents/open-source/multimodal.

## Completion criterion

The audit closes only after a full repository-side recomputation confirms:

- Foundations: 6 / 6 teaching surfaces;
- Experiments: 93 / 93 teaching surfaces;
- Challenges: 12 / 12 teaching surfaces;
- local visual reference errors: 0.

Further images after closure should be added only for a concrete causal, spatial, temporal, quantitative, procedural, or safety-learning need.

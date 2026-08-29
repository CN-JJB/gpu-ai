# Current State

## Source of truth

- Repo: CN-JJB/gpu-ai
- Branch: main
- Stable course and dynamic Intelligence lane remain separate.

## Post-freeze visual/comprehension audit — ACTIVE

The learner-ready substantive checkpoint remains valid, but a new post-freeze maintenance pass is active at the user's request:

~~~text
docs/course/VISUAL-COMPREHENSION-AUDIT.md
~~~

Goal: review every stable lesson for explanation depth, beginner legibility, and whether spatial/temporal/quantitative mechanisms should be taught with SVG, plots, timelines, calculators, or interactive simulations rather than prose alone.

Baseline scan:

~~~text
stable lesson HTML = 62
<img> before pass = 0
<svg> before pass = 0
<figure> before pass = 0
interactive lesson pages before pass = 1
~~~

Batch 01 (Lessons 01–05), Batch 02 (Lessons 06–13), and Batch 03 (Lessons 14–23) are implemented and marker-checked. The pass now includes causal/static SVGs, evidence/dataflow diagrams, queue/cache/speculation simulations, Roofline and VRAM/bpw calculators, generation maps, vendor execution/software-stack teaching lenses, and decision/market/acceptance flows. All simulator/calculator outputs remain explicitly conceptual or paper-budget evidence, not measured benchmark evidence.

Batch 03 added second-layer mechanism diagrams for NVIDIA SM execution, AMD wave/CU/WGP resources, Apple unified-memory LLM data paths, and Intel SYCL→Level Zero→Xe software evidence. All 23 HTML pages in Lessons 14–23 retain Retrieval Practice, completion evidence, primary sources and valid HTML closure.

Batch 04 (Lessons 24–33) is now also reviewed and marker-checked. All 10 pages already had mechanism-appropriate SVG or interactive surfaces, so no redundant new asset was added. The RoPE, hybrid-KV and sampling interactions explicitly state their teaching-model boundaries.

Batch 05 (Lessons 34–45) is implemented and marker-checked. Ten existing operations diagrams were connected to previously text-only lesson pages, and two new teaching SVGs were added for Little's Law/serving capacity and power→energy→J/token reasoning. All 12 pages now expose a visual teaching surface.

Batch 06 (Lessons 46–49) is implemented and marker-checked. Lesson 46 now exposes the staged used-GPU acceptance flow; Lessons 47–49 add dedicated PSU delivery, whole-machine hard-gate and graduation Design Review diagrams.

All planned lesson groups have been reviewed. Next: final 62-page visual/comprehension closure scan, including teaching-surface coverage and core lesson markers.

## Stable course

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
Stable v1 mainline structurally complete
Student textbook completion pass: COMPLETE — learner-ready checkpoint
~~~

The learner will start only after the stable teaching material is substantively complete. Structural existence is no longer treated as sufficient student readiness.

Authoring contract:

~~~text
docs/course/STUDENT-TEXTBOOK-COMPLETION.md
~~~

Every lesson is being reviewed for prerequisite recovery, mental model, mechanism, worked example, misconception boundary, explicit Why it matters, experiment expectations, troubleshooting, no-hardware fallback, retrieval practice, decision rule, transfer, and primary sources.

Real learner-owned benchmark results are a later learning activity and are **not an authoring blocker**.

## Latest textbook authoring progress

The stable teaching lane has advanced substantially beyond the earlier structural checkpoint:

~~~text
Experiment instruction textbook pass: complete
Foundation 00–05 learner-contract pass: complete
Challenge 01–12 teaching closure: complete
Architecture/vendor thin-page pass: complete
Transformer/model-internals thin-page pass: complete
Benchmark/quality/decision thin-page pass: complete
Operations/whole-machine/used-GPU thin-page pass: complete
Lessons 34–49 explicit opening-contract remediation: complete (16/16 verified)
~~~

Latest repository depth audit after these edits:

~~~text
stable lessons/*.html under 8 KiB = 0
~~~

Byte depth was never used as the completion criterion. The previously confirmed lessons 34–49 opening-contract defect was repaired and re-checked at 16/16 for explicit prerequisite, real-problem, retrieval, completion-evidence and primary-source semantics. A later full-corpus audit found all 62 lesson HTML files contain a no-hardware/hardware-independent path, troubleshooting/failure-recovery guidance, and a decision boundary/rule. The 338-file local-link corpus was also fully checked with zero broken or repo-escaping links.

The recent pass deliberately added or strengthened:
- mental models and causal diagrams;
- worked examples and engineering calculations;
- Experiment Evidence / Packet outputs;
- PASS / FAIL / UNKNOWN / BLOCKED interpretation branches;
- failure recovery and no-hardware fallbacks;
- decision boundaries and explicit non-claims;
- human-review boundaries for purchasing and release decisions.

Real production benchmark rows remain zero by design; no synthetic result was promoted.


## Textbook completion checkpoint

~~~text
TEXTBOOK COMPLETE
teaching-content checkpoint head = f514db1733f0e26a06e82e596e70922ab2458915
lesson slices = 49
lesson HTML = 62
experiments = 93
challenges = 12
foundations = 6
local-link corpus = 338 / 338
broken local links = 0
repo-escaping local links = 0
~~~

High-risk spot reviews passed Foundations, vendor capstone, Transformer/model dossier, serving/operations, used-GPU acceptance, whole-machine integration and graduation Design Review.

The repository connector did not expose an exact-head push-triggered Course Readiness GitHub Actions run. This remains a CI observability boundary only; the checks implemented by `tools/course/audit_student_readiness.py` were reproduced through the repository connector and passed.

## Active Phase 4 frontier

~~~text
I01–I19  catalog / compatibility / market evidence / refresh
I20–I32  real benchmark + artifact + prompt + sealed quality admission
I33–I41  reproducible model/execution performance × quality tradeoff paths
I42       automatic verified tradeoff routing
I43       decision evidence gap matrix
I44–I45  packet-bound used-GPU acceptance + readiness bridge
I46–I47  explicit performance-target policy + readiness bridge
I48–I49  explicit personal price-ceiling policy + readiness bridge
I50–I51  condition-evidence provenance grades + readiness bridge
I52       real Experiment 61 evidence session runner
I53       byte-derived real-session materializer / preflight
I54       raw semantic-source capture before manual manifest fill
~~~

Intelligence implementation is sufficiently complete for the current authoring phase. Do not expand new decision gates merely to avoid writing the textbook.

## Structural status

All currently defined Experiment 38 / Intelligence decision-readiness domains now have machine contracts:

~~~text
verified tradeoff
real benchmark provenance
exact measured compatibility
current market evidence
whole-machine feasibility
used-GPU technical acceptance
explicit performance target
explicit personal price ceiling
condition-evidence provenance
~~~

I43 returns:

~~~text
READY-FOR-HUMAN-REVIEW
~~~

only when every component passes.

It always records:

~~~text
automatic_purchase_decision = NOT-PERMITTED
~~~

No BUY action is automated.

## Benchmark boundary

~~~text
real production benchmark rows = 0
~~~

No synthetic PP/TG/PPL value is production evidence.

This remains a valid evidence boundary but no longer pauses stable-course authorship. The textbook should fully explain how the future learner will acquire, interpret, troubleshoot, and review real evidence without inventing the final numbers.

Real non-synthetic Experiment 61 intake still requires:

~~~text
manifest
+ raw llama-bench
+ benchmark PACKET
+ canonical IDs
+ exact model artifact
+ benchmark command record
+ hardware profile
+ prompt evidence
+ concrete quality corpus
+ quality identity schema v2
+ sealed quality command/raw streams
+ quality PACKET
+ exact evaluation argv
+ machine-readable PPL metric
→ I07/I20/I22/I23/I24/I25/I26/I27/I29/I30/I32 READY
~~~

## Tradeoff provenance

### Model-artifact lane

~~~text
I33 exact quality A/B
→ I36 reproduce quality comparison
→ I37 bind PP/TG × PPL
→ I38 reproduce full joint artifact
~~~

### Execution-variable lane

~~~text
I35 explicit manifest-value ↔ quality argv contract
→ I39 reproduce execution-variable quality comparison
→ I40 bind PP/TG × PPL
→ I41 reproduce full joint artifact
~~~

### Unified route

~~~text
variant.model*      → I38
variant.execution.* → I41
other variables     → BLOCKED
~~~

I42 chooses the route from the validated manifests; callers cannot force it.

## Decision-readiness lane

~~~text
I43 gap matrix
I44 packet-bound ACCEPT / REVIEW / REJECT
I45 acceptance bridge
I46 explicit PP/TG/PPL hard thresholds
I47 performance-target bridge
I48 explicit max sticker + watch band
I49 price bridge using the same market record
I50 C0–C4 condition-evidence provenance contract
I51 condition provenance bridge
~~~

Condition has two separate axes:

~~~text
evidence strength: C0 C1 C2 C3 C4
technical health: ACCEPT REVIEW REJECT
~~~

Current production condition rule:
- real, learner-owned, PACKET-bound, independently reproducible I44 evidence → C3 provenance;
- synthetic evidence → C0;
- C4 is reserved and not emitted.

A C3 REJECT is strong evidence but still fails the separate used-GPU ACCEPT gate.

## Market evidence

Stable mapping:

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current production count remains:

~~~text
M1=3
M2=3
M3=9
market observations=15
~~~

Market observations are dynamic Intelligence data. Stable lessons teach how to interpret provenance, freshness, cohorts, uncertainty, and transaction semantics; they must not freeze today's prices into permanent textbook claims.

## Latest implementation CI

~~~text
workflow: Intelligence Self-Test
run #178
run id 33195425859
head d308acbc62f3d540ed26181d23ed8a1602d127d1
job id 98931209062
conclusion success
~~~

The complete suite passed through I54, including raw semantic-source capture, the unnumbered I54-to-profile assembler, byte-derived I53 preparation, the end-to-end I52 orchestration path, and the first-real workspace bootstrap.

## Newest authoring contract

- docs/course/STUDENT-TEXTBOOK-COMPLETION.md

## Next — learner phase

1. Begin the learner at Foundation 00 / Lesson 01 using the stable course sequence; do not reopen architecture or add Intelligence gates merely to postpone learning.
2. Keep real production benchmark rows at zero until the learner reaches the real-evidence experiments and produces learner-owned artifacts.
3. When the learner later reaches Experiment 61, use the existing I54 → verified profile → human semantic fill → I53 → I52 workflow.
4. Continue to treat purchase, release and used-GPU decisions as human-reviewed outcomes. `automatic_purchase_decision = NOT-PERMITTED`.
5. Any future textbook edits after this checkpoint must be treated as post-freeze maintenance and should re-run the affected readiness/link checks.

No fake benchmark results, no auto-purchase, and no unsafe hardware modification.

# Research Note 0004 — Graduation Machine Design Capstone

日期：2026-08-27

## Research question

How should the course turn the whole-machine dossier from Slice 48 into a graduation deliverable that demonstrates transfer rather than merely filling a form?

This slice does not introduce a new hardware theory. It composes already-established course Evidence into an auditable engineering review.

Primary internal inputs:
- Slice 29 Model Architecture Dossier;
- Slice 33 Benchmark / Workload Manifest and Evidence Packet;
- Slices 34–41 serving / reliability / observability;
- Slices 42–47 energy, storage, host RAM, thermal, used-GPU and PSU evidence;
- Slice 48 whole-machine hard-gate dossier;
- Experiment 91 real machine design dossier.

## 1. Graduation is a decision argument

The learner must defend a machine relative to a frozen workload:

~~~text
goal/workload
→ model identity
→ machine architecture
→ feasibility gates
→ measured quality/performance/SLO
→ TCO/risk
→ revision alternatives
→ upgrade roadmap
→ final decision
~~~

The final artifact is not a parts list and not a benchmark screenshot collection.

## 2. Preserve Slice 48 decision semantics

The capstone keeps:

~~~text
known required FAIL → REVISE
critical UNKNOWN → BLOCKED
all required gates PASS → ACCEPT
~~~

A graduation report may validly conclude REVISE or BLOCKED. Engineering maturity is shown by refusing to purchase or modify hardware when critical evidence is missing.

## 3. Evidence completeness is separate from hardware feasibility

Experiment 91 checks gate status and source presence. The graduation layer additionally asks whether the final argument covers every material claim.

For each material claim, record:
- claim id;
- claim text;
- evidence source/path/hash;
- evidence type;
- scope/conditions;
- whether the evidence is measured, derived, official, or seller/community information.

A report with many PASS labels but no traceable evidence is incomplete.

## 4. Evidence strength is contextual

The capstone should not invent one global evidence score.

Examples:
- runtime output can prove the exact backend recognized and executed the target path;
- an official product document can establish a published connector or capability;
- a seller listing can establish what the seller claimed, but not that the card physically matches the claim;
- one cold benchmark cannot prove sustained thermal capacity;
- one single-user token-generation number cannot prove a multi-user serving SLO.

The rubric therefore asks whether the evidence is sufficient for the claim it supports.

## 5. The report must state what its Evidence does NOT prove

Every final report must include explicit non-claims.

Examples:
- ACCEPT does not prove universal optimality;
- a synthetic case does not prove real hardware behavior;
- a short benchmark does not prove long-term reliability;
- a model hash does not prove model quality for every task;
- measured performance on one backend/version does not prove future compatibility;
- non-invasive validation does not prove hidden board-level defects;
- a purchase recommendation does not prove future resale value or market price.

## 6. Revision alternatives must be causal

A REVISE report should not write vague advice such as “buy a better GPU.”

Each revision candidate must state:
1. which failed gate or target pressure it addresses;
2. what variable changes;
3. what new evidence is required;
4. what new risk/cost it introduces.

Canonical revision families:
- smaller model or quant;
- lower context / concurrency / tighter workload target;
- different GPU;
- multi-GPU;
- PSU/platform upgrade;
- cooling or service-policy change.

The capstone does not automatically choose or purchase a revision.

## 7. Upgrade roadmap is staged, not speculative shopping

A useful roadmap separates:
- now: what is required to make the declared target feasible;
- next: what evidence-triggered upgrade would unlock the next workload;
- later: optional improvements after measured bottlenecks appear.

Every upgrade should have a trigger such as:
- VRAM capacity ceiling reached;
- serving p95 exceeds SLO;
- energy/TCO crosses a declared threshold;
- PCIe/topology becomes the measured limiter;
- sustained thermal drift exceeds target.

## 8. Rubric structure

The graduation rubric should grade transfer evidence, not prose polish alone.

Required dimensions:
1. workload identity;
2. model/system architecture reasoning;
3. hard-gate correctness;
4. evidence traceability;
5. benchmark/quality/SLO validity;
6. TCO/risk reasoning;
7. revision alternatives;
8. upgrade roadmap;
9. limits/non-claims;
10. final decision consistency.

A learner should not pass if a fatal gate is averaged away by strong scores elsewhere.

## 9. Synthetic review cases

The L0 validator needs at least three distinct conclusions.

### Case A — ACCEPT

All required gates PASS, all material claims have evidence references, and the final decision is ACCEPT.

### Case B — REVISE

One known hard gate FAILS, there are no blocking unknowns, and at least one revision directly addresses the failed gate.

### Case C — BLOCKED

No known hard failure is necessary, but a purchase/safety/compatibility-critical required claim remains UNKNOWN or lacks evidence.

The validator checks decision consistency, not whether a particular GPU should be purchased.

## 10. Real report workflow

The real graduation experiment should:

~~~text
freeze target
→ complete Experiment 91 dossier
→ build final Evidence index
→ write architecture narrative
→ attach measured benchmark/quality/SLO evidence
→ list failures/unknowns
→ propose revision alternatives
→ build evidence-triggered upgrade roadmap
→ declare non-claims
→ validate completeness
→ issue ACCEPT / REVISE / BLOCKED
~~~

## 11. Success evidence

Graduation-level transfer is demonstrated when the learner can:
- explain why the target implies the chosen machine constraints;
- identify a fatal gate without hiding it behind preference scores;
- distinguish measured evidence from claims;
- reject an unsupported PASS;
- propose a revision and specify the new evidence needed;
- explain what the final report still does not prove.

## Claims to avoid

- “the capstone must end in ACCEPT”;
- “more benchmark screenshots mean stronger evidence”;
- “one weighted score can grade away a hard failure”;
- “a seller claim is equivalent to runtime identity evidence”;
- “one successful run proves long-term reliability”;
- “an upgrade roadmap is a shopping list”;
- “ACCEPT means universally optimal or future-proof”.
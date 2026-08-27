# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–48 are implemented.
Experiments 01–91 exist.

## Learning state

The previous long CURRENT state through Slice 45 is archived byte-for-byte at:

```text
learning/archive/CURRENT-through-slice45-2026-08-27.md
```

`learning/CURRENT.md` is now intentionally concise and tracks the active frontier.

## Slice 48 core — Whole-Machine System Integration Dossier

Feasibility order:

```text
workload/model
→ hard gates
→ blocking unknowns
→ measured performance/quality/SLO
→ preferences/TCO
→ decision
```

Decision semantics:

```text
known hard FAIL → REVISE
critical UNKNOWN → BLOCKED
all required gates PASS → ACCEPT
```

Synthetic verified:

```text
balanced machine → ACCEPT
30 GiB required vs 24 GiB available → REVISE
unknown modular PSU cable compatibility → BLOCKED
```

No weighted score is allowed to average away a hard failure.

Real Experiment 91 requires source evidence for every required gate and links prior course packets rather than copying unverified numbers.

## Active next slice — Graduation Machine Design Capstone

Build the final learner deliverable:

```text
goal/workload
→ model dossier
→ machine architecture
→ hard-gate matrix
→ measured benchmark/SLO/quality
→ TCO/energy
→ risks/unknowns
→ revision alternatives
→ upgrade roadmap
→ final ACCEPT / REVISE / BLOCKED
```

Need:
- final report rubric;
- evidence completeness validator;
- two or three synthetic design-review cases;
- real report skeleton linked to Experiment 91;
- no auto-purchasing or hardware modification;
- explicit statement of what the final evidence does NOT prove.

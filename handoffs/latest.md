# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

~~~text
Slices 01–49 implemented
Experiments 01–93 exist
~~~

The stable v1 mainline now reaches the graduation Machine Design Capstone.

## Slice 48 foundation

Whole-machine feasibility remains:

~~~text
workload/model
→ hard gates
→ blocking unknowns
→ measured performance/quality/SLO
→ preferences/TCO
→ ACCEPT / REVISE / BLOCKED
~~~

Experiment 91 is the real machine dossier.

Decision semantics:

~~~text
known required FAIL → REVISE
critical UNKNOWN / missing required evidence → BLOCKED
all required gates PASS → ACCEPT
~~~

No weighted score may average away a hard failure.

## Slice 49 core — Graduation Machine Design Capstone

New final workflow:

~~~text
freeze target
→ link Experiment 91
→ material-claim Evidence index
→ architecture narrative
→ benchmark / quality / SLO
→ TCO / risk
→ causal revision alternatives
→ evidence-triggered upgrade roadmap
→ explicit non-claims
→ final rationale
→ transfer check
~~~

Key distinction:

~~~text
machine feasibility
!=
graduation packet completeness
~~~

A BLOCKED machine can still have a COMPLETE graduation packet if the learner correctly proves the blocker and resolution path.

An ACCEPT machine can still have an INCOMPLETE graduation packet if its material claims are not auditable.

## New artifacts

Research:
- research/system/0004-graduation-machine-design-capstone.md

Reference:
- reference/system/graduation-machine-design-capstone.md

Lesson:
- lessons/49-graduation-capstone/01-evidence-to-design-review.html

Synthetic lab:
- labs/experiments/92-graduation-design-review/

Real graduation lab:
- labs/experiments/93-real-graduation-report/

Evidence:
- examples/evidence/experiment-49-graduation-machine-design-capstone.md

Learning record:
- learning/records/2026-08-27-graduation-machine-design-capstone.md

## Experiment 92

Synthetic cases cover:

~~~text
ACCEPT
REVISE
BLOCKED
~~~

Validator checks:
- gate/decision consistency;
- material-claim evidence presence and scope;
- revision coverage for failed gates;
- explicit non-claims;
- evidence-triggered roadmap structure.

## Experiment 93

Contains:
- CAPSTONE-REPORT-TEMPLATE.md;
- RUBRIC.md;
- capstone.template.json;
- validate_capstone.py;
- EXPECTED.md.

The validator returns independently:

~~~text
MACHINE DECISION: ACCEPT / REVISE / BLOCKED
CAPSTONE COMPLETENESS: COMPLETE / INCOMPLETE
~~~

## Active next work

Do not extend the stable mainline by default.

Next:
1. run Experiment 93 on a real learner-owned target/machine;
2. feed demonstrated gaps back into existing Lessons;
3. otherwise begin Phase 4 Intelligence Stations for dynamic hardware/model/benchmark data.

No auto-purchase or unsafe hardware modification is part of the graduation workflow.

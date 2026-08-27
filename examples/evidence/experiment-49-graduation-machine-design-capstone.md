# Evidence — Experiment 49: Graduation Machine Design Capstone

状态：graduation capstone slice implemented; L0 review cases defined; real graduation report workflow ready.

## Claim

> A graduation-quality Local-LLM machine design is an auditable decision argument, not a parts list. Machine feasibility and graduation-packet completeness must be evaluated separately.

## Inherited machine-decision semantics

From Slice 48 / Experiment 91:

~~~text
known required FAIL → REVISE
critical UNKNOWN / missing gate evidence → BLOCKED
all required gates PASS → ACCEPT
~~~

Slice 49 does not replace this decision model.

## New graduation layer

The final report additionally requires:
- material-claim Evidence index;
- evidence type and scope/conditions;
- architecture narrative;
- benchmark/quality/SLO interpretation;
- causal revision alternatives;
- evidence-triggered upgrade roadmap;
- explicit statements of what the Evidence does not prove;
- rubric self-review;
- final rationale and transfer check.

## Experiment 92

Three synthetic review cases were added:

~~~text
case-accept.json
→ ACCEPT

case-revise.json
→ REVISE

case-blocked.json
→ BLOCKED
~~~

The validator checks:
- required gate consistency;
- material-claim evidence completeness;
- evidence scope;
- explicit non-claims;
- revision coverage for failed gates;
- decision consistency.

It intentionally does not choose hardware.

## Experiment 93

The real graduation workflow links Experiment 91 rather than copying it.

The final validator returns two independent outputs:

~~~text
MACHINE DECISION: ACCEPT / REVISE / BLOCKED
CAPSTONE COMPLETENESS: COMPLETE / INCOMPLETE
~~~

Therefore this is valid:

~~~text
MACHINE DECISION: BLOCKED
CAPSTONE COMPLETENESS: COMPLETE
~~~

if the learner correctly proves why the design is blocked and what Evidence resolves it.

Likewise:

~~~text
MACHINE DECISION: ACCEPT
CAPSTONE COMPLETENESS: INCOMPLETE
~~~

is possible when the machine may be feasible but the graduation submission lacks an auditable evidence chain.

## Rubric

Ten required dimensions:
1. workload identity;
2. architecture reasoning;
3. hard-gate discipline;
4. evidence traceability;
5. benchmark/quality/SLO validity;
6. TCO/risk;
7. revision quality;
8. upgrade roadmap;
9. non-claims;
10. final decision consistency.

Ratings:
- NEEDS-EVIDENCE;
- INDEPENDENT;
- TRANSFER.

No numeric average can override a fatal evidence/decision inconsistency.

## Revision principle

A valid revision must identify:
- failed gate or pressure;
- changed variable;
- new evidence required;
- new cost/risk.

Canonical families include:
- smaller model/quant;
- lower context/concurrency;
- different GPU;
- multi-GPU;
- PSU/platform upgrade;
- cooling/service-policy change.

No automatic purchase occurs.

## Upgrade-roadmap principle

The roadmap is not a speculative shopping list.

It uses:

~~~text
NOW
NEXT — evidence trigger
LATER — evidence trigger
~~~

Examples of triggers:
- VRAM headroom falls below target;
- serving p95 exceeds SLO;
- sustained thermal drift exceeds target;
- measured topology/interconnect becomes the limiter.

## Explicit non-claims

The final workflow requires the learner to state what the evidence does not prove, including boundaries such as:
- universal optimality;
- future backend compatibility;
- hidden board-level defects;
- long-term reliability;
- future market/resale value.

## Transfer evidence

Graduation-level transfer is demonstrated by applying the same reasoning to an unseen machine or changed workload and explaining:
- which gates change;
- which evidence is reusable;
- which evidence must be recollected;
- why the final decision may change.
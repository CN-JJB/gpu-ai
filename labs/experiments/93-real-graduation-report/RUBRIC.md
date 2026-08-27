# Graduation Machine Design Rubric

This rubric grades engineering transfer, not hardware price or prose style.

## Rating scale

For each dimension use:

- NEEDS-EVIDENCE — missing, inconsistent, or mostly asserted;
- INDEPENDENT — learner can complete the task correctly with traceable Evidence;
- TRANSFER — learner can explain the boundary and adapt the reasoning to a changed machine/workload.

## Required dimensions

| Dimension | INDEPENDENT evidence | TRANSFER evidence |
|---|---|---|
| 1. Workload identity | target/model/context/concurrency/SLO are frozen | predicts which requirements change under a new workload |
| 2. Architecture reasoning | each major component is justified by target constraints | compares an unseen architecture without brand-only reasoning |
| 3. Hard-gate discipline | PASS/FAIL/UNKNOWN follows Experiment 91 | identifies when a previously optional gate becomes hard |
| 4. Evidence traceability | material claims link to source/path/hash and scope | distinguishes what each evidence type can and cannot prove |
| 5. Benchmark/quality/SLO | metrics have workload identity and conditions | explains why a metric does not transfer to another workload |
| 6. TCO/risk | purchase/platform/energy/risk are separated | changes time horizon/duty cycle and updates the decision logic |
| 7. Revision quality | each revision addresses a named failure/pressure | proposes multiple causal revisions with different tradeoffs |
| 8. Upgrade roadmap | upgrades have evidence triggers | rejects an upgrade when the measured trigger is absent |
| 9. Non-claims | report states explicit limits | explains how new evidence would narrow one limitation |
| 10. Final decision | ACCEPT/REVISE/BLOCKED matches evidence | explains what new evidence would change the decision |

## Graduation rule

The capstone packet is not COMPLETE if any required dimension is NEEDS-EVIDENCE.

A strong graduation submission should show TRANSFER in several dimensions, especially:
- workload identity;
- hard-gate discipline;
- evidence traceability;
- revision quality;
- final decision.

No numeric average can override a fatal inconsistency.

## Hard veto conditions

Any of these makes the packet INCOMPLETE until corrected:
- declared ACCEPT while a required gate is FAIL or UNKNOWN;
- a material claim has no traceable evidence;
- a purchase/safety-critical unknown is guessed into PASS;
- benchmark numbers omit the workload identity needed to interpret them;
- a REVISE conclusion gives no revision that addresses the failed gate;
- Experiment 91 identity/decision is missing;
- no explicit non-claims;
- final decision and evidence disagree.

## Important distinction

Machine feasibility and graduation completeness are independent.

Examples:

~~~text
Machine: BLOCKED
Packet: COMPLETE
~~~

is valid when the report correctly proves why the machine is blocked and how to resolve the unknown.

~~~text
Machine: ACCEPT
Packet: INCOMPLETE
~~~

is also possible when the hardware may be feasible but the submitted evidence/report is not auditable.
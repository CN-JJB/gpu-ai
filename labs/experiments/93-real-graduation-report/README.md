# Experiment 93 — Real Graduation Machine Design Report

硬件等级：L1–L3，取决于你的目标和已有机器。

## Goal

Produce the final human-readable Local-LLM machine design report from existing course Evidence.

This experiment:
- does not auto-purchase hardware;
- does not flash firmware;
- does not change PSU wiring;
- does not require the final machine decision to be ACCEPT.

A complete graduation packet may end in:

~~~text
ACCEPT
REVISE
BLOCKED
~~~

## Prerequisite

Complete Experiment 91 first.

You need:
- frozen target;
- Experiment 91 dossier;
- its ACCEPT / REVISE / BLOCKED decision;
- raw Evidence paths/hashes for material claims.

## 1. Copy templates

~~~bash
cp CAPSTONE-REPORT-TEMPLATE.md my-machine-report.md
cp capstone.template.json capstone.json
~~~

Do not overwrite the template in place.

## 2. Link, do not duplicate, Experiment 91

In capstone.json record:
- target identity/hash;
- Experiment 91 dossier path/hash;
- Experiment 91 machine decision.

The final report must not silently change the machine decision without new Evidence and a new dossier run.

## 3. Build the material-claim index

Every claim that can change:
- feasibility;
- purchase;
- safety;
- quality;
- performance/SLO;
- TCO;
- upgrade timing

needs:
- evidence reference;
- evidence type;
- scope/conditions.

Use Experiment 61 for the final Evidence Packet index when applicable.

## 4. Write the report

Fill CAPSTONE-REPORT-TEMPLATE.md.

Required narrative:
- goal/workload;
- model identity;
- architecture;
- hard-gate summary;
- benchmark/quality/SLO;
- TCO/risk;
- unknowns;
- revisions;
- upgrade roadmap;
- explicit non-claims;
- final rationale.

## 5. Validate completeness

~~~bash
python3 validate_capstone.py capstone.json
~~~

The validator returns two independent outputs:

~~~text
MACHINE DECISION: ACCEPT / REVISE / BLOCKED
CAPSTONE COMPLETENESS: COMPLETE / INCOMPLETE
~~~

A BLOCKED machine can still have a COMPLETE graduation packet.

## 6. Review against rubric

Use RUBRIC.md.

Graduation quality is based on:
- traceability;
- causal reasoning;
- uncertainty discipline;
- revision quality;
- transfer.

It is not based on buying expensive hardware.

## 7. Stop conditions

Do not proceed with purchase or modification when:
- the linked machine decision is BLOCKED;
- a safety/power-path claim is unresolved;
- the target identity changed and Experiment 91 has not been rerun.

## Final Evidence

Keep:
- final report;
- capstone.json;
- Experiment 91 dossier;
- Evidence Packet index/hash;
- raw benchmark/quality/SLO evidence;
- any redaction notes needed before publishing the report.
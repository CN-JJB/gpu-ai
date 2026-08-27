#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DECISIONS = {"ACCEPT", "REVISE", "BLOCKED"}
RATINGS = {"NEEDS-EVIDENCE", "INDEPENDENT", "TRANSFER"}
EVIDENCE_TYPES = {"MEASURED", "DERIVED", "OFFICIAL", "SELLER/COMMUNITY"}
PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN"}


def present(value):
    return str(value or "").strip().upper() not in PLACEHOLDERS


def main():
    p = argparse.ArgumentParser()
    p.add_argument("packet", type=Path)
    a = p.parse_args()
    c = json.loads(a.packet.read_text(encoding="utf-8"))

    problems = []

    for field in ("capstone_id", "report_path", "target_sha256"):
        if not present(c.get(field)):
            problems.append(f"missing {field}")

    e91 = c.get("experiment91", {})
    for field in ("dossier_source", "dossier_sha256"):
        if not present(e91.get(field)):
            problems.append(f"missing experiment91.{field}")

    decision = str(e91.get("machine_decision", "")).upper()
    if decision not in DECISIONS:
        problems.append(f"invalid experiment91.machine_decision: {decision!r}")

    packet = c.get("evidence_packet", {})
    for field in ("index_source", "index_sha256"):
        if not present(packet.get(field)):
            problems.append(f"missing evidence_packet.{field}")

    material_claims = [x for x in c.get("claims", []) if x.get("material", True)]
    if not material_claims:
        problems.append("no material claims indexed")

    for i, claim in enumerate(material_claims, start=1):
        cid = str(claim.get("id", "")).strip() or f"#{i}"
        if not present(claim.get("claim")):
            problems.append(f"claim {cid}: missing claim text")
        etype = str(claim.get("evidence_type", "")).upper()
        if etype not in EVIDENCE_TYPES:
            problems.append(f"claim {cid}: invalid evidence_type {etype!r}")
        if not present(claim.get("evidence")):
            problems.append(f"claim {cid}: missing evidence reference")
        if not present(claim.get("scope")):
            problems.append(f"claim {cid}: missing scope/conditions")

    revisions = c.get("revisions", [])
    if decision == "REVISE":
        useful = []
        for r in revisions:
            gates = [str(x).strip() for x in r.get("addresses_gates", []) if str(x).strip()]
            if gates and present(r.get("change")) and present(r.get("new_evidence_required")):
                useful.append(r)
        if not useful:
            problems.append("REVISE decision has no causal revision with addressed gate and new evidence requirement")

    roadmap = c.get("upgrade_roadmap", {})
    if not isinstance(roadmap.get("now", []), list):
        problems.append("upgrade_roadmap.now must be a list")
    for stage in ("next", "later"):
        entries = roadmap.get(stage, [])
        if not isinstance(entries, list) or not entries:
            problems.append(f"upgrade_roadmap.{stage} must contain at least one evidence-triggered item")
            continue
        for i, item in enumerate(entries, start=1):
            for field in ("trigger", "action", "validation_required"):
                if not present(item.get(field)):
                    problems.append(f"{stage} roadmap item {i}: missing {field}")

    non_claims = [str(x).strip() for x in c.get("non_claims", []) if present(x)]
    if len(non_claims) < 4:
        problems.append("need at least 4 explicit non-claims")

    rubric = c.get("rubric", {})
    required = {
        "workload_identity",
        "architecture_reasoning",
        "hard_gate_discipline",
        "evidence_traceability",
        "benchmark_quality_slo",
        "tco_risk",
        "revision_quality",
        "upgrade_roadmap",
        "non_claims",
        "final_decision",
    }

    missing_rubric = sorted(required - set(rubric))
    if missing_rubric:
        problems.append("missing rubric dimensions: " + ", ".join(missing_rubric))

    for name in sorted(required & set(rubric)):
        rating = str(rubric[name]).upper()
        if rating not in RATINGS:
            problems.append(f"rubric {name}: invalid rating {rating!r}")
        elif rating == "NEEDS-EVIDENCE":
            problems.append(f"rubric {name}: still NEEDS-EVIDENCE")

    completeness = "COMPLETE" if not problems else "INCOMPLETE"

    print(f"MACHINE DECISION: {decision if decision in DECISIONS else '<invalid>'}")
    print(f"CAPSTONE COMPLETENESS: {completeness}")
    print("PROBLEMS:")
    for x in problems:
        print("- " + x)

    if problems:
        raise SystemExit(2)


if __name__ == "__main__":
    main()

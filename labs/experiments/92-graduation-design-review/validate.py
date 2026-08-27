#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

VALID = {"PASS", "FAIL", "UNKNOWN"}
DECISIONS = {"ACCEPT", "REVISE", "BLOCKED"}
PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN"}


def present(value):
    return str(value or "").strip().upper() not in PLACEHOLDERS


def main():
    p = argparse.ArgumentParser()
    p.add_argument("case", type=Path)
    a = p.parse_args()

    c = json.loads(a.case.read_text(encoding="utf-8"))

    passed = []
    failed = []
    blocked = []
    errors = []

    for name, gate in c.get("gates", {}).items():
        if not gate.get("required", False):
            continue

        status = str(gate.get("status", "")).upper()
        source = str(gate.get("source", "")).strip()

        if status not in VALID:
            errors.append(f"{name}: invalid gate status {status!r}")
            continue

        if not present(source):
            blocked.append(f"{name}: required gate missing evidence source")
        elif status == "UNKNOWN":
            blocked.append(f"{name}: UNKNOWN ({source})")
        elif status == "FAIL":
            failed.append(name)
        else:
            passed.append(name)

    for claim in c.get("claims", []):
        if not claim.get("material", True):
            continue
        claim_id = str(claim.get("id", "")).strip() or "<unnamed>"
        source = str(claim.get("evidence", "")).strip()
        scope = str(claim.get("scope", "")).strip()
        if not present(source):
            blocked.append(f"claim {claim_id}: missing evidence")
        if not present(scope):
            blocked.append(f"claim {claim_id}: missing evidence scope/conditions")

    non_claims = [str(x).strip() for x in c.get("non_claims", []) if str(x).strip()]
    if len(non_claims) < 3:
        blocked.append("fewer than 3 explicit non-claims")

    if blocked:
        expected = "BLOCKED"
    elif failed:
        expected = "REVISE"
    else:
        expected = "ACCEPT"

    declared = str(c.get("declared_decision", "")).upper()
    if declared not in DECISIONS:
        errors.append(f"invalid declared_decision: {declared!r}")
    elif declared != expected:
        errors.append(f"declared_decision={declared} but evidence implies {expected}")

    revisions = c.get("revisions", [])
    addressed = {
        str(g).strip()
        for r in revisions
        for g in r.get("addresses_gates", [])
        if str(g).strip()
    }

    if expected == "REVISE":
        missing = [g for g in failed if g not in addressed]
        if missing:
            errors.append("failed gates without a revision path: " + ", ".join(missing))
        for i, r in enumerate(revisions, start=1):
            if not present(r.get("change")):
                errors.append(f"revision {i}: missing change")
            if not present(r.get("new_evidence_required")):
                errors.append(f"revision {i}: missing new evidence requirement")

    roadmap = c.get("upgrade_roadmap", {})
    for stage in ("now", "next", "later"):
        entries = roadmap.get(stage, [])
        if not isinstance(entries, list):
            errors.append(f"upgrade_roadmap.{stage} must be a list")
    for stage in ("next", "later"):
        for i, item in enumerate(roadmap.get(stage, []), start=1):
            if not present(item.get("trigger")):
                errors.append(f"{stage} roadmap item {i}: missing evidence trigger")

    print(f"CASE: {c.get('case_id', '<missing>')}")
    print("PASS GATES:", ", ".join(passed) if passed else "-")
    print("FAILED GATES:", ", ".join(failed) if failed else "-")
    print("BLOCKERS:")
    for x in blocked:
        print("- " + x)
    print("ERRORS:")
    for x in errors:
        print("- " + x)
    print(f"IMPLIED DECISION: {expected}")
    print(f"DECLARED DECISION: {declared or '<missing>'}")

    if errors:
        raise SystemExit(2)
    if declared != expected:
        raise SystemExit(3)


if __name__ == "__main__":
    main()

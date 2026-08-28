#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from verify_used_gpu_acceptance import verify_used_gpu_acceptance_artifact


CONTRACT = "condition-evidence-provenance-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_condition_evidence_grade(
    acceptance,
    case,
    packet,
):
    acceptance = Path(acceptance)
    case = Path(case)
    packet = Path(packet)

    verified = verify_used_gpu_acceptance_artifact(
        acceptance,
        case,
        packet,
    )
    errors = list(verified["errors"])
    artifact = verified["supplied"] if not errors else {}

    result = None
    if not errors and artifact:
        synthetic = bool(artifact.get("synthetic", False))
        grade = "C0" if synthetic else "C3"
        basis = (
            "SYNTHETIC-FIXTURE-NOT-PRODUCTION"
            if synthetic
            else "LEARNER-OWNED-PACKET-BOUND-REPRODUCIBLE-I44"
        )
        result = {
            "condition_evidence_schema_version": 1,
            "condition_evidence_contract": CONTRACT,
            "hardware_id": artifact.get("hardware_id"),
            "case_id": artifact.get("case_id"),
            "synthetic_input": synthetic,
            "evidence_grade": grade,
            "evidence_grade_basis": basis,
            "acceptance_decision": artifact.get("decision"),
            "health_decision_is_separate": True,
            "c4_status": "RESERVED-NOT-EMITTED",
            "evidence": {
                "acceptance_sha256": sha256_file(acceptance),
                "case_sha256": sha256_file(case),
                "packet_sha256": sha256_file(packet),
            },
            "scope": (
                "condition evidence provenance strength only; "
                "not a GPU health certificate or purchase decision"
            ),
        }

    return {"errors": errors, "result": result}


def main():
    p = argparse.ArgumentParser(
        description=(
            "Derive the course condition-evidence provenance grade from an "
            "independently reproducible I44 used-GPU acceptance packet."
        )
    )
    p.add_argument("--acceptance", type=Path, required=True)
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    built = build_condition_evidence_grade(
        a.acceptance,
        a.case,
        a.packet,
    )

    print("CONDITION EVIDENCE GRADE")
    print("ERRORS")
    for error in built["errors"]:
        print("- " + error)
    if built["errors"] or built["result"] is None:
        print("CONDITION EVIDENCE: BLOCKED")
        raise SystemExit(2)

    result = built["result"]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"grade={result['evidence_grade']}")
    print(f"acceptance_decision={result['acceptance_decision']}")
    print(f"synthetic_input={result['synthetic_input']}")
    print(f"out={a.out}")
    print("CONDITION EVIDENCE: PASS")
    print(
        "The grade describes evidence provenance. ACCEPT/REVIEW/REJECT remains a "
        "separate health decision."
    )


if __name__ == "__main__":
    main()

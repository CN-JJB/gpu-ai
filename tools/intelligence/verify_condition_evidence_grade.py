#!/usr/bin/env python3
import argparse
from pathlib import Path

from bind_performance_quality_ab import load_object
from derive_condition_evidence_grade import build_condition_evidence_grade


def verify_condition_evidence_grade(
    result_path,
    acceptance,
    case,
    packet,
):
    result_path = Path(result_path)
    errors = []
    supplied = {}
    if not result_path.is_file():
        errors.append(f"condition evidence result is not a file: {result_path}")
    else:
        supplied = load_object(result_path, "condition evidence result", errors)

    rebuilt = build_condition_evidence_grade(
        acceptance,
        case,
        packet,
    )
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["result"]
    if expected is not None and supplied != expected:
        errors.append(
            "condition evidence artifact does not exactly match independently rebuilt "
            "I44 acceptance provenance"
        )

    return {"errors": errors, "supplied": supplied, "expected": expected}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--acceptance", type=Path, required=True)
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    a = p.parse_args()

    verified = verify_condition_evidence_grade(
        a.result,
        a.acceptance,
        a.case,
        a.packet,
    )
    print("CONDITION EVIDENCE VERIFICATION")
    print("ERRORS")
    for error in verified["errors"]:
        print("- " + error)
    if verified["errors"]:
        print("CONDITION EVIDENCE ARTIFACT: BLOCKED")
        raise SystemExit(2)
    print("CONDITION EVIDENCE ARTIFACT: PASS")
    print("The provenance grade is exactly reproducible from I44 evidence.")


if __name__ == "__main__":
    main()

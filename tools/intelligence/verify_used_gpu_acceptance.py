#!/usr/bin/env python3
import argparse
from pathlib import Path

from evaluate_used_gpu_acceptance import (
    build_acceptance_artifact,
    load_object,
)


def verify_used_gpu_acceptance_artifact(
    acceptance,
    case,
    packet,
):
    acceptance = Path(acceptance)
    case = Path(case)
    packet = Path(packet)

    errors = []
    supplied = {}
    if not acceptance.is_file():
        errors.append(f"acceptance artifact is not a file: {acceptance}")
    else:
        supplied = load_object(acceptance, "acceptance artifact", errors)

    rebuilt = build_acceptance_artifact(case, packet)
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["artifact"]
    if expected is not None and supplied != expected:
        errors.append(
            "used-GPU acceptance artifact does not exactly match independently "
            "rebuilt PACKET-bound case evidence"
        )

    return {
        "errors": errors,
        "supplied": supplied,
        "expected": expected,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Independently rebuild and verify a packet-bound used-GPU acceptance artifact."
        )
    )
    p.add_argument("--acceptance", type=Path, required=True)
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    a = p.parse_args()

    result = verify_used_gpu_acceptance_artifact(
        a.acceptance,
        a.case,
        a.packet,
    )

    print("USED GPU ACCEPTANCE VERIFICATION")
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"]:
        print("USED GPU ACCEPTANCE ARTIFACT: BLOCKED")
        raise SystemExit(2)

    print("USED GPU ACCEPTANCE ARTIFACT: PASS")
    print(
        "PASS means the acceptance artifact is exactly reproducible. "
        "It still does not map ACCEPT to Experiment 38 C3/C4."
    )


if __name__ == "__main__":
    main()

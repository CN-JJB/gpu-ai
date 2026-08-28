#!/usr/bin/env python3
import argparse
from pathlib import Path

from evaluate_used_gpu_acceptance import (
    build_acceptance_artifact,
    load_object,
)


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

    errors = []
    supplied = {}
    if not a.acceptance.is_file():
        errors.append(f"acceptance artifact is not a file: {a.acceptance}")
    else:
        supplied = load_object(a.acceptance, "acceptance artifact", errors)

    rebuilt = build_acceptance_artifact(a.case, a.packet)
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["artifact"]
    if expected is not None and supplied != expected:
        errors.append(
            "used-GPU acceptance artifact does not exactly match independently "
            "rebuilt PACKET-bound case evidence"
        )

    print("USED GPU ACCEPTANCE VERIFICATION")
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors:
        print("USED GPU ACCEPTANCE ARTIFACT: BLOCKED")
        raise SystemExit(2)

    print("USED GPU ACCEPTANCE ARTIFACT: PASS")
    print(
        "PASS means the acceptance artifact is exactly reproducible. "
        "It still does not map ACCEPT to Experiment 38 C3/C4."
    )


if __name__ == "__main__":
    main()

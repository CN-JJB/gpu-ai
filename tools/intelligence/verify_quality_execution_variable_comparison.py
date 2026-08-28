#!/usr/bin/env python3
import argparse
from pathlib import Path

from compare_quality_execution_variable import (
    build_execution_variable_quality_comparison,
    load_object,
)


def verify_execution_variable_quality_comparison(
    comparison_path,
    baseline_manifest,
    candidate_manifest,
    baseline_dir,
    candidate_dir,
    baseline_model,
    candidate_model,
    quality_corpus,
    variable_contract,
):
    comparison_path = Path(comparison_path)
    errors = []
    supplied = {}
    if not comparison_path.is_file():
        errors.append(f"quality variable comparison is not a file: {comparison_path}")
    else:
        supplied = load_object(
            comparison_path, "quality variable comparison", errors
        )

    rebuilt = build_execution_variable_quality_comparison(
        baseline_manifest,
        candidate_manifest,
        baseline_dir,
        candidate_dir,
        baseline_model,
        candidate_model,
        quality_corpus,
        variable_contract,
    )
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["output"]

    if expected is not None and supplied != expected:
        errors.append(
            "quality execution-variable comparison artifact does not exactly match "
            "independently rebuilt sealed evidence + variable contract"
        )

    return {
        "errors": errors,
        "supplied": supplied,
        "expected": expected,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Independently rebuild and verify an I39 execution-variable quality comparison."
        )
    )
    p.add_argument("--quality-comparison", type=Path, required=True)
    p.add_argument("--baseline-manifest", type=Path, required=True)
    p.add_argument("--candidate-manifest", type=Path, required=True)
    p.add_argument("--baseline-dir", type=Path, required=True)
    p.add_argument("--candidate-dir", type=Path, required=True)
    p.add_argument("--baseline-model", type=Path, required=True)
    p.add_argument("--candidate-model", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--variable-contract", type=Path, required=True)
    a = p.parse_args()

    result = verify_execution_variable_quality_comparison(
        a.quality_comparison,
        a.baseline_manifest,
        a.candidate_manifest,
        a.baseline_dir,
        a.candidate_dir,
        a.baseline_model,
        a.candidate_model,
        a.quality_corpus,
        a.variable_contract,
    )

    print("QUALITY EXECUTION-VARIABLE COMPARISON VERIFICATION")
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"]:
        print("QUALITY VARIABLE COMPARISON ARTIFACT: BLOCKED")
        raise SystemExit(2)

    print("QUALITY VARIABLE COMPARISON ARTIFACT: PASS")
    print(
        "PASS means the v2 execution-variable comparison exactly reproduces the sealed "
        "quality bundles, Experiment 61 manifests and declared variable contract."
    )


if __name__ == "__main__":
    main()

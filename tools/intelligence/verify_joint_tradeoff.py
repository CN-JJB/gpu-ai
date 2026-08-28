#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from bind_performance_quality_ab import (
    build_joint_tradeoff_evidence,
    load_object,
)


def verify_joint_tradeoff_evidence(
    joint_tradeoff,
    baseline_manifest,
    candidate_manifest,
    baseline_benchmark,
    candidate_benchmark,
    quality_comparison,
    baseline_quality_dir,
    candidate_quality_dir,
    baseline_model_artifact,
    candidate_model_artifact,
    quality_corpus,
):
    joint_tradeoff = Path(joint_tradeoff)
    errors = []
    supplied = {}
    if not joint_tradeoff.is_file():
        errors.append(f"joint tradeoff is not a file: {joint_tradeoff}")
    else:
        supplied = load_object(joint_tradeoff, "joint tradeoff", errors)

    rebuilt = build_joint_tradeoff_evidence(
        baseline_manifest,
        candidate_manifest,
        baseline_benchmark,
        candidate_benchmark,
        quality_comparison,
        baseline_quality_dir,
        candidate_quality_dir,
        baseline_model_artifact,
        candidate_model_artifact,
        quality_corpus,
    )
    errors.extend("source evidence: " + x for x in rebuilt["errors"])

    expected = rebuilt["output"]
    if expected is not None and supplied != expected:
        errors.append(
            "joint tradeoff artifact does not exactly match independently rebuilt "
            "performance + quality evidence"
        )

    return {
        "errors": errors,
        "supplied": supplied,
        "expected": expected,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Independently rebuild and verify an I37 joint PP/TG × PPL tradeoff artifact."
        )
    )
    p.add_argument("--joint-tradeoff", type=Path, required=True)
    p.add_argument("--baseline-manifest", type=Path, required=True)
    p.add_argument("--candidate-manifest", type=Path, required=True)
    p.add_argument("--baseline-benchmark", type=Path, required=True)
    p.add_argument("--candidate-benchmark", type=Path, required=True)
    p.add_argument("--quality-comparison", type=Path, required=True)
    p.add_argument("--baseline-quality-dir", type=Path, required=True)
    p.add_argument("--candidate-quality-dir", type=Path, required=True)
    p.add_argument("--baseline-model-artifact", type=Path, required=True)
    p.add_argument("--candidate-model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    a = p.parse_args()

    result = verify_joint_tradeoff_evidence(
        a.joint_tradeoff,
        a.baseline_manifest,
        a.candidate_manifest,
        a.baseline_benchmark,
        a.candidate_benchmark,
        a.quality_comparison,
        a.baseline_quality_dir,
        a.candidate_quality_dir,
        a.baseline_model_artifact,
        a.candidate_model_artifact,
        a.quality_corpus,
    )

    print("JOINT TRADEOFF VERIFICATION")
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"]:
        print("JOINT TRADEOFF ARTIFACT: BLOCKED")
        raise SystemExit(2)

    print("JOINT TRADEOFF ARTIFACT: PASS")
    print(
        "PASS means the entire schema-v2 PP/TG × PPL artifact is exactly reproducible "
        "from the Experiment 61 and sealed quality evidence roots."
    )
    print("It is still descriptive evidence, not a recommendation.")


if __name__ == "__main__":
    main()

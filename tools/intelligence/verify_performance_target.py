#!/usr/bin/env python3
import argparse
from pathlib import Path

from bind_performance_quality_ab import load_object
from evaluate_performance_target import build_performance_target_result


def verify_performance_target_result(
    result_path,
    policy_path,
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
    variable_contract=None,
):
    result_path = Path(result_path)
    errors = []
    supplied = {}
    if not result_path.is_file():
        errors.append(f"performance target result is not a file: {result_path}")
    else:
        supplied = load_object(result_path, "performance target result", errors)

    rebuilt = build_performance_target_result(
        policy_path,
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
        variable_contract,
    )
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["result"]
    if expected is not None and supplied != expected:
        errors.append(
            "performance target result does not exactly match independently rebuilt "
            "verified tradeoff + policy"
        )
    return {"errors": errors, "supplied": supplied, "expected": expected}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--policy", type=Path, required=True)
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
    p.add_argument("--variable-contract", type=Path)
    a = p.parse_args()

    verified = verify_performance_target_result(
        a.result,
        a.policy,
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
        a.variable_contract,
    )
    print("PERFORMANCE TARGET VERIFICATION")
    print("ERRORS")
    for error in verified["errors"]:
        print("- " + error)
    if verified["errors"]:
        print("PERFORMANCE TARGET ARTIFACT: BLOCKED")
        raise SystemExit(2)
    print("PERFORMANCE TARGET ARTIFACT: PASS")
    print("The policy result is exactly reproducible from the verified tradeoff and policy.")


if __name__ == "__main__":
    main()

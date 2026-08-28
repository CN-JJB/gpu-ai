#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from compare_quality_metrics import (
    build_exact_quality_comparison,
    load_object,
    verify_bundle,
)


def verify_exact_quality_comparison_evidence(
    comparison_path,
    baseline_dir,
    candidate_dir,
    baseline_model,
    candidate_model,
    quality_corpus,
):
    comparison_path = Path(comparison_path)
    baseline_dir = Path(baseline_dir)
    candidate_dir = Path(candidate_dir)
    baseline_model = Path(baseline_model)
    candidate_model = Path(candidate_model)
    quality_corpus = Path(quality_corpus)

    errors = []
    for label, path in (
        ("quality comparison", comparison_path),
        ("baseline model", baseline_model),
        ("candidate model", candidate_model),
        ("quality corpus", quality_corpus),
    ):
        if not path.is_file():
            errors.append(f"{label} is not a file: {path}")

    comparison = {}
    if comparison_path.is_file():
        comparison = load_object(
            comparison_path, "quality comparison", errors
        )

    baseline = None
    candidate = None
    if (
        baseline_model.is_file()
        and candidate_model.is_file()
        and quality_corpus.is_file()
    ):
        baseline = verify_bundle(
            "baseline",
            baseline_dir,
            baseline_model,
            quality_corpus,
            errors,
        )
        candidate = verify_bundle(
            "candidate",
            candidate_dir,
            candidate_model,
            quality_corpus,
            errors,
        )

    expected = None
    if baseline is not None and candidate is not None:
        expected = build_exact_quality_comparison(
            baseline, candidate, errors
        )

    if expected is not None and comparison != expected:
        errors.append(
            "quality comparison artifact does not exactly match independently "
            "recomputed quality bundles"
        )

    return {
        "errors": errors,
        "comparison": comparison,
        "expected": expected,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Independently verify an I33 quality-comparison.json by rechecking both "
            "sealed quality bundles and reconstructing the comparison object."
        )
    )
    p.add_argument("--quality-comparison", type=Path, required=True)
    p.add_argument("--baseline-dir", type=Path, required=True)
    p.add_argument("--candidate-dir", type=Path, required=True)
    p.add_argument("--baseline-model", type=Path, required=True)
    p.add_argument("--candidate-model", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    a = p.parse_args()

    result = verify_exact_quality_comparison_evidence(
        a.quality_comparison,
        a.baseline_dir,
        a.candidate_dir,
        a.baseline_model,
        a.candidate_model,
        a.quality_corpus,
    )

    print("QUALITY COMPARISON VERIFICATION")
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"]:
        print("QUALITY COMPARISON ARTIFACT: BLOCKED")
        raise SystemExit(2)

    print("QUALITY COMPARISON ARTIFACT: PASS")
    print(
        "PASS means the comparison artifact is exactly reproducible from both sealed "
        "quality bundles. It is still descriptive quality evidence, not a recommendation."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from bind_performance_quality_ab import (
    bind_benchmark,
    load_object,
    perf_delta,
    sha256_file,
)
from experiment61_ab_contract import get_path, validate_manifest_pair
from verify_quality_execution_variable_comparison import (
    verify_execution_variable_quality_comparison,
)


TRADEOFF_CONTRACT = "experiment61-execution-performance-quality-v1"
QUALITY_COMPARISON_CONTRACT = "ppl-declared-execution-variable-v2"
FIXED_QUALITY_FIELDS = (
    "tokenizer_identity",
    "corpus_sha256",
    "fixture_revision",
)


def compare_field(actual, expected, label, errors):
    if actual != expected:
        errors.append(f"{label} mismatch: actual={actual!r} expected={expected!r}")


def validate_quality_against_manifests(
    quality,
    manifest_contract,
    baseline_manifest,
    candidate_manifest,
    variable_contract_path,
    errors,
):
    if quality.get("quality_comparison_schema_version") != 2:
        errors.append("quality comparison schema version must be 2")
    if quality.get("comparison_contract") != QUALITY_COMPARISON_CONTRACT:
        errors.append(
            f"quality comparison contract must be {QUALITY_COMPARISON_CONTRACT!r}"
        )
    if quality.get("comparison_id") != manifest_contract.get("comparison_id"):
        errors.append("quality comparison_id does not match Experiment 61 manifests")
    if quality.get("intentional_variable") != manifest_contract.get(
        "intentional_variable"
    ):
        errors.append(
            "quality intentional_variable does not match Experiment 61 manifests"
        )
    if quality.get("metric") != "PPL":
        errors.append("quality metric must be PPL")
    if quality.get("lower_is_better") is not True:
        errors.append("quality comparison must declare lower_is_better=true")

    intentional_variable = manifest_contract.get("intentional_variable")
    if not (
        isinstance(intentional_variable, str)
        and intentional_variable.startswith("variant.execution.")
    ):
        errors.append(
            "execution joint tradeoff requires intentional_variable under variant.execution.*"
        )
        return None

    declared = quality.get("declared_variable") or {}
    compare_field(
        declared.get("path"),
        intentional_variable,
        "quality declared variable path",
        errors,
    )
    compare_field(
        declared.get("baseline_value"),
        get_path(baseline_manifest, intentional_variable),
        "quality declared baseline value",
        errors,
    )
    compare_field(
        declared.get("candidate_value"),
        get_path(candidate_manifest, intentional_variable),
        "quality declared candidate value",
        errors,
    )

    fixed_quality = quality.get("fixed_quality_identity") or {}
    for field in FIXED_QUALITY_FIELDS:
        compare_field(
            fixed_quality.get(field),
            get_path(baseline_manifest, f"fixed.quality_eval.{field}"),
            f"quality fixed {field} vs baseline manifest",
            errors,
        )
        compare_field(
            fixed_quality.get(field),
            get_path(candidate_manifest, f"fixed.quality_eval.{field}"),
            f"quality fixed {field} vs candidate manifest",
            errors,
        )

    for side, manifest in (
        ("baseline", baseline_manifest),
        ("candidate", candidate_manifest),
    ):
        qside = quality.get(side) or {}
        model = get_path(manifest, "variant.model") or {}
        compare_field(
            qside.get("model_sha256"),
            model.get("artifact_sha256"),
            f"quality {side} model_sha256",
            errors,
        )
        compare_field(
            qside.get("model_bytes"),
            model.get("artifact_bytes"),
            f"quality {side} model_bytes",
            errors,
        )

    evidence = quality.get("evidence") or {}
    if Path(variable_contract_path).is_file():
        compare_field(
            evidence.get("variable_contract_sha256"),
            sha256_file(Path(variable_contract_path)),
            "quality variable contract SHA256",
            errors,
        )

    baseline = quality.get("baseline") or {}
    candidate = quality.get("candidate") or {}
    bppl = baseline.get("value")
    cppl = candidate.get("value")
    if not (
        isinstance(bppl, (int, float))
        and not isinstance(bppl, bool)
        and math.isfinite(float(bppl))
        and bppl > 0
        and isinstance(cppl, (int, float))
        and not isinstance(cppl, bool)
        and math.isfinite(float(cppl))
        and cppl > 0
    ):
        errors.append("quality comparison baseline/candidate PPL must be finite and > 0")
        return None

    bppl = float(bppl)
    cppl = float(cppl)
    ratio = cppl / bppl

    for actual, expected, label in (
        (
            quality.get("delta_candidate_minus_baseline"),
            cppl - bppl,
            "quality delta_candidate_minus_baseline",
        ),
        (
            quality.get("ratio_candidate_to_baseline"),
            ratio,
            "quality ratio_candidate_to_baseline",
        ),
        (
            quality.get("percent_change"),
            (ratio - 1.0) * 100.0,
            "quality percent_change",
        ),
    ):
        if (
            not isinstance(actual, (int, float))
            or isinstance(actual, bool)
            or not math.isclose(
                float(actual), expected, rel_tol=1e-12, abs_tol=1e-12
            )
        ):
            errors.append(f"{label} does not reproduce PPL arithmetic")

    return {
        "baseline_ppl": bppl,
        "candidate_ppl": cppl,
        "delta": cppl - bppl,
        "ratio": ratio,
        "percent_change": (ratio - 1.0) * 100.0,
        "baseline_uncertainty": baseline.get("reported_uncertainty"),
        "candidate_uncertainty": candidate.get("reported_uncertainty"),
    }


def build_execution_joint_tradeoff_evidence(
    baseline_manifest_path,
    candidate_manifest_path,
    baseline_benchmark_path,
    candidate_benchmark_path,
    quality_comparison_path,
    baseline_quality_dir,
    candidate_quality_dir,
    baseline_model_artifact,
    candidate_model_artifact,
    quality_corpus,
    variable_contract_path,
):
    baseline_manifest_path = Path(baseline_manifest_path)
    candidate_manifest_path = Path(candidate_manifest_path)
    baseline_benchmark_path = Path(baseline_benchmark_path)
    candidate_benchmark_path = Path(candidate_benchmark_path)
    quality_comparison_path = Path(quality_comparison_path)
    baseline_quality_dir = Path(baseline_quality_dir)
    candidate_quality_dir = Path(candidate_quality_dir)
    baseline_model_artifact = Path(baseline_model_artifact)
    candidate_model_artifact = Path(candidate_model_artifact)
    quality_corpus = Path(quality_corpus)
    variable_contract_path = Path(variable_contract_path)

    errors = []
    baseline_manifest = load_object(
        baseline_manifest_path, "baseline manifest", errors
    )
    candidate_manifest = load_object(
        candidate_manifest_path, "candidate manifest", errors
    )
    baseline_benchmark = load_object(
        baseline_benchmark_path, "baseline benchmark", errors
    )
    candidate_benchmark = load_object(
        candidate_benchmark_path, "candidate benchmark", errors
    )

    quality_result = verify_execution_variable_quality_comparison(
        quality_comparison_path,
        baseline_manifest_path,
        candidate_manifest_path,
        baseline_quality_dir,
        candidate_quality_dir,
        baseline_model_artifact,
        candidate_model_artifact,
        quality_corpus,
        variable_contract_path,
    )
    errors.extend(
        "quality comparison evidence: " + error
        for error in quality_result["errors"]
    )
    quality = quality_result["supplied"] if not quality_result["errors"] else {}

    manifest_contract = None
    if baseline_manifest and candidate_manifest:
        manifest_contract = validate_manifest_pair(
            baseline_manifest, candidate_manifest
        )
        errors.extend(
            "manifest contract: " + x for x in manifest_contract["errors"]
        )
        declared = manifest_contract.get("intentional_variable")
        if not (
            isinstance(declared, str)
            and declared.startswith("variant.execution.")
        ):
            errors.append(
                "execution joint tradeoff requires intentional_variable under variant.execution.*"
            )

    baseline_metrics = {}
    candidate_metrics = {}
    if baseline_manifest and baseline_benchmark:
        baseline_metrics = bind_benchmark(
            "baseline", baseline_manifest, baseline_benchmark, errors
        )
    if candidate_manifest and candidate_benchmark:
        candidate_metrics = bind_benchmark(
            "candidate", candidate_manifest, candidate_benchmark, errors
        )

    quality_metrics = None
    if quality and manifest_contract and baseline_manifest and candidate_manifest:
        quality_metrics = validate_quality_against_manifests(
            quality,
            manifest_contract,
            baseline_manifest,
            candidate_manifest,
            variable_contract_path,
            errors,
        )

    output = None
    if (
        not errors
        and manifest_contract is not None
        and quality_metrics is not None
        and all(key in baseline_metrics for key in ("pp_tok_s", "tg_tok_s"))
        and all(key in candidate_metrics for key in ("pp_tok_s", "tg_tok_s"))
    ):
        intentional_variable = manifest_contract["intentional_variable"]
        evidence = quality.get("evidence") or {}
        output = {
            "joint_tradeoff_schema_version": 1,
            "tradeoff_contract": TRADEOFF_CONTRACT,
            "comparison_id": manifest_contract["comparison_id"],
            "intentional_variable": intentional_variable,
            "semantic_differences": manifest_contract["semantic_differences"],
            "model_sha256": get_path(
                baseline_manifest, "variant.model.artifact_sha256"
            ),
            "declared_variable": {
                "path": intentional_variable,
                "baseline_value": get_path(
                    baseline_manifest, intentional_variable
                ),
                "candidate_value": get_path(
                    candidate_manifest, intentional_variable
                ),
            },
            "performance": {
                "pp_tok_s": perf_delta(
                    baseline_metrics["pp_tok_s"],
                    candidate_metrics["pp_tok_s"],
                ),
                "tg_tok_s": perf_delta(
                    baseline_metrics["tg_tok_s"],
                    candidate_metrics["tg_tok_s"],
                ),
            },
            "quality": {
                "metric": "PPL",
                "lower_is_better": True,
                "baseline": quality_metrics["baseline_ppl"],
                "candidate": quality_metrics["candidate_ppl"],
                "delta_candidate_minus_baseline": quality_metrics["delta"],
                "ratio_candidate_to_baseline": quality_metrics["ratio"],
                "percent_change": quality_metrics["percent_change"],
                "baseline_reported_uncertainty": quality_metrics[
                    "baseline_uncertainty"
                ],
                "candidate_reported_uncertainty": quality_metrics[
                    "candidate_uncertainty"
                ],
            },
            "evaluation_args": quality.get("evaluation_args"),
            "quality_evidence": {
                "comparison_sha256": sha256_file(quality_comparison_path),
                "comparison_contract": quality.get("comparison_contract"),
                "variable_contract_sha256": evidence.get(
                    "variable_contract_sha256"
                ),
                "baseline_metric_sha256": evidence.get(
                    "baseline_metric_sha256"
                ),
                "candidate_metric_sha256": evidence.get(
                    "candidate_metric_sha256"
                ),
                "verification": "INDEPENDENTLY-REPRODUCED-I39",
            },
        }

    return {
        "errors": errors,
        "output": output,
        "manifest_contract": manifest_contract,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Bind an independently reproducible I39 execution-variable PPL A/B "
            "to the same Experiment 61 PP/TG A/B."
        )
    )
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
    p.add_argument("--variable-contract", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    result = build_execution_joint_tradeoff_evidence(
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

    errors = result["errors"]
    output = result["output"]
    manifest_contract = result["manifest_contract"]

    print("EXECUTION PERFORMANCE × QUALITY A/B BINDING")
    if manifest_contract is not None:
        print(f"comparison_id={manifest_contract.get('comparison_id')}")
        print(
            f"intentional_variable={manifest_contract.get('intentional_variable')}"
        )
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors or output is None:
        print("EXECUTION JOINT TRADEOFF: BLOCKED")
        raise SystemExit(2)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        f"PP percent_change={output['performance']['pp_tok_s']['percent_change']}"
    )
    print(
        f"TG percent_change={output['performance']['tg_tok_s']['percent_change']}"
    )
    print(f"PPL percent_change={output['quality']['percent_change']}")
    print("quality_comparison_verification=INDEPENDENTLY-REPRODUCED-I39")
    print(f"out={a.out}")
    print("EXECUTION JOINT TRADEOFF: PASS")
    print(
        "PASS is a descriptive binding of one declared execution-variable A/B across "
        "performance and PPL. It is not a significance test, semantic flag proof, "
        "ACCEPT/REJECT, or purchase recommendation."
    )


if __name__ == "__main__":
    main()

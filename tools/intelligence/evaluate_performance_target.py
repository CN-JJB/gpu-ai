#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from pathlib import Path

from bind_performance_quality_ab import load_object
from verify_tradeoff_route import verify_tradeoff_route


POLICY_CONTRACT = "explicit-candidate-performance-target-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value))


def positive_or_null(value):
    return value is None or (finite(value) and float(value) > 0)


def build_performance_target_result(
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
    policy_path = Path(policy_path)
    joint_tradeoff = Path(joint_tradeoff)
    baseline_benchmark = Path(baseline_benchmark)
    candidate_benchmark = Path(candidate_benchmark)

    errors = []
    policy = {}
    if not policy_path.is_file():
        errors.append(f"performance target policy is not a file: {policy_path}")
    else:
        policy = load_object(policy_path, "performance target policy", errors)

    route = verify_tradeoff_route(
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
    errors.extend("tradeoff route: " + x for x in route["errors"])

    joint = {}
    baseline = {}
    candidate = {}
    if joint_tradeoff.is_file():
        joint = load_object(joint_tradeoff, "joint tradeoff", errors)
    if baseline_benchmark.is_file():
        baseline = load_object(baseline_benchmark, "baseline benchmark", errors)
    if candidate_benchmark.is_file():
        candidate = load_object(candidate_benchmark, "candidate benchmark", errors)

    requirements = {}
    if policy:
        if policy.get("performance_target_policy_schema_version") != 1:
            errors.append("performance_target_policy_schema_version must be 1")
        if not isinstance(policy.get("policy_id"), str) or not policy.get("policy_id"):
            errors.append("policy_id must be non-empty")
        expected_comparison = (
            route["contract"].get("comparison_id")
            if route["contract"] is not None
            else None
        )
        if policy.get("comparison_id") != expected_comparison:
            errors.append(
                "performance target policy comparison_id does not match verified tradeoff"
            )
        requirements = policy.get("requirements")
        if not isinstance(requirements, dict):
            errors.append("policy requirements must be an object")
            requirements = {}

    allowed = {
        "min_pp_tok_s",
        "min_tg_tok_s",
        "max_candidate_ppl",
        "max_ppl_percent_change",
    }
    unknown = sorted(set(requirements) - allowed)
    if unknown:
        errors.append("unknown performance target requirements: " + ", ".join(unknown))

    for field in ("min_pp_tok_s", "min_tg_tok_s", "max_candidate_ppl"):
        if not positive_or_null(requirements.get(field)):
            errors.append(f"{field} must be finite > 0 or null")
    change = requirements.get("max_ppl_percent_change")
    if change is not None and not finite(change):
        errors.append("max_ppl_percent_change must be finite numeric or null")

    active = {
        key: value for key, value in requirements.items()
        if key in allowed and value is not None
    }
    if not active:
        errors.append("performance target policy must declare at least one active requirement")

    actual = {}
    if joint:
        performance = joint.get("performance") or {}
        quality = joint.get("quality") or {}
        pp = (performance.get("pp_tok_s") or {}).get("candidate")
        tg = (performance.get("tg_tok_s") or {}).get("candidate")
        ppl = quality.get("candidate")
        ppl_change = quality.get("percent_change")
        for label, value in (
            ("candidate PP", pp),
            ("candidate TG", tg),
            ("candidate PPL", ppl),
            ("PPL percent change", ppl_change),
        ):
            if not finite(value):
                errors.append(f"{label} must be finite in joint tradeoff")
        if not errors:
            actual = {
                "pp_tok_s": float(pp),
                "tg_tok_s": float(tg),
                "ppl": float(ppl),
                "ppl_percent_change": float(ppl_change),
            }

    checks = []
    if not errors and actual:
        mapping = (
            ("min_pp_tok_s", "pp_tok_s", ">="),
            ("min_tg_tok_s", "tg_tok_s", ">="),
            ("max_candidate_ppl", "ppl", "<="),
            ("max_ppl_percent_change", "ppl_percent_change", "<="),
        )
        for policy_field, actual_field, op in mapping:
            threshold = requirements.get(policy_field)
            if threshold is None:
                continue
            observed = actual[actual_field]
            passed = (
                observed >= float(threshold)
                if op == ">="
                else observed <= float(threshold)
            )
            checks.append(
                {
                    "requirement": policy_field,
                    "operator": op,
                    "threshold": float(threshold),
                    "actual": observed,
                    "status": "PASS" if passed else "FAIL",
                }
            )

    result = None
    if not errors and checks:
        decision = "PASS" if all(x["status"] == "PASS" for x in checks) else "FAIL"
        result = {
            "performance_target_result_schema_version": 1,
            "policy_contract": POLICY_CONTRACT,
            "policy_id": policy["policy_id"],
            "comparison_id": policy["comparison_id"],
            "route": route["route"],
            "synthetic_input": bool(
                baseline.get("synthetic", False)
                or candidate.get("synthetic", False)
            ),
            "actual": actual,
            "checks": checks,
            "decision": decision,
            "evidence": {
                "policy_sha256": sha256_file(policy_path),
                "joint_tradeoff_sha256": sha256_file(joint_tradeoff),
            },
            "scope": "EXPLICIT_POLICY_ONLY_NO_WEIGHTED_SCORE",
        }

    return {"errors": errors, "result": result}


def main():
    p = argparse.ArgumentParser(
        description=(
            "Evaluate an explicit no-weight performance/PPL target policy against a "
            "fully verified I42 tradeoff route."
        )
    )
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
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    built = build_performance_target_result(
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

    print("PERFORMANCE TARGET POLICY")
    print("ERRORS")
    for error in built["errors"]:
        print("- " + error)

    if built["errors"] or built["result"] is None:
        print("PERFORMANCE TARGET: BLOCKED")
        raise SystemExit(2)

    result = built["result"]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    for check in result["checks"]:
        print(
            f"- {check['requirement']}: {check['status']} | "
            f"actual={check['actual']} {check['operator']} {check['threshold']}"
        )
    print(f"synthetic_input={result['synthetic_input']}")
    print(f"PERFORMANCE TARGET: {result['decision']}")
    print(f"out={a.out}")
    print(
        "This is an explicit threshold policy evaluation, not a weighted score or "
        "purchase recommendation."
    )


if __name__ == "__main__":
    main()

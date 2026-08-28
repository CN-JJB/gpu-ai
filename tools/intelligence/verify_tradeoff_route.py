#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

from bind_performance_quality_ab import load_object
from experiment61_ab_contract import validate_manifest_pair
from verify_execution_joint_tradeoff import verify_execution_joint_tradeoff
from verify_joint_tradeoff import verify_joint_tradeoff_evidence


MODEL_ROUTE = "MODEL_ARTIFACT_I38"
EXECUTION_ROUTE = "EXECUTION_VARIABLE_I41"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def select_route(intentional_variable):
    if intentional_variable == "variant.model" or (
        isinstance(intentional_variable, str)
        and intentional_variable.startswith("variant.model.")
    ):
        return MODEL_ROUTE
    if isinstance(intentional_variable, str) and intentional_variable.startswith(
        "variant.execution."
    ):
        return EXECUTION_ROUTE
    return None


def verify_tradeoff_route(
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
    joint_tradeoff = Path(joint_tradeoff)
    baseline_manifest = Path(baseline_manifest)
    candidate_manifest = Path(candidate_manifest)
    baseline_benchmark = Path(baseline_benchmark)
    candidate_benchmark = Path(candidate_benchmark)
    quality_comparison = Path(quality_comparison)
    baseline_quality_dir = Path(baseline_quality_dir)
    candidate_quality_dir = Path(candidate_quality_dir)
    baseline_model_artifact = Path(baseline_model_artifact)
    candidate_model_artifact = Path(candidate_model_artifact)
    quality_corpus = Path(quality_corpus)
    variable_contract = Path(variable_contract) if variable_contract is not None else None

    errors = []
    baseline_obj = {}
    candidate_obj = {}
    if not baseline_manifest.is_file():
        errors.append(f"baseline manifest is not a file: {baseline_manifest}")
    else:
        baseline_obj = load_object(baseline_manifest, "baseline manifest", errors)
    if not candidate_manifest.is_file():
        errors.append(f"candidate manifest is not a file: {candidate_manifest}")
    else:
        candidate_obj = load_object(candidate_manifest, "candidate manifest", errors)

    contract = None
    route = None
    if baseline_obj and candidate_obj:
        contract = validate_manifest_pair(baseline_obj, candidate_obj)
        errors.extend("manifest contract: " + x for x in contract["errors"])
        route = select_route(contract.get("intentional_variable"))
        if route is None:
            errors.append(
                "unsupported tradeoff route for intentional_variable="
                f"{contract.get('intentional_variable')!r}; "
                "supported routes are variant.model* and variant.execution.*"
            )

    verification = None
    if not errors and route == MODEL_ROUTE:
        if variable_contract is not None:
            errors.append(
                "model-artifact tradeoff route does not accept --variable-contract"
            )
        else:
            verification = verify_joint_tradeoff_evidence(
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
            )
            errors.extend(
                "I38 model route: " + x for x in verification["errors"]
            )

    if not errors and route == EXECUTION_ROUTE:
        if variable_contract is None:
            errors.append(
                "execution-variable tradeoff route requires --variable-contract"
            )
        elif not variable_contract.is_file():
            errors.append(
                f"variable contract is not a file: {variable_contract}"
            )
        else:
            verification = verify_execution_joint_tradeoff(
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
            errors.extend(
                "I41 execution route: " + x for x in verification["errors"]
            )

    envelope = None
    if not errors and contract is not None and route is not None:
        joint_obj = load_object(joint_tradeoff, "joint tradeoff", errors)
        if not errors and joint_obj:
            sources = {
                "joint_tradeoff_sha256": sha256_file(joint_tradeoff),
                "baseline_manifest_sha256": sha256_file(baseline_manifest),
                "candidate_manifest_sha256": sha256_file(candidate_manifest),
                "baseline_benchmark_sha256": sha256_file(baseline_benchmark),
                "candidate_benchmark_sha256": sha256_file(candidate_benchmark),
                "quality_comparison_sha256": sha256_file(quality_comparison),
            }
            if variable_contract is not None:
                sources["variable_contract_sha256"] = sha256_file(
                    variable_contract
                )

            envelope = {
                "verified_tradeoff_schema_version": 1,
                "comparison_id": contract.get("comparison_id"),
                "intentional_variable": contract.get("intentional_variable"),
                "route": route,
                "verifier": "I38" if route == MODEL_ROUTE else "I41",
                "verification": "PASS",
                "joint_tradeoff": {
                    "schema_version": joint_obj.get(
                        "joint_tradeoff_schema_version"
                    ),
                    "tradeoff_contract": joint_obj.get("tradeoff_contract"),
                    "sha256": sources["joint_tradeoff_sha256"],
                },
                "sources": sources,
                "scope": "DESCRIPTIVE_ONLY",
            }

    return {
        "errors": errors,
        "route": route,
        "contract": contract,
        "envelope": envelope,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Automatically route Experiment 61 joint evidence to the correct verified "
            "model-artifact (I38) or execution-variable (I41) tradeoff verifier."
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
    p.add_argument("--variable-contract", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    result = verify_tradeoff_route(
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

    print("UNIFIED VERIFIED TRADEOFF ROUTE")
    print(f"route={result['route']}")
    if result["contract"] is not None:
        print(f"comparison_id={result['contract'].get('comparison_id')}")
        print(
            "intentional_variable="
            f"{result['contract'].get('intentional_variable')}"
        )
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"] or result["envelope"] is None:
        print("VERIFIED TRADEOFF ROUTE: BLOCKED")
        raise SystemExit(2)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(result["envelope"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"verifier={result['envelope']['verifier']}")
    print(f"out={a.out}")
    print("VERIFIED TRADEOFF ROUTE: PASS")
    print(
        "PASS selects and verifies the evidence route only. It does not score, rank, "
        "accept, reject, or recommend hardware."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

from experiment61_ab_contract import get_path, validate_manifest_pair
from verify_quality_metric import verify_quality_metric_evidence


COMPARISON_CONTRACT = "ppl-declared-execution-variable-v1"
FIXED_QUALITY_FIELDS = (
    "tokenizer_identity",
    "corpus_sha256",
    "fixture_revision",
)


def load_object(path, label, errors):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(obj, dict):
        errors.append(f"{label}: expected one JSON object")
        return {}
    return obj


def bundle_paths(root):
    return {
        "command": root / "quality-command.json",
        "stdout": root / "stdout.txt",
        "stderr": root / "stderr.txt",
        "packet": root / "PACKET.json",
        "identity": root / "quality-identity.json",
        "metric": root / "quality-metric.json",
    }


def verify_bundle(label, root, model, corpus, errors):
    paths = bundle_paths(root)
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"{label}: missing {name}: {path}")
    if any(not path.is_file() for path in paths.values()):
        return None

    result = verify_quality_metric_evidence(
        paths["metric"],
        paths["command"],
        paths["stdout"],
        paths["stderr"],
        paths["packet"],
        model,
        corpus,
        paths["identity"],
    )
    errors.extend(f"{label}: {x}" for x in result["errors"])
    if result["errors"]:
        return None

    identity = load_object(paths["identity"], f"{label} identity", errors)
    command = load_object(paths["command"], f"{label} command", errors)
    if not identity or not command:
        return None

    executable = command.get("executable")
    if not isinstance(executable, dict):
        errors.append(f"{label}: command missing executable identity")
        return None
    executable_sha = executable.get("sha256")
    executable_bytes = executable.get("bytes")
    if not isinstance(executable_sha, str) or len(executable_sha) != 64:
        errors.append(
            f"{label}: execution-variable comparison requires a hashable executable SHA256"
        )
    if not isinstance(executable_bytes, int) or executable_bytes <= 0:
        errors.append(
            f"{label}: execution-variable comparison requires executable byte count"
        )

    model_binding = command.get("model_artifact")
    if not isinstance(model_binding, dict):
        errors.append(f"{label}: command missing model artifact binding")
        return None

    return {
        "identity": identity,
        "command": command,
        "metric": result["metric"],
        "executable_sha256": executable_sha,
        "executable_bytes": executable_bytes,
        "model_sha256": model_binding.get("sha256"),
        "model_bytes": model_binding.get("bytes"),
    }


def validate_declared_contract(
    contract,
    manifest_contract,
    baseline_manifest,
    candidate_manifest,
    baseline_bundle,
    candidate_bundle,
    errors,
):
    if contract.get("quality_variable_contract_schema_version") != 1:
        errors.append("quality variable contract schema version must be 1")

    comparison_id = manifest_contract.get("comparison_id")
    intentional_variable = manifest_contract.get("intentional_variable")

    if contract.get("comparison_id") != comparison_id:
        errors.append(
            "quality variable contract comparison_id does not match Experiment 61 manifests"
        )
    if contract.get("intentional_variable") != intentional_variable:
        errors.append(
            "quality variable contract intentional_variable does not match Experiment 61 manifests"
        )

    if not (
        isinstance(intentional_variable, str)
        and intentional_variable.startswith("variant.execution.")
    ):
        errors.append(
            "I35 supports only declared variant.execution.* quality-variable contracts"
        )
        return

    baseline_value = get_path(baseline_manifest, intentional_variable)
    candidate_value = get_path(candidate_manifest, intentional_variable)

    baseline_contract = contract.get("baseline")
    candidate_contract = contract.get("candidate")
    if not isinstance(baseline_contract, dict):
        errors.append("quality variable contract missing baseline object")
        baseline_contract = {}
    if not isinstance(candidate_contract, dict):
        errors.append("quality variable contract missing candidate object")
        candidate_contract = {}

    if baseline_contract.get("manifest_value") != baseline_value:
        errors.append(
            "quality variable contract baseline manifest_value does not match baseline manifest"
        )
    if candidate_contract.get("manifest_value") != candidate_value:
        errors.append(
            "quality variable contract candidate manifest_value does not match candidate manifest"
        )

    baseline_args = baseline_contract.get("evaluation_args")
    candidate_args = candidate_contract.get("evaluation_args")
    for label, args in (("baseline", baseline_args), ("candidate", candidate_args)):
        if not (
            isinstance(args, list)
            and all(isinstance(token, str) and token != "" for token in args)
        ):
            errors.append(
                f"quality variable contract {label} evaluation_args must be a JSON list of non-empty strings"
            )

    if baseline_args == candidate_args:
        errors.append(
            "execution-variable quality comparison requires baseline/candidate evaluation_args to differ"
        )

    if baseline_bundle is not None:
        if baseline_bundle["identity"].get("evaluation_args") != baseline_args:
            errors.append(
                "baseline quality identity evaluation_args do not match quality variable contract"
            )
    if candidate_bundle is not None:
        if candidate_bundle["identity"].get("evaluation_args") != candidate_args:
            errors.append(
                "candidate quality identity evaluation_args do not match quality variable contract"
            )


def main():
    p = argparse.ArgumentParser(
        description=(
            "Compare two verified quality bundles for a declared Experiment 61 execution "
            "variable whose baseline/candidate evaluation argv are explicitly contracted."
        )
    )
    p.add_argument("--baseline-manifest", type=Path, required=True)
    p.add_argument("--candidate-manifest", type=Path, required=True)
    p.add_argument("--baseline-dir", type=Path, required=True)
    p.add_argument("--candidate-dir", type=Path, required=True)
    p.add_argument("--baseline-model", type=Path, required=True)
    p.add_argument("--candidate-model", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--variable-contract", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    errors = []
    for label, path in (
        ("baseline model", a.baseline_model),
        ("candidate model", a.candidate_model),
        ("quality corpus", a.quality_corpus),
    ):
        if not path.is_file():
            errors.append(f"{label} is not a file: {path}")

    baseline_manifest = load_object(a.baseline_manifest, "baseline manifest", errors)
    candidate_manifest = load_object(a.candidate_manifest, "candidate manifest", errors)
    variable_contract = load_object(a.variable_contract, "quality variable contract", errors)

    manifest_contract = None
    if baseline_manifest and candidate_manifest:
        manifest_contract = validate_manifest_pair(
            baseline_manifest, candidate_manifest
        )
        errors.extend(
            "manifest contract: " + x for x in manifest_contract["errors"]
        )

    baseline_bundle = None
    candidate_bundle = None
    if not any(not path.is_file() for path in (
        a.baseline_model,
        a.candidate_model,
        a.quality_corpus,
    )):
        baseline_bundle = verify_bundle(
            "baseline",
            a.baseline_dir,
            a.baseline_model,
            a.quality_corpus,
            errors,
        )
        candidate_bundle = verify_bundle(
            "candidate",
            a.candidate_dir,
            a.candidate_model,
            a.quality_corpus,
            errors,
        )

    if (
        manifest_contract is not None
        and variable_contract
        and baseline_bundle is not None
        and candidate_bundle is not None
    ):
        validate_declared_contract(
            variable_contract,
            manifest_contract,
            baseline_manifest,
            candidate_manifest,
            baseline_bundle,
            candidate_bundle,
            errors,
        )

        for field in FIXED_QUALITY_FIELDS:
            left = baseline_bundle["identity"].get(field)
            right = candidate_bundle["identity"].get(field)
            if left != right:
                errors.append(
                    f"quality identity mismatch for fixed field {field}: "
                    f"baseline={left!r} candidate={right!r}"
                )

        if baseline_bundle["executable_sha256"] != candidate_bundle["executable_sha256"]:
            errors.append("quality executable SHA256 differs between baseline and candidate")
        if baseline_bundle["executable_bytes"] != candidate_bundle["executable_bytes"]:
            errors.append("quality executable byte count differs between baseline and candidate")

        baseline_model_manifest = get_path(
            baseline_manifest, "variant.model.artifact_sha256"
        )
        candidate_model_manifest = get_path(
            candidate_manifest, "variant.model.artifact_sha256"
        )
        if baseline_model_manifest != candidate_model_manifest:
            errors.append(
                "execution-variable comparison requires identical model artifact SHA256 in both manifests"
            )
        if baseline_bundle["model_sha256"] != baseline_model_manifest:
            errors.append("baseline quality model SHA256 does not match baseline manifest")
        if candidate_bundle["model_sha256"] != candidate_model_manifest:
            errors.append("candidate quality model SHA256 does not match candidate manifest")

    output = None
    if (
        not errors
        and manifest_contract is not None
        and baseline_bundle is not None
        and candidate_bundle is not None
    ):
        bppl = float(baseline_bundle["metric"]["value"])
        cppl = float(candidate_bundle["metric"]["value"])
        ratio = cppl / bppl
        output = {
            "quality_comparison_schema_version": 1,
            "comparison_contract": COMPARISON_CONTRACT,
            "comparison_id": manifest_contract["comparison_id"],
            "intentional_variable": manifest_contract["intentional_variable"],
            "metric": "PPL",
            "lower_is_better": True,
            "baseline": {
                "value": bppl,
                "reported_uncertainty": baseline_bundle["metric"].get(
                    "reported_uncertainty"
                ),
                "model_sha256": baseline_bundle["model_sha256"],
                "model_bytes": baseline_bundle["model_bytes"],
            },
            "candidate": {
                "value": cppl,
                "reported_uncertainty": candidate_bundle["metric"].get(
                    "reported_uncertainty"
                ),
                "model_sha256": candidate_bundle["model_sha256"],
                "model_bytes": candidate_bundle["model_bytes"],
            },
            "delta_candidate_minus_baseline": cppl - bppl,
            "ratio_candidate_to_baseline": ratio,
            "percent_change": (ratio - 1.0) * 100.0,
            "fixed_quality_identity": {
                field: baseline_bundle["identity"].get(field)
                for field in FIXED_QUALITY_FIELDS
            },
            "evaluation_args": {
                "baseline": baseline_bundle["identity"].get("evaluation_args"),
                "candidate": candidate_bundle["identity"].get("evaluation_args"),
            },
            "declared_variable": {
                "path": manifest_contract["intentional_variable"],
                "baseline_value": get_path(
                    baseline_manifest, manifest_contract["intentional_variable"]
                ),
                "candidate_value": get_path(
                    candidate_manifest, manifest_contract["intentional_variable"]
                ),
            },
            "quality_executable": {
                "sha256": baseline_bundle["executable_sha256"],
                "bytes": baseline_bundle["executable_bytes"],
            },
        }

    print("DECLARED EXECUTION-VARIABLE QUALITY A/B")
    if manifest_contract is not None:
        print(f"comparison_id={manifest_contract.get('comparison_id')}")
        print(f"intentional_variable={manifest_contract.get('intentional_variable')}")
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors or output is None:
        print("QUALITY VARIABLE COMPARISON: BLOCKED")
        raise SystemExit(2)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"baseline_ppl={output['baseline']['value']}")
    print(f"candidate_ppl={output['candidate']['value']}")
    print(f"percent_change={output['percent_change']}")
    print(f"out={a.out}")
    print("QUALITY VARIABLE COMPARISON: PASS")
    print(
        "PASS proves the PPL A/B is bound to an explicit execution-variable manifest/argv "
        "contract. It does not prove the declared argv tokens implement the intended upstream semantics."
    )


if __name__ == "__main__":
    main()

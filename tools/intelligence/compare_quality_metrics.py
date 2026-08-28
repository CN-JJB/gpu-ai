#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from pathlib import Path

from verify_quality_metric import verify_quality_metric_evidence


IDENTITY_FIELDS = (
    "tokenizer_identity",
    "corpus_sha256",
    "fixture_revision",
    "evaluation_args",
)
COMPARISON_CONTRACT = "ppl-exact-quality-identity-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
    metric = result["metric"]
    if not identity or not command or not metric:
        return None

    executable = command.get("executable")
    if not isinstance(executable, dict):
        errors.append(f"{label}: command missing executable identity")
        return None
    executable_sha = executable.get("sha256")
    executable_bytes = executable.get("bytes")
    if not isinstance(executable_sha, str) or len(executable_sha) != 64:
        errors.append(
            f"{label}: exact quality comparison requires a hashable executable SHA256"
        )
    if not isinstance(executable_bytes, int) or executable_bytes <= 0:
        errors.append(
            f"{label}: exact quality comparison requires executable byte count"
        )

    model_record = command.get("model_artifact")
    if not isinstance(model_record, dict):
        errors.append(f"{label}: command missing model artifact binding")
        return None

    return {
        "paths": paths,
        "identity": identity,
        "command": command,
        "metric": metric,
        "executable_sha256": executable_sha,
        "executable_bytes": executable_bytes,
        "model_sha256": model_record.get("sha256"),
        "model_bytes": model_record.get("bytes"),
    }


def compare_contracts(baseline, candidate, errors):
    for field in IDENTITY_FIELDS:
        left = baseline["identity"].get(field)
        right = candidate["identity"].get(field)
        if left != right:
            errors.append(
                f"quality identity mismatch for {field}: "
                f"baseline={left!r} candidate={right!r}"
            )

    if baseline["metric"].get("parser_contract") != candidate["metric"].get(
        "parser_contract"
    ):
        errors.append("quality metric parser_contract differs between baseline and candidate")

    if baseline["metric"].get("metric") != candidate["metric"].get("metric"):
        errors.append("quality metric names differ between baseline and candidate")

    if baseline["executable_sha256"] != candidate["executable_sha256"]:
        errors.append(
            "quality executable SHA256 differs between baseline and candidate"
        )
    if baseline["executable_bytes"] != candidate["executable_bytes"]:
        errors.append(
            "quality executable byte count differs between baseline and candidate"
        )


def build_exact_quality_comparison(baseline, candidate, errors):
    compare_contracts(baseline, candidate, errors)
    if errors:
        return None

    baseline_ppl = float(baseline["metric"]["value"])
    candidate_ppl = float(candidate["metric"]["value"])
    if (
        not math.isfinite(baseline_ppl)
        or baseline_ppl <= 0
        or not math.isfinite(candidate_ppl)
        or candidate_ppl <= 0
    ):
        errors.append("PPL values must be finite and > 0")
        return None

    delta = candidate_ppl - baseline_ppl
    ratio = candidate_ppl / baseline_ppl
    return {
        "quality_comparison_schema_version": 1,
        "comparison_contract": COMPARISON_CONTRACT,
        "metric": "PPL",
        "lower_is_better": True,
        "baseline": {
            "value": baseline_ppl,
            "reported_uncertainty": baseline["metric"].get(
                "reported_uncertainty"
            ),
            "model_sha256": baseline["model_sha256"],
            "model_bytes": baseline["model_bytes"],
            "metric_sha256": sha256_file(baseline["paths"]["metric"]),
        },
        "candidate": {
            "value": candidate_ppl,
            "reported_uncertainty": candidate["metric"].get(
                "reported_uncertainty"
            ),
            "model_sha256": candidate["model_sha256"],
            "model_bytes": candidate["model_bytes"],
            "metric_sha256": sha256_file(candidate["paths"]["metric"]),
        },
        "delta_candidate_minus_baseline": delta,
        "ratio_candidate_to_baseline": ratio,
        "percent_change": (ratio - 1.0) * 100.0,
        "fixed_quality_identity": {
            field: baseline["identity"].get(field)
            for field in IDENTITY_FIELDS
        },
        "quality_executable": {
            "sha256": baseline["executable_sha256"],
            "bytes": baseline["executable_bytes"],
        },
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Verify two I31/I32 quality bundles, require an exact quality identity/build "
            "contract, then compute descriptive PPL delta and ratio."
        )
    )
    p.add_argument("--baseline-dir", type=Path, required=True)
    p.add_argument("--candidate-dir", type=Path, required=True)
    p.add_argument("--baseline-model", type=Path, required=True)
    p.add_argument("--candidate-model", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
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

    baseline = None
    candidate = None
    if not errors:
        baseline = verify_bundle(
            "baseline",
            a.baseline_dir,
            a.baseline_model,
            a.quality_corpus,
            errors,
        )
        candidate = verify_bundle(
            "candidate",
            a.candidate_dir,
            a.candidate_model,
            a.quality_corpus,
            errors,
        )

    comparison = None
    if baseline is not None and candidate is not None:
        comparison = build_exact_quality_comparison(
            baseline, candidate, errors
        )

    print("QUALITY A/B COMPARISON")
    print(f"comparison_contract={COMPARISON_CONTRACT}")
    print("ERRORS")
    for error in errors:
        print("- " + error)

    if errors or comparison is None:
        print("QUALITY COMPARISON: BLOCKED")
        raise SystemExit(2)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(comparison, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"baseline_ppl={comparison['baseline']['value']}")
    print(f"candidate_ppl={comparison['candidate']['value']}")
    print(
        "delta_candidate_minus_baseline="
        f"{comparison['delta_candidate_minus_baseline']}"
    )
    print(
        "ratio_candidate_to_baseline="
        f"{comparison['ratio_candidate_to_baseline']}"
    )
    print(f"percent_change={comparison['percent_change']}")
    print(f"out={a.out}")
    print("QUALITY COMPARISON: PASS")
    print(
        "PASS is a descriptive exact-contract PPL comparison. It is not a causal claim, "
        "task-quality verdict, or purchase recommendation."
    )


if __name__ == "__main__":
    main()

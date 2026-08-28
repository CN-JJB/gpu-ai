#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from extract_quality_metric import (
    PARSER_CONTRACT,
    build_metric_artifact,
    parse_final_estimate,
)
from verify_quality_execution import verify_quality_execution_evidence


def load_metric(path, errors):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid quality metric JSON: {exc}")
        return {}
    if not isinstance(obj, dict):
        errors.append("quality metric must be one JSON object")
        return {}
    return obj


def verify_quality_metric_evidence(
    quality_metric,
    quality_command_record,
    stdout,
    stderr,
    packet,
    model_artifact,
    quality_corpus,
    quality_manifest,
):
    quality_metric = Path(quality_metric)
    quality_command_record = Path(quality_command_record)
    stdout = Path(stdout)
    stderr = Path(stderr)
    packet = Path(packet)
    model_artifact = Path(model_artifact)
    quality_corpus = Path(quality_corpus)
    quality_manifest = Path(quality_manifest)

    errors = []
    if not quality_metric.is_file():
        errors.append(f"quality metric is not a file: {quality_metric}")

    execution = verify_quality_execution_evidence(
        quality_command_record,
        stdout,
        stderr,
        packet,
        model_artifact,
        quality_corpus,
        quality_manifest,
    )
    errors.extend("execution evidence: " + x for x in execution["errors"])

    metric_obj = {}
    if quality_metric.is_file():
        metric_obj = load_metric(quality_metric, errors)

    if metric_obj:
        if metric_obj.get("quality_metric_schema_version") != 1:
            errors.append("quality_metric_schema_version must be 1")
        if metric_obj.get("parser_contract") != PARSER_CONTRACT:
            errors.append(f"parser_contract must be {PARSER_CONTRACT!r}")
        if metric_obj.get("metric") != "PPL":
            errors.append("quality metric name must be PPL")

    parsed = None
    if not execution["errors"]:
        try:
            parsed = parse_final_estimate(stdout, stderr)
        except Exception as exc:
            errors.append(str(exc))

    expected = None
    if parsed is not None:
        expected = build_metric_artifact(
            quality_command_record,
            stdout,
            stderr,
            quality_manifest,
            parsed,
        )
        if metric_obj != expected:
            errors.append(
                "quality metric artifact does not exactly match independently reparsed evidence"
            )

    return {
        "errors": errors,
        "metric": metric_obj,
        "expected": expected,
        "execution": execution,
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Verify an I31 machine-readable PPL artifact by re-checking I28/I30 evidence "
            "and independently reparsing the sealed raw output."
        )
    )
    p.add_argument("--quality-metric", type=Path, required=True)
    p.add_argument("--quality-command-record", type=Path, required=True)
    p.add_argument("--stdout", type=Path, required=True)
    p.add_argument("--stderr", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--quality-manifest", type=Path, required=True)
    a = p.parse_args()

    result = verify_quality_metric_evidence(
        a.quality_metric,
        a.quality_command_record,
        a.stdout,
        a.stderr,
        a.packet,
        a.model_artifact,
        a.quality_corpus,
        a.quality_manifest,
    )

    print("QUALITY METRIC VERIFICATION")
    if result["metric"]:
        print(f"parser_contract={result['metric'].get('parser_contract')}")
        print(f"metric={result['metric'].get('metric')}")
        print(f"value={result['metric'].get('value')}")
        print(
            f"reported_uncertainty={result['metric'].get('reported_uncertainty')}"
        )
    print("ERRORS")
    for error in result["errors"]:
        print("- " + error)

    if result["errors"]:
        print("QUALITY METRIC: BLOCKED")
        raise SystemExit(2)

    print("QUALITY METRIC: PASS")
    print(
        "PASS means the machine-readable metric exactly reproduces the supported raw-output "
        "contract from the sealed execution evidence."
    )
    print(
        "It does not prove universal model quality, statistical sufficiency, or purchase suitability."
    )


if __name__ == "__main__":
    main()

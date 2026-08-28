#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import re
from pathlib import Path

from verify_quality_execution import verify_quality_execution_evidence


PARSER_CONTRACT = "llama-perplexity-final-estimate-v1"
NUMBER = rb"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
FINAL_RE = re.compile(
    rb"^\s*Final estimate:\s*PPL\s*=\s*(" + NUMBER + rb")\s*\+/-\s*(" + NUMBER + rb")\s*$"
)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def evidence_record(path):
    return {
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def parse_final_estimate(stdout_path, stderr_path):
    matches = []
    for stream_name, path in (("stdout", stdout_path), ("stderr", stderr_path)):
        data = path.read_bytes()
        for line_number, line in enumerate(data.splitlines(), start=1):
            match = FINAL_RE.match(line)
            if not match:
                continue

            value = float(match.group(1).decode("ascii"))
            uncertainty = float(match.group(2).decode("ascii"))
            if not math.isfinite(value) or value <= 0:
                raise ValueError(
                    f"{stream_name} line {line_number}: PPL must be finite and > 0"
                )
            if not math.isfinite(uncertainty) or uncertainty < 0:
                raise ValueError(
                    f"{stream_name} line {line_number}: reported uncertainty must be finite and >= 0"
                )

            matches.append(
                {
                    "stream": stream_name,
                    "line_number": line_number,
                    "line_sha256": sha256_bytes(line),
                    "value": value,
                    "reported_uncertainty": uncertainty,
                }
            )

    if not matches:
        raise ValueError(
            "no supported Final estimate PPL line found in stdout/stderr; "
            "do not infer a metric from chunk progress output"
        )
    if len(matches) != 1:
        raise ValueError(
            f"ambiguous quality output: found {len(matches)} Final estimate PPL lines"
        )
    return matches[0]


def build_metric_artifact(
    quality_command_record,
    stdout,
    stderr,
    quality_manifest,
    parsed,
):
    return {
        "quality_metric_schema_version": 1,
        "parser_contract": PARSER_CONTRACT,
        "metric": "PPL",
        "value": parsed["value"],
        "reported_uncertainty": parsed["reported_uncertainty"],
        "source": {
            "stream": parsed["stream"],
            "line_number": parsed["line_number"],
            "line_sha256": parsed["line_sha256"],
        },
        "evidence": {
            "quality_command": evidence_record(quality_command_record),
            "quality_identity": evidence_record(quality_manifest),
            "stdout": evidence_record(stdout),
            "stderr": evidence_record(stderr),
        },
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Fail-closed extraction of the standard llama-perplexity Final estimate "
            "from already sealed I28/I30 quality execution evidence."
        )
    )
    p.add_argument("--quality-command-record", type=Path, required=True)
    p.add_argument("--stdout", type=Path, required=True)
    p.add_argument("--stderr", type=Path, required=True)
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--quality-manifest", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    result = verify_quality_execution_evidence(
        a.quality_command_record,
        a.stdout,
        a.stderr,
        a.packet,
        a.model_artifact,
        a.quality_corpus,
        a.quality_manifest,
    )
    if result["errors"]:
        print("QUALITY METRIC EXTRACTION")
        print("ERRORS")
        for error in result["errors"]:
            print("- execution evidence: " + error)
        print("QUALITY METRIC: BLOCKED")
        raise SystemExit(2)

    try:
        parsed = parse_final_estimate(a.stdout, a.stderr)
    except Exception as exc:
        print("QUALITY METRIC EXTRACTION")
        print("ERRORS")
        print("- " + str(exc))
        print("QUALITY METRIC: BLOCKED")
        raise SystemExit(2)

    artifact = build_metric_artifact(
        a.quality_command_record,
        a.stdout,
        a.stderr,
        a.quality_manifest,
        parsed,
    )
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("QUALITY METRIC EXTRACTION")
    print(f"parser_contract={PARSER_CONTRACT}")
    print("metric=PPL")
    print(f"value={artifact['value']}")
    print(f"reported_uncertainty={artifact['reported_uncertainty']}")
    print(f"source_stream={artifact['source']['stream']}")
    print(f"source_line={artifact['source']['line_number']}")
    print(f"out={a.out}")
    print("QUALITY METRIC: EXTRACTED")
    print(
        "EXTRACTED means a narrow supported raw-output contract was parsed from sealed evidence; "
        "it is not a model-quality or purchase claim."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from quality_execution_test_support import (
    write_packet,
    write_quality_execution_fixture,
)


HERE = Path(__file__).resolve().parent
PY = sys.executable


def run(args, expect=0):
    proc = subprocess.run(args, text=True, capture_output=True)
    out = proc.stdout + proc.stderr
    if proc.returncode != expect:
        print(out)
        raise AssertionError(
            f"expected return code {expect}, got {proc.returncode}: {args}"
        )
    return out


def extract_args(exec_evidence, model, corpus, out):
    return [
        PY,
        str(HERE / "extract_quality_metric.py"),
        "--quality-command-record",
        str(exec_evidence["command"]),
        "--stdout",
        str(exec_evidence["stdout"]),
        "--stderr",
        str(exec_evidence["stderr"]),
        "--packet",
        str(exec_evidence["packet"]),
        "--model-artifact",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(exec_evidence["identity"]),
        "--out",
        str(out),
    ]


def verify_args(exec_evidence, model, corpus, metric):
    return [
        PY,
        str(HERE / "verify_quality_metric.py"),
        "--quality-metric",
        str(metric),
        "--quality-command-record",
        str(exec_evidence["command"]),
        "--stdout",
        str(exec_evidence["stdout"]),
        "--stderr",
        str(exec_evidence["stderr"]),
        "--packet",
        str(exec_evidence["packet"]),
        "--model-artifact",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(exec_evidence["identity"]),
    ]


def reseal(exec_evidence):
    write_packet(
        exec_evidence["packet"],
        [
            exec_evidence["command"],
            exec_evidence["stdout"],
            exec_evidence["stderr"],
            exec_evidence["identity"],
        ],
    )


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"i31-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"i31-corpus\n")

        identity = td / "quality-identity.json"
        identity.write_text(
            json.dumps(
                {
                    "quality_identity_schema_version": 2,
                    "tokenizer_identity": "fixture-tokenizer-i31",
                    "corpus_sha256": __import__("hashlib").sha256(
                        corpus.read_bytes()
                    ).hexdigest(),
                    "fixture_revision": "fixture-i31",
                    "evaluation_args": ["--fixture-eval", "i31"],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        exec_evidence = write_quality_execution_fixture(
            td / "quality-execution",
            model,
            corpus,
            identity,
        )
        exec_evidence["stdout"].write_text(
            "[1]7.5000,[2]7.2500,\n"
            "Final estimate: PPL = 7.2500 +/- 0.10000\n",
            encoding="utf-8",
        )
        reseal(exec_evidence)

        metric = td / "quality-metric.json"
        out = run(extract_args(exec_evidence, model, corpus, metric))
        assert "QUALITY METRIC: EXTRACTED" in out

        obj = json.loads(metric.read_text(encoding="utf-8"))
        assert obj["quality_metric_schema_version"] == 1
        assert obj["parser_contract"] == "llama-perplexity-final-estimate-v1"
        assert obj["metric"] == "PPL"
        assert obj["value"] == 7.25
        assert obj["reported_uncertainty"] == 0.1
        assert obj["source"]["stream"] == "stdout"

        out = run(verify_args(exec_evidence, model, corpus, metric))
        assert "QUALITY METRIC: PASS" in out

        tampered = td / "tampered-metric.json"
        bad = dict(obj)
        bad["value"] = 7.0
        tampered.write_text(
            json.dumps(bad, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        out = run(
            verify_args(exec_evidence, model, corpus, tampered),
            expect=2,
        )
        assert (
            "quality metric artifact does not exactly match independently reparsed evidence"
            in out
        )
        assert "QUALITY METRIC: BLOCKED" in out

        exec_evidence["stdout"].write_text(
            "[1]360.9578,[2]85.1178,[3]63.2695,[4]49.5185,[5]37.1328,"
            "[6]23.8184,[7]17.7486,\n",
            encoding="utf-8",
        )
        reseal(exec_evidence)
        no_final = td / "no-final.json"
        out = run(
            extract_args(exec_evidence, model, corpus, no_final),
            expect=2,
        )
        assert "no supported Final estimate PPL line found" in out
        assert "do not infer a metric from chunk progress output" in out
        assert "QUALITY METRIC: BLOCKED" in out
        assert not no_final.exists()

        exec_evidence["stdout"].write_text(
            "Final estimate: PPL = 7.2500 +/- 0.10000\n"
            "Final estimate: PPL = 7.2600 +/- 0.11000\n",
            encoding="utf-8",
        )
        reseal(exec_evidence)
        ambiguous = td / "ambiguous.json"
        out = run(
            extract_args(exec_evidence, model, corpus, ambiguous),
            expect=2,
        )
        assert "ambiguous quality output" in out
        assert "QUALITY METRIC: BLOCKED" in out
        assert not ambiguous.exists()

    print("QUALITY METRIC SELFTEST: PASS")
    print("- one supported Final estimate line becomes a machine-readable PPL artifact")
    print("- metric verification reparses raw evidence instead of trusting copied numbers")
    print("- changed metric values are blocked")
    print("- chunk-only output is blocked rather than guessed")
    print("- multiple Final estimate lines are ambiguous and blocked")
    print("- all values are synthetic parser fixtures, not real model quality results")


if __name__ == "__main__":
    main()

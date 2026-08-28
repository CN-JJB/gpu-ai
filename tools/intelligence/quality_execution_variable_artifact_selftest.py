#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from quality_execution_variable_selftest import (
    capture,
    compare_args,
    fake_executable,
    identity,
    manifest,
    run,
    sha256_bytes,
    write,
)


HERE = Path(__file__).resolve().parent
PY = sys.executable


def verify_args(comparison, bm, cm, base, cand, model, corpus, contract):
    return [
        PY,
        str(HERE / "verify_quality_execution_variable_comparison.py"),
        "--quality-comparison",
        str(comparison),
        "--baseline-manifest",
        str(bm),
        "--candidate-manifest",
        str(cm),
        "--baseline-dir",
        str(base),
        "--candidate-dir",
        str(cand),
        "--baseline-model",
        str(model),
        "--candidate-model",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--variable-contract",
        str(contract),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"same-i39-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same-i39-corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        bm = manifest("baseline", "f16")
        cm = manifest("candidate", "q8_0")
        bm["comparison_id"] = "fixture-i39"
        cm["comparison_id"] = "fixture-i39"
        model_sha = sha256_bytes(model.read_bytes())
        model_bytes = model.stat().st_size
        for obj in (bm, cm):
            obj["variant"]["model"]["artifact_sha256"] = model_sha
            obj["variant"]["model"]["artifact_bytes"] = model_bytes
            obj["fixed"]["quality_eval"]["corpus_sha256"] = corpus_sha

        bm_path = td / "baseline-manifest.json"
        cm_path = td / "candidate-manifest.json"
        write(bm_path, bm)
        write(cm_path, cm)

        baseline_args = ["--fixture-kv-k", "f16"]
        candidate_args = ["--fixture-kv-k", "q8_0"]
        baseline_identity = td / "baseline-identity.json"
        candidate_identity = td / "candidate-identity.json"
        identity(baseline_identity, corpus, baseline_args)
        identity(candidate_identity, corpus, candidate_args)

        fake = td / "fake-quality"
        fake_executable(fake)

        base = td / "baseline-run"
        cand = td / "candidate-run"
        capture(base, fake, model, corpus, baseline_identity, baseline_args)
        capture(cand, fake, model, corpus, candidate_identity, candidate_args)

        contract = {
            "quality_variable_contract_schema_version": 1,
            "comparison_id": "fixture-i39",
            "intentional_variable": "variant.execution.kv_k",
            "baseline": {
                "manifest_value": "f16",
                "evaluation_args": baseline_args,
            },
            "candidate": {
                "manifest_value": "q8_0",
                "evaluation_args": candidate_args,
            },
        }
        contract_path = td / "quality-variable-contract.json"
        write(contract_path, contract)

        comparison = td / "comparison.json"
        out = run(
            compare_args(
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                contract_path,
                comparison,
            )
        )
        assert "QUALITY VARIABLE COMPARISON: PASS" in out

        obj = json.loads(comparison.read_text(encoding="utf-8"))
        assert obj["quality_comparison_schema_version"] == 2
        assert obj["comparison_contract"] == "ppl-declared-execution-variable-v2"
        assert obj["evidence"]["variable_contract_sha256"]

        out = run(
            verify_args(
                comparison,
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                contract_path,
            )
        )
        assert "QUALITY VARIABLE COMPARISON ARTIFACT: PASS" in out

        tampered = td / "tampered.json"
        bad = json.loads(comparison.read_text(encoding="utf-8"))
        bad["baseline"]["value"] = 19.6
        bad["candidate"]["value"] = 20.2
        bad["delta_candidate_minus_baseline"] = 0.6
        bad["ratio_candidate_to_baseline"] = 20.2 / 19.6
        bad["percent_change"] = ((20.2 / 19.6) - 1.0) * 100.0
        write(tampered, bad)

        out = run(
            verify_args(
                tampered,
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                contract_path,
            ),
            expect=2,
        )
        assert "does not exactly match independently rebuilt sealed evidence + variable contract" in out
        assert "QUALITY VARIABLE COMPARISON ARTIFACT: BLOCKED" in out

    print("QUALITY EXECUTION-VARIABLE ARTIFACT SELFTEST: PASS")
    print("- valid v2 comparison is independently reproducible")
    print("- coherent PPL/delta/ratio edits are blocked")
    print("- variable-contract and metric SHA roots are embedded in the comparison")
    print("- synthetic values remain provenance fixtures only")


if __name__ == "__main__":
    main()

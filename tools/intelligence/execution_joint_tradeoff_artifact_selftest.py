#!/usr/bin/env python3
import json
import sys
import tempfile
from pathlib import Path

from execution_joint_tradeoff_selftest import bind_args
from joint_tradeoff_selftest import benchmark
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


def verify_args(
    joint,
    bm,
    cm,
    bb,
    cb,
    comparison,
    base,
    cand,
    model,
    corpus,
    contract,
):
    return [
        PY,
        str(HERE / "verify_execution_joint_tradeoff.py"),
        "--joint-tradeoff",
        str(joint),
        "--baseline-manifest",
        str(bm),
        "--candidate-manifest",
        str(cm),
        "--baseline-benchmark",
        str(bb),
        "--candidate-benchmark",
        str(cb),
        "--quality-comparison",
        str(comparison),
        "--baseline-quality-dir",
        str(base),
        "--candidate-quality-dir",
        str(cand),
        "--baseline-model-artifact",
        str(model),
        "--candidate-model-artifact",
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
        model.write_bytes(b"same-i41-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same-i41-corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        bm = manifest("baseline", "f16")
        cm = manifest("candidate", "q8_0")
        bm["comparison_id"] = "fixture-i41"
        cm["comparison_id"] = "fixture-i41"

        model_sha = sha256_bytes(model.read_bytes())
        model_bytes = model.stat().st_size
        for obj in (bm, cm):
            obj["variant"]["model"]["artifact_sha256"] = model_sha
            obj["variant"]["model"]["artifact_bytes"] = model_bytes
            obj["fixed"]["quality_eval"]["corpus_sha256"] = corpus_sha

        bm_path = td / "baseline-manifest.json"
        cm_path = td / "candidate-manifest.json"
        bb_path = td / "baseline-benchmark.json"
        cb_path = td / "candidate-benchmark.json"
        write(bm_path, bm)
        write(cm_path, cm)
        write(bb_path, benchmark(bm, 1000.0, 50.0))
        write(cb_path, benchmark(cm, 1100.0, 52.5))

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
            "comparison_id": "fixture-i41",
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

        comparison = td / "quality-comparison.json"
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

        joint = td / "joint.json"
        out = run(
            bind_args(
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                comparison,
                base,
                cand,
                model,
                corpus,
                contract_path,
                joint,
            )
        )
        assert "EXECUTION JOINT TRADEOFF: PASS" in out

        out = run(
            verify_args(
                joint,
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                comparison,
                base,
                cand,
                model,
                corpus,
                contract_path,
            )
        )
        assert "EXECUTION JOINT TRADEOFF ARTIFACT: PASS" in out

        tampered = td / "tampered-joint.json"
        obj = json.loads(joint.read_text(encoding="utf-8"))
        obj["performance"]["pp_tok_s"] = {
            "baseline": 2000.0,
            "candidate": 2200.0,
            "delta_candidate_minus_baseline": 200.0,
            "ratio_candidate_to_baseline": 1.1,
            "percent_change": 10.0,
            "higher_is_better": True,
        }
        obj["performance"]["tg_tok_s"] = {
            "baseline": 100.0,
            "candidate": 105.0,
            "delta_candidate_minus_baseline": 5.0,
            "ratio_candidate_to_baseline": 1.05,
            "percent_change": 5.0,
            "higher_is_better": True,
        }
        obj["quality"].update(
            {
                "baseline": 19.6,
                "candidate": 20.2,
                "delta_candidate_minus_baseline": 0.6,
                "ratio_candidate_to_baseline": 20.2 / 19.6,
                "percent_change": ((20.2 / 19.6) - 1.0) * 100.0,
            }
        )
        write(tampered, obj)

        out = run(
            verify_args(
                tampered,
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                comparison,
                base,
                cand,
                model,
                corpus,
                contract_path,
            ),
            expect=2,
        )
        assert "does not exactly match independently rebuilt performance + quality evidence" in out
        assert "EXECUTION JOINT TRADEOFF ARTIFACT: BLOCKED" in out

    print("EXECUTION JOINT TRADEOFF ARTIFACT SELFTEST: PASS")
    print("- valid execution-variable joint evidence is independently reproducible")
    print("- coherently edited PP/TG/PPL arithmetic is blocked")
    print("- rebuild roots include manifests, benchmarks, I39 quality evidence and variable contract")
    print("- synthetic values remain provenance fixtures only")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

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


def bind_args(
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
    out,
):
    return [
        PY,
        str(HERE / "bind_execution_performance_quality_ab.py"),
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
        "--out",
        str(out),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"same-i40-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same-i40-corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        bm = manifest("baseline", "f16")
        cm = manifest("candidate", "q8_0")
        bm["comparison_id"] = "fixture-i40"
        cm["comparison_id"] = "fixture-i40"

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
            "comparison_id": "fixture-i40",
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
        assert "INDEPENDENTLY-REPRODUCED-I39" in out

        obj = json.loads(joint.read_text(encoding="utf-8"))
        assert obj["joint_tradeoff_schema_version"] == 1
        assert (
            obj["tradeoff_contract"]
            == "experiment61-execution-performance-quality-v1"
        )
        assert obj["intentional_variable"] == "variant.execution.kv_k"
        assert abs(
            obj["performance"]["pp_tok_s"]["percent_change"] - 10.0
        ) < 1e-9
        assert abs(
            obj["performance"]["tg_tok_s"]["percent_change"] - 5.0
        ) < 1e-9
        assert obj["quality_evidence"]["verification"] == "INDEPENDENTLY-REPRODUCED-I39"

        tampered = td / "tampered-quality.json"
        bad_quality = json.loads(comparison.read_text(encoding="utf-8"))
        bad_quality["baseline"]["value"] = 19.6
        bad_quality["candidate"]["value"] = 20.2
        bad_quality["delta_candidate_minus_baseline"] = 0.6
        bad_quality["ratio_candidate_to_baseline"] = 20.2 / 19.6
        bad_quality["percent_change"] = ((20.2 / 19.6) - 1.0) * 100.0
        write(tampered, bad_quality)

        blocked = td / "blocked-quality.json"
        out = run(
            bind_args(
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                tampered,
                base,
                cand,
                model,
                corpus,
                contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "quality comparison evidence:" in out
        assert "does not exactly match independently rebuilt sealed evidence + variable contract" in out
        assert "EXECUTION JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

        bad_bench = benchmark(cm, 1100.0, 52.5)
        bad_bench["workload"]["context"] = 4096
        bad_bench_path = td / "bad-benchmark.json"
        write(bad_bench_path, bad_bench)

        blocked = td / "blocked-workload.json"
        out = run(
            bind_args(
                bm_path,
                cm_path,
                bb_path,
                bad_bench_path,
                comparison,
                base,
                cand,
                model,
                corpus,
                contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "candidate workload.context mismatch" in out
        assert "EXECUTION JOINT TRADEOFF: BLOCKED" in out

        bad_manifest = copy.deepcopy(cm)
        bad_manifest["variant"]["execution"]["context"] = 4096
        bad_manifest_path = td / "bad-manifest.json"
        write(bad_manifest_path, bad_manifest)

        blocked = td / "blocked-manifest.json"
        out = run(
            bind_args(
                bm_path,
                bad_manifest_path,
                bb_path,
                cb_path,
                comparison,
                base,
                cand,
                model,
                corpus,
                contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "manifest contract: undeclared differences" in out
        assert "EXECUTION JOINT TRADEOFF: BLOCKED" in out

    print("EXECUTION JOINT TRADEOFF SELFTEST: PASS")
    print("- I39-verified execution-variable PPL binds to matching Experiment 61 PP/TG")
    print("- coherently edited quality comparison is blocked")
    print("- benchmark workload drift is blocked")
    print("- undeclared manifest drift is blocked")
    print("- synthetic values remain descriptive provenance fixtures only")


if __name__ == "__main__":
    main()

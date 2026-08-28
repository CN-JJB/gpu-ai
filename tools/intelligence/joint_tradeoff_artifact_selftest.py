#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from joint_tradeoff_selftest import (
    benchmark,
    bind_args,
    capture_quality,
    make_quality_comparison,
    manifest,
    run,
    sha256_bytes,
    write,
    write_fake,
    write_identity,
)


HERE = Path(__file__).resolve().parent
PY = sys.executable


def verify_args(
    joint,
    bm,
    cm,
    bb,
    cb,
    qc,
    base_q,
    cand_q,
    baseline_model,
    candidate_model,
    corpus,
):
    return [
        PY,
        str(HERE / "verify_joint_tradeoff.py"),
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
        str(qc),
        "--baseline-quality-dir",
        str(base_q),
        "--candidate-quality-dir",
        str(cand_q),
        "--baseline-model-artifact",
        str(baseline_model),
        "--candidate-model-artifact",
        str(candidate_model),
        "--quality-corpus",
        str(corpus),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same i38 corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        baseline_model = td / "baseline.gguf"
        baseline_model.write_bytes(b"baseline-i38-model\n")
        candidate_model = td / "candidate.gguf"
        candidate_model.write_bytes(b"candidate-i38-model\n")

        bm = manifest(
            "baseline",
            sha256_bytes(baseline_model.read_bytes()),
            baseline_model.stat().st_size,
            "Q8_0",
            corpus_sha,
        )
        cm = manifest(
            "candidate",
            sha256_bytes(candidate_model.read_bytes()),
            candidate_model.stat().st_size,
            "Q4_K_M",
            corpus_sha,
        )
        bm["comparison_id"] = "fixture-i38"
        cm["comparison_id"] = "fixture-i38"

        bm_path = td / "baseline-manifest.json"
        cm_path = td / "candidate-manifest.json"
        bb_path = td / "baseline-benchmark.json"
        cb_path = td / "candidate-benchmark.json"
        write(bm_path, bm)
        write(cm_path, cm)
        write(bb_path, benchmark(bm, 1000.0, 50.0))
        write(cb_path, benchmark(cm, 1200.0, 60.0))

        baseline_identity = td / "baseline-identity.json"
        candidate_identity = td / "candidate-identity.json"
        write_identity(baseline_identity, corpus_sha)
        write_identity(candidate_identity, corpus_sha)

        fake = td / "fake-quality"
        write_fake(fake)

        base_q = td / "baseline-quality"
        cand_q = td / "candidate-quality"
        capture_quality(base_q, fake, baseline_model, corpus, baseline_identity)
        capture_quality(cand_q, fake, candidate_model, corpus, candidate_identity)

        qc_path = td / "quality-comparison.json"
        make_quality_comparison(
            base_q,
            cand_q,
            baseline_model,
            candidate_model,
            corpus,
            qc_path,
        )

        joint = td / "joint.json"
        out = run(
            bind_args(
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                qc_path,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
                joint,
            )
        )
        assert "JOINT TRADEOFF: PASS" in out

        out = run(
            verify_args(
                joint,
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                qc_path,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
            )
        )
        assert "JOINT TRADEOFF ARTIFACT: PASS" in out

        tampered = td / "tampered-joint.json"
        obj = json.loads(joint.read_text(encoding="utf-8"))

        obj["performance"]["pp_tok_s"] = {
            "baseline": 2000.0,
            "candidate": 2400.0,
            "delta_candidate_minus_baseline": 400.0,
            "ratio_candidate_to_baseline": 1.2,
            "percent_change": 20.0,
            "higher_is_better": True,
        }
        obj["performance"]["tg_tok_s"] = {
            "baseline": 100.0,
            "candidate": 120.0,
            "delta_candidate_minus_baseline": 20.0,
            "ratio_candidate_to_baseline": 1.2,
            "percent_change": 20.0,
            "higher_is_better": True,
        }
        obj["quality"].update(
            {
                "baseline": 20.0,
                "candidate": 21.0,
                "delta_candidate_minus_baseline": 1.0,
                "ratio_candidate_to_baseline": 1.05,
                "percent_change": 5.0,
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
                qc_path,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
            ),
            expect=2,
        )
        assert "does not exactly match independently rebuilt performance + quality evidence" in out
        assert "JOINT TRADEOFF ARTIFACT: BLOCKED" in out

    print("JOINT TRADEOFF ARTIFACT SELFTEST: PASS")
    print("- valid schema-v2 joint evidence is independently reproducible")
    print("- coherently edited PP/TG and PPL arithmetic is still blocked")
    print("- the verifier rebuilds from manifests, benchmark records and sealed quality roots")
    print("- synthetic values remain provenance fixtures only")


if __name__ == "__main__":
    main()

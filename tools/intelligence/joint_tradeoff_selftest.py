#!/usr/bin/env python3
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


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


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write(path, obj):
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def manifest(label, model_sha, model_bytes, quant, corpus_sha):
    return {
        "schema_version": 1,
        "comparison_id": "fixture-i37",
        "label": label,
        "intentional_variable": "variant.model",
        "fixed": {
            "protocol": {
                "pp_tokens": 512,
                "tg_tokens": 128,
                "repetitions": 5,
                "warmup_runs": 1,
            },
            "quality_eval": {
                "tokenizer_identity": "fixture-tokenizer-i37",
                "corpus_sha256": corpus_sha,
                "fixture_revision": "fixture-i37",
                "evaluation_args": ["--fixture-mode", "strict"],
            },
        },
        "variant": {
            "hardware": {
                "device_identity": "Synthetic I37 GPU",
                "profile_sha256": "d" * 64,
            },
            "runtime": {
                "runtime_identity": "llama.cpp fixture-i37",
                "backend": "FIXTURE",
                "build_identity": "fixture-build-i37",
            },
            "model": {
                "artifact_sha256": model_sha,
                "artifact_bytes": model_bytes,
                "quant": quant,
                "source_revision": "fixture-source",
            },
            "execution": {
                "context": 8192,
                "sequences": 1,
                "gpu_layers": "all",
                "flash_attention": True,
                "kv_k": "f16",
                "kv_v": "f16",
                "split_mode": "none",
                "tensor_split": "",
                "threads": "8",
            },
            "prompt": {
                "messages_sha256": "e" * 64,
                "chat_template_sha256": "f" * 64,
                "rendered_sha256": "1" * 64,
                "token_ids_sha256": "2" * 64,
                "token_count": 512,
            },
            "sampler": {
                "mode": "not-applicable-model-eval",
                "temperature": None,
                "top_k": None,
                "top_p": None,
                "min_p": None,
                "seed": None,
                "chain": [],
            },
        },
        "audit": {
            "command_record": "synthetic",
            "raw_result": "synthetic",
            "telemetry": "synthetic",
            "quality_log": "synthetic",
            "notes": "I37 synthetic selftest",
        },
    }


def benchmark(manifest_obj, pp, tg):
    variant = manifest_obj["variant"]
    fixed = manifest_obj["fixed"]
    model = variant["model"]
    runtime = variant["runtime"]
    hardware = variant["hardware"]
    execution = variant["execution"]
    protocol = fixed["protocol"]
    prompt = variant["prompt"]

    return {
        "schema_version": 1,
        "record_type": "benchmark",
        "record_id": "synthetic-" + manifest_obj["label"],
        "hardware_id": "hw:fixture:i37",
        "model_id": "model:fixture:i37",
        "runtime_id": "runtime:fixture:i37",
        "observed_at": "2026-08-28",
        "artifact": {
            "sha256": model["artifact_sha256"],
            "bytes": model["artifact_bytes"],
            "quant": model["quant"],
            "source_revision": model["source_revision"],
        },
        "runtime": {
            "name": "llama.cpp",
            "runtime_identity": runtime["runtime_identity"],
            "backend": runtime["backend"],
            "build_identity": runtime["build_identity"],
        },
        "hardware_evidence": {
            "device_identity": hardware["device_identity"],
            "profile_sha256": hardware["profile_sha256"],
        },
        "workload": {
            "pp_tokens": protocol["pp_tokens"],
            "tg_tokens": protocol["tg_tokens"],
            "repetitions": protocol["repetitions"],
            "warmup_runs": protocol["warmup_runs"],
            "context": execution["context"],
            "sequences": execution["sequences"],
            "gpu_layers": execution["gpu_layers"],
            "flash_attention": execution["flash_attention"],
            "kv_k": execution["kv_k"],
            "kv_v": execution["kv_v"],
            "split_mode": execution["split_mode"],
            "tensor_split": execution["tensor_split"],
            "threads": execution["threads"],
            "prompt_token_ids_sha256": prompt["token_ids_sha256"],
        },
        "metrics": {"pp_tok_s": pp, "tg_tok_s": tg},
        "synthetic": True,
    }


def write_identity(path, corpus_sha):
    write(
        path,
        {
            "quality_identity_schema_version": 2,
            "tokenizer_identity": "fixture-tokenizer-i37",
            "corpus_sha256": corpus_sha,
            "fixture_revision": "fixture-i37",
            "evaluation_args": ["--fixture-mode", "strict"],
        },
    )


def write_fake(path):
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import argparse\n"
        "from pathlib import Path\n"
        "p = argparse.ArgumentParser()\n"
        "p.add_argument('-m', '--model', required=True)\n"
        "p.add_argument('-f', '--file', required=True)\n"
        "p.add_argument('--fixture-mode', required=True)\n"
        "a = p.parse_args()\n"
        "data = Path(a.model).read_bytes()\n"
        "ppl = 10.0 if data.startswith(b'baseline') else 10.5\n"
        "print('Final estimate: PPL = %.4f +/- 0.10000' % ppl)\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def capture_quality(root, fake, model, corpus, identity):
    out = run(
        [
            PY,
            str(HERE / "capture_quality_eval.py"),
            "--out-dir",
            str(root),
            "--model-artifact",
            str(model),
            "--quality-corpus",
            str(corpus),
            "--quality-manifest",
            str(identity),
            "--",
            str(fake),
            "-m",
            str(model),
            "-f",
            str(corpus),
            "--fixture-mode",
            "strict",
        ]
    )
    assert "QUALITY CAPTURE: SEALED" in out

    out = run(
        [
            PY,
            str(HERE / "extract_quality_metric.py"),
            "--quality-command-record",
            str(root / "quality-command.json"),
            "--stdout",
            str(root / "stdout.txt"),
            "--stderr",
            str(root / "stderr.txt"),
            "--packet",
            str(root / "PACKET.json"),
            "--model-artifact",
            str(model),
            "--quality-corpus",
            str(corpus),
            "--quality-manifest",
            str(root / "quality-identity.json"),
            "--out",
            str(root / "quality-metric.json"),
        ]
    )
    assert "QUALITY METRIC: EXTRACTED" in out


def make_quality_comparison(base, cand, bm, cm, corpus, out):
    result = run(
        [
            PY,
            str(HERE / "compare_quality_metrics.py"),
            "--baseline-dir",
            str(base),
            "--candidate-dir",
            str(cand),
            "--baseline-model",
            str(bm),
            "--candidate-model",
            str(cm),
            "--quality-corpus",
            str(corpus),
            "--out",
            str(out),
        ]
    )
    assert "QUALITY COMPARISON: PASS" in result


def bind_args(
    base_m,
    cand_m,
    base_b,
    cand_b,
    quality,
    base_q,
    cand_q,
    base_model,
    cand_model,
    corpus,
    out,
):
    return [
        PY,
        str(HERE / "bind_performance_quality_ab.py"),
        "--baseline-manifest",
        str(base_m),
        "--candidate-manifest",
        str(cand_m),
        "--baseline-benchmark",
        str(base_b),
        "--candidate-benchmark",
        str(cand_b),
        "--quality-comparison",
        str(quality),
        "--baseline-quality-dir",
        str(base_q),
        "--candidate-quality-dir",
        str(cand_q),
        "--baseline-model-artifact",
        str(base_model),
        "--candidate-model-artifact",
        str(cand_model),
        "--quality-corpus",
        str(corpus),
        "--out",
        str(out),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same i37 corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        baseline_model = td / "baseline.gguf"
        baseline_model.write_bytes(b"baseline-i37-model\n")
        candidate_model = td / "candidate.gguf"
        candidate_model.write_bytes(b"candidate-i37-model\n")

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

        output = td / "joint.json"
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
                output,
            )
        )
        assert "JOINT TRADEOFF: PASS" in out
        assert "quality_comparison_verification=INDEPENDENTLY-REPRODUCED-I36" in out

        obj = json.loads(output.read_text(encoding="utf-8"))
        assert obj["joint_tradeoff_schema_version"] == 2
        assert obj["comparison_id"] == "fixture-i37"
        assert obj["tradeoff_contract"] == "experiment61-model-performance-quality-v2"
        assert abs(obj["performance"]["pp_tok_s"]["percent_change"] - 20.0) < 1e-9
        assert abs(obj["performance"]["tg_tok_s"]["percent_change"] - 20.0) < 1e-9
        assert abs(obj["quality"]["percent_change"] - 5.0) < 1e-9
        assert obj["quality_evidence"]["verification"] == "INDEPENDENTLY-REPRODUCED-I36"

        tampered = td / "tampered-quality.json"
        bad = json.loads(qc_path.read_text(encoding="utf-8"))
        bad["baseline"]["value"] = 20.0
        bad["candidate"]["value"] = 21.0
        bad["delta_candidate_minus_baseline"] = 1.0
        bad["ratio_candidate_to_baseline"] = 1.05
        bad["percent_change"] = 5.0
        write(tampered, bad)

        blocked = td / "blocked-tampered-quality.json"
        out = run(
            bind_args(
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                tampered,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
                blocked,
            ),
            expect=2,
        )
        assert "quality comparison evidence:" in out
        assert "does not exactly match independently recomputed quality bundles" in out
        assert "JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

        bad_bench = benchmark(cm, 1200.0, 60.0)
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
                qc_path,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
                blocked,
            ),
            expect=2,
        )
        assert "candidate workload.context mismatch" in out
        assert "JOINT TRADEOFF: BLOCKED" in out

        bad_manifest = copy.deepcopy(cm)
        bad_manifest["variant"]["execution"]["context"] = 4096
        bad_manifest_path = td / "bad-manifest.json"
        write(bad_manifest_path, bad_manifest)
        blocked = td / "blocked-contract.json"
        out = run(
            bind_args(
                bm_path,
                bad_manifest_path,
                bb_path,
                cb_path,
                qc_path,
                base_q,
                cand_q,
                baseline_model,
                candidate_model,
                corpus,
                blocked,
            ),
            expect=2,
        )
        assert "manifest contract: undeclared differences" in out
        assert "JOINT TRADEOFF: BLOCKED" in out

        execution_bm = copy.deepcopy(bm)
        execution_cm = copy.deepcopy(bm)
        execution_bm["label"] = "baseline"
        execution_cm["label"] = "candidate"
        execution_bm["intentional_variable"] = "variant.execution.flash_attention"
        execution_cm["intentional_variable"] = "variant.execution.flash_attention"
        execution_cm["variant"]["execution"]["flash_attention"] = False

        ebm_path = td / "execution-baseline.json"
        ecm_path = td / "execution-candidate.json"
        ebb_path = td / "execution-baseline-benchmark.json"
        ecb_path = td / "execution-candidate-benchmark.json"
        write(ebm_path, execution_bm)
        write(ecm_path, execution_cm)
        write(ebb_path, benchmark(execution_bm, 1000.0, 50.0))
        write(ecb_path, benchmark(execution_cm, 1100.0, 55.0))

        same_model_qc = td / "same-model-quality-comparison.json"
        make_quality_comparison(
            base_q,
            base_q,
            baseline_model,
            baseline_model,
            corpus,
            same_model_qc,
        )

        blocked = td / "blocked-scope.json"
        out = run(
            bind_args(
                ebm_path,
                ecm_path,
                ebb_path,
                ecb_path,
                same_model_qc,
                base_q,
                base_q,
                baseline_model,
                baseline_model,
                corpus,
                blocked,
            ),
            expect=2,
        )
        assert "I33 quality comparison currently binds only model-artifact A/B" in out
        assert "JOINT TRADEOFF: BLOCKED" in out

    print("JOINT TRADEOFF SELFTEST: PASS")
    print("- valid model-artifact A/B binds PP/TG to independently reproduced I33 PPL evidence")
    print("- coherently edited quality-comparison.json is blocked")
    print("- benchmark workload mismatch is blocked")
    print("- undeclared manifest differences are blocked")
    print("- execution-variable quality attribution remains blocked on the I33 path")
    print("- synthetic arithmetic is not real performance, quality, or recommendation evidence")


if __name__ == "__main__":
    main()

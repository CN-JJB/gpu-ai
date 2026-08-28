#!/usr/bin/env python3
import copy
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


def write(path, obj):
    path.write_text(
        json.dumps(obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def manifest(label, model_sha, model_bytes, quant):
    return {
        "schema_version": 1,
        "comparison_id": "fixture-i34",
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
                "tokenizer_identity": "fixture-tokenizer-i34",
                "corpus_sha256": "c" * 64,
                "fixture_revision": "fixture-i34",
                "evaluation_args": ["--fixture-mode", "strict"],
            },
        },
        "variant": {
            "hardware": {
                "device_identity": "Synthetic I34 GPU",
                "profile_sha256": "d" * 64,
            },
            "runtime": {
                "runtime_identity": "llama.cpp fixture-i34",
                "backend": "FIXTURE",
                "build_identity": "fixture-build-i34",
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
            "notes": "I34 synthetic selftest",
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
        "hardware_id": "hw:fixture:i34",
        "model_id": "model:fixture:i34",
        "runtime_id": "runtime:fixture:i34",
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
        "metrics": {
            "pp_tok_s": pp,
            "tg_tok_s": tg,
        },
        "synthetic": True,
    }


def quality_comparison(base_manifest, cand_manifest):
    fixed = base_manifest["fixed"]["quality_eval"]
    bppl = 10.0
    cppl = 10.5
    ratio = cppl / bppl
    return {
        "quality_comparison_schema_version": 1,
        "comparison_contract": "ppl-exact-quality-identity-v1",
        "metric": "PPL",
        "lower_is_better": True,
        "baseline": {
            "value": bppl,
            "reported_uncertainty": 0.1,
            "model_sha256": base_manifest["variant"]["model"]["artifact_sha256"],
            "model_bytes": base_manifest["variant"]["model"]["artifact_bytes"],
            "metric_sha256": "3" * 64,
        },
        "candidate": {
            "value": cppl,
            "reported_uncertainty": 0.1,
            "model_sha256": cand_manifest["variant"]["model"]["artifact_sha256"],
            "model_bytes": cand_manifest["variant"]["model"]["artifact_bytes"],
            "metric_sha256": "4" * 64,
        },
        "delta_candidate_minus_baseline": cppl - bppl,
        "ratio_candidate_to_baseline": ratio,
        "percent_change": (ratio - 1.0) * 100.0,
        "fixed_quality_identity": copy.deepcopy(fixed),
        "quality_executable": {
            "sha256": "5" * 64,
            "bytes": 123456,
        },
    }


def args(base_m, cand_m, base_b, cand_b, quality, out):
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
        "--out",
        str(out),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        bm = manifest("baseline", "a" * 64, 1000, "Q8_0")
        cm = manifest("candidate", "b" * 64, 800, "Q4_K_M")
        bb = benchmark(bm, 1000.0, 50.0)
        cb = benchmark(cm, 1200.0, 60.0)
        qc = quality_comparison(bm, cm)

        bm_path = td / "baseline-manifest.json"
        cm_path = td / "candidate-manifest.json"
        bb_path = td / "baseline-benchmark.json"
        cb_path = td / "candidate-benchmark.json"
        qc_path = td / "quality-comparison.json"
        for path, obj in (
            (bm_path, bm),
            (cm_path, cm),
            (bb_path, bb),
            (cb_path, cb),
            (qc_path, qc),
        ):
            write(path, obj)

        output = td / "joint.json"
        out = run(args(bm_path, cm_path, bb_path, cb_path, qc_path, output))
        assert "JOINT TRADEOFF: PASS" in out

        obj = json.loads(output.read_text(encoding="utf-8"))
        assert obj["comparison_id"] == "fixture-i34"
        assert obj["intentional_variable"] == "variant.model"
        assert abs(obj["performance"]["pp_tok_s"]["percent_change"] - 20.0) < 1e-9
        assert abs(obj["performance"]["tg_tok_s"]["percent_change"] - 20.0) < 1e-9
        assert abs(obj["quality"]["percent_change"] - 5.0) < 1e-9

        bad_quality = copy.deepcopy(qc)
        bad_quality["candidate"]["model_sha256"] = "9" * 64
        bad_quality_path = td / "bad-quality.json"
        write(bad_quality_path, bad_quality)
        blocked = td / "blocked-model.json"
        out = run(
            args(
                bm_path,
                cm_path,
                bb_path,
                cb_path,
                bad_quality_path,
                blocked,
            ),
            expect=2,
        )
        assert "quality candidate model_sha256 mismatch" in out
        assert "JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

        bad_bench = copy.deepcopy(cb)
        bad_bench["workload"]["context"] = 4096
        bad_bench_path = td / "bad-benchmark.json"
        write(bad_bench_path, bad_bench)
        blocked = td / "blocked-workload.json"
        out = run(
            args(
                bm_path,
                cm_path,
                bb_path,
                bad_bench_path,
                qc_path,
                blocked,
            ),
            expect=2,
        )
        assert "candidate workload.context mismatch" in out
        assert "JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

        bad_manifest = copy.deepcopy(cm)
        bad_manifest["variant"]["execution"]["context"] = 4096
        bad_manifest_path = td / "bad-manifest.json"
        write(bad_manifest_path, bad_manifest)
        blocked = td / "blocked-contract.json"
        out = run(
            args(
                bm_path,
                bad_manifest_path,
                bb_path,
                cb_path,
                qc_path,
                blocked,
            ),
            expect=2,
        )
        assert "manifest contract: undeclared differences" in out
        assert "JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

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
        eqc_path = td / "execution-quality.json"
        write(ebm_path, execution_bm)
        write(ecm_path, execution_cm)
        write(ebb_path, benchmark(execution_bm, 1000.0, 50.0))
        write(ecb_path, benchmark(execution_cm, 1100.0, 55.0))
        write(eqc_path, quality_comparison(execution_bm, execution_cm))

        blocked = td / "blocked-scope.json"
        out = run(
            args(
                ebm_path,
                ecm_path,
                ebb_path,
                ecb_path,
                eqc_path,
                blocked,
            ),
            expect=2,
        )
        assert "I33 quality comparison currently binds only model-artifact A/B" in out
        assert "JOINT TRADEOFF: BLOCKED" in out
        assert not blocked.exists()

    print("JOINT TRADEOFF SELFTEST: PASS")
    print("- valid model-artifact Experiment 61 A/B binds PP/TG and PPL evidence")
    print("- quality model SHA mismatch is blocked")
    print("- benchmark workload mismatch is blocked")
    print("- undeclared manifest differences are blocked")
    print("- execution-variable quality attribution is blocked by current I33 scope")
    print("- synthetic arithmetic is not real performance, quality, or recommendation evidence")


if __name__ == "__main__":
    main()

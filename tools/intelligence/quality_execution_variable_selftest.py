#!/usr/bin/env python3
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


def manifest(label, kv_k):
    return {
        "schema_version": 1,
        "comparison_id": "fixture-i35",
        "label": label,
        "intentional_variable": "variant.execution.kv_k",
        "fixed": {
            "protocol": {
                "pp_tokens": 512,
                "tg_tokens": 128,
                "repetitions": 5,
                "warmup_runs": 1,
            },
            "quality_eval": {
                "tokenizer_identity": "fixture-tokenizer-i35",
                "corpus_sha256": "c" * 64,
                "fixture_revision": "fixture-i35",
                "evaluation_args": [],
            },
        },
        "variant": {
            "hardware": {
                "device_identity": "Synthetic I35 GPU",
                "profile_sha256": "d" * 64,
            },
            "runtime": {
                "runtime_identity": "llama.cpp fixture-i35",
                "backend": "FIXTURE",
                "build_identity": "fixture-build-i35",
            },
            "model": {
                "artifact_sha256": "a" * 64,
                "artifact_bytes": 1000,
                "quant": "Q4_K_M",
                "source_revision": "fixture-source",
            },
            "execution": {
                "context": 8192,
                "sequences": 1,
                "gpu_layers": "all",
                "flash_attention": True,
                "kv_k": kv_k,
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
            "notes": "I35 synthetic selftest",
        },
    }


def identity(path, corpus, args):
    write(
        path,
        {
            "quality_identity_schema_version": 2,
            "tokenizer_identity": "fixture-tokenizer-i35",
            "corpus_sha256": sha256_bytes(corpus.read_bytes()),
            "fixture_revision": "fixture-i35",
            "evaluation_args": args,
        },
    )


def fake_executable(path):
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import argparse\n"
        "p = argparse.ArgumentParser()\n"
        "p.add_argument('-m', '--model', required=True)\n"
        "p.add_argument('-f', '--file', required=True)\n"
        "p.add_argument('--fixture-kv-k', required=True)\n"
        "a = p.parse_args()\n"
        "ppl = 9.8 if a.fixture_kv_k == 'f16' else 10.1\n"
        "print('Final estimate: PPL = %.4f +/- 0.10000' % ppl)\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def capture(root, fake, model, corpus, identity_path, args):
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
            str(identity_path),
            "--",
            str(fake),
            "-m",
            str(model),
            "-f",
            str(corpus),
            *args,
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


def compare_args(bm, cm, base, cand, model, corpus, contract, out):
    return [
        PY,
        str(HERE / "compare_quality_execution_variable.py"),
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
        "--out",
        str(out),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"same-i35-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"same-i35-corpus\n")
        corpus_sha = sha256_bytes(corpus.read_bytes())

        bm = manifest("baseline", "f16")
        cm = manifest("candidate", "q8_0")
        model_sha = sha256_bytes(model.read_bytes())
        model_bytes = model.stat().st_size
        for manifest_obj in (bm, cm):
            manifest_obj["variant"]["model"]["artifact_sha256"] = model_sha
            manifest_obj["variant"]["model"]["artifact_bytes"] = model_bytes
            manifest_obj["fixed"]["quality_eval"]["corpus_sha256"] = corpus_sha

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
            "comparison_id": "fixture-i35",
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

        output = td / "comparison.json"
        out = run(
            compare_args(
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                contract_path,
                output,
            )
        )
        assert "QUALITY VARIABLE COMPARISON: PASS" in out
        obj = json.loads(output.read_text(encoding="utf-8"))
        assert obj["comparison_contract"] == "ppl-declared-execution-variable-v1"
        assert obj["intentional_variable"] == "variant.execution.kv_k"
        assert obj["declared_variable"]["baseline_value"] == "f16"
        assert obj["declared_variable"]["candidate_value"] == "q8_0"

        bad_contract = dict(contract)
        bad_contract["candidate"] = {
            "manifest_value": "f16",
            "evaluation_args": candidate_args,
        }
        bad_contract_path = td / "bad-contract.json"
        write(bad_contract_path, bad_contract)
        blocked = td / "blocked-contract.json"
        out = run(
            compare_args(
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                bad_contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "candidate manifest_value does not match candidate manifest" in out
        assert "QUALITY VARIABLE COMPARISON: BLOCKED" in out
        assert not blocked.exists()

        same_contract = dict(contract)
        same_contract["candidate"] = {
            "manifest_value": "q8_0",
            "evaluation_args": baseline_args,
        }
        same_contract_path = td / "same-args-contract.json"
        write(same_contract_path, same_contract)
        blocked = td / "blocked-same-args.json"
        out = run(
            compare_args(
                bm_path,
                cm_path,
                base,
                cand,
                model,
                corpus,
                same_contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "baseline/candidate evaluation_args to differ" in out
        assert "candidate quality identity evaluation_args do not match" in out
        assert "QUALITY VARIABLE COMPARISON: BLOCKED" in out

        bad_manifest = json.loads(cm_path.read_text(encoding="utf-8"))
        bad_manifest["variant"]["execution"]["context"] = 4096
        bad_manifest_path = td / "bad-manifest.json"
        write(bad_manifest_path, bad_manifest)
        blocked = td / "blocked-manifest.json"
        out = run(
            compare_args(
                bm_path,
                bad_manifest_path,
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
        assert "QUALITY VARIABLE COMPARISON: BLOCKED" in out

        fake2 = td / "fake-quality-2"
        fake2.write_bytes(fake.read_bytes() + b"\n# different executable\n")
        fake2.chmod(0o755)
        cand2 = td / "candidate-different-executable"
        capture(cand2, fake2, model, corpus, candidate_identity, candidate_args)
        blocked = td / "blocked-executable.json"
        out = run(
            compare_args(
                bm_path,
                cm_path,
                base,
                cand2,
                model,
                corpus,
                contract_path,
                blocked,
            ),
            expect=2,
        )
        assert "quality executable SHA256 differs" in out
        assert "QUALITY VARIABLE COMPARISON: BLOCKED" in out

    print("QUALITY EXECUTION-VARIABLE SELFTEST: PASS")
    print("- explicit manifest-value ↔ evaluation-argv contract enables execution-variable PPL A/B")
    print("- wrong manifest value mapping is blocked")
    print("- unchanged evaluation argv is blocked for a declared execution variable")
    print("- undeclared Experiment 61 manifest drift is blocked")
    print("- changed quality executable is blocked")
    print("- argv semantics remain declared evidence, not independently proven upstream semantics")


if __name__ == "__main__":
    main()

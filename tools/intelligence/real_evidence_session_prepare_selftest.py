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


def sha(data):
    return hashlib.sha256(data).hexdigest()


def copy_catalog(src, dst):
    dst.mkdir()
    for name in ("hardware.jsonl", "models.jsonl", "runtimes.jsonl"):
        (dst / name).write_bytes((src / name).read_bytes())


def main():
    fixture_catalog = HERE / "fixtures" / "catalog"
    exp = HERE / "fixtures" / "experiment61"

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        catalog = td / "catalog"
        copy_catalog(fixture_catalog, catalog)

        model = td / "model.gguf"
        model.write_bytes(b"synthetic-i53-model-bytes\n")
        profile = td / "profile.txt"
        profile.write_bytes(b"synthetic-i53-profile\n")
        corpus = td / "quality-corpus.txt"
        corpus.write_bytes((exp / "quality-corpus.txt").read_bytes())
        prompt = td / "prompt-manifest.json"
        prompt.write_bytes((exp / "prompt-manifest.json").read_bytes())

        quality_identity = td / "quality-identity.json"
        quality_identity.write_text(
            json.dumps(
                {
                    "quality_identity_schema_version": 2,
                    "tokenizer_identity": "fixture-tokenizer",
                    "corpus_sha256": "REPLACE",
                    "fixture_revision": "fixture",
                    "evaluation_args": ["--fixture-mode", "strict"],
                },
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )

        manifest_obj = json.loads(
            (exp / "manifest.json").read_text(encoding="utf-8")
        )
        manifest_obj["comparison_id"] = "i53-fixture"
        manifest_obj["intentional_variable"] = "variant.execution.flash_attention"
        manifest_obj["variant"]["hardware"]["profile_sha256"] = "REPLACE"
        manifest_obj["variant"]["model"]["artifact_sha256"] = "REPLACE"
        manifest_obj["variant"]["model"]["artifact_bytes"] = 0
        manifest_obj["fixed"]["quality_eval"] = {
            "tokenizer_identity": "REPLACE",
            "corpus_sha256": "REPLACE",
            "fixture_revision": "REPLACE",
            "evaluation_args": [],
        }
        manifest_obj["variant"]["prompt"] = {
            "messages_sha256": "REPLACE",
            "chat_template_sha256": "REPLACE",
            "rendered_sha256": "REPLACE",
            "token_ids_sha256": "REPLACE",
            "token_count": 0,
        }
        manifest = td / "manifest.json"
        manifest.write_text(
            json.dumps(manifest_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        source_manifest_bytes = manifest.read_bytes()
        source_identity_bytes = quality_identity.read_bytes()

        session = {
            "real_evidence_session_schema_version": 1,
            "working_directory": str(td),
            "catalog": str(catalog),
            "manifest": str(manifest),
            "model_artifact": str(model),
            "hardware_profile": str(profile),
            "prompt_manifest": str(prompt),
            "quality_corpus": str(corpus),
            "quality_identity": str(quality_identity),
            "hardware_id": "hw:fixture:24g",
            "model_id": "model:fixture:8b",
            "runtime_id": "runtime:fixture",
            "observed_at": "2026-08-28",
            "benchmark_argv": [
                "llama-bench",
                "-m",
                str(model),
                "-p",
                "512",
                "-n",
                "128",
                "-r",
                "5",
                "-o",
                "json",
            ],
            "quality_argv": [
                "llama-perplexity",
                "-m",
                str(model),
                "-f",
                str(corpus),
                "--fixture-mode",
                "strict",
            ],
        }
        session_path = td / "session.json"
        session_path.write_text(
            json.dumps(session, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        out_dir = td / "prepared"
        out = run(
            [
                PY,
                str(HERE / "prepare_real_evidence_session.py"),
                str(session_path),
                "--out-dir",
                str(out_dir),
                "--allow-synthetic",
            ]
        )
        assert "REAL SESSION PREPARE: READY-TO-RUN-I52" in out

        prepared_manifest = json.loads(
            (out_dir / "manifest.json").read_text(encoding="utf-8")
        )
        prepared_identity = json.loads(
            (out_dir / "quality-identity.json").read_text(encoding="utf-8")
        )
        prepared_session = json.loads(
            (out_dir / "session.json").read_text(encoding="utf-8")
        )
        report = json.loads(
            (out_dir / "preflight.json").read_text(encoding="utf-8")
        )

        assert prepared_manifest["variant"]["model"]["artifact_sha256"] == sha(model.read_bytes())
        assert prepared_manifest["variant"]["model"]["artifact_bytes"] == model.stat().st_size
        assert prepared_manifest["variant"]["hardware"]["profile_sha256"] == sha(profile.read_bytes())
        assert prepared_manifest["fixed"]["quality_eval"]["corpus_sha256"] == sha(corpus.read_bytes())
        assert prepared_identity["corpus_sha256"] == sha(corpus.read_bytes())
        assert prepared_manifest["fixed"]["quality_eval"]["evaluation_args"] == [
            "--fixture-mode",
            "strict",
        ]

        prompt_obj = json.loads(prompt.read_text(encoding="utf-8"))
        for field in (
            "messages_sha256",
            "chat_template_sha256",
            "rendered_sha256",
            "token_ids_sha256",
            "token_count",
        ):
            assert prepared_manifest["variant"]["prompt"][field] == prompt_obj[field]

        assert prepared_manifest["variant"]["runtime"] == manifest_obj["variant"]["runtime"]
        assert prepared_manifest["variant"]["execution"] == manifest_obj["variant"]["execution"]
        assert prepared_manifest["variant"]["model"]["quant"] == manifest_obj["variant"]["model"]["quant"]
        assert prepared_session["manifest"] == str((out_dir / "manifest.json").resolve())
        assert prepared_session["quality_identity"] == str((out_dir / "quality-identity.json").resolve())
        assert report["status"] == "READY-TO-RUN-I52"

        assert manifest.read_bytes() == source_manifest_bytes
        assert quality_identity.read_bytes() == source_identity_bytes

        out = run(
            [
                PY,
                str(HERE / "prepare_real_evidence_session.py"),
                str(session_path),
                "--out-dir",
                str(out_dir),
                "--allow-synthetic",
            ],
            expect=1,
        )
        assert "out-dir is not empty" in out

        bad_manifest_obj = json.loads(manifest.read_text(encoding="utf-8"))
        bad_manifest_obj["variant"]["runtime"]["runtime_identity"] = "REPLACE"
        bad_manifest = td / "bad-manifest.json"
        bad_manifest.write_text(
            json.dumps(bad_manifest_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        bad_session = dict(session)
        bad_session["manifest"] = str(bad_manifest)
        bad_session_path = td / "bad-session.json"
        bad_session_path.write_text(
            json.dumps(bad_session, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        bad_out = td / "bad-prepared"
        out = run(
            [
                PY,
                str(HERE / "prepare_real_evidence_session.py"),
                str(bad_session_path),
                "--out-dir",
                str(bad_out),
                "--allow-synthetic",
            ],
            expect=2,
        )
        assert "semantic field still missing/placeholder: variant.runtime.runtime_identity" in out
        assert not bad_out.exists()

        wrong_quality = dict(session)
        wrong_quality["quality_argv"] = list(session["quality_argv"])
        wrong_quality["quality_argv"][-1] = "different"
        wrong_quality_path = td / "wrong-quality-session.json"
        wrong_quality_path.write_text(
            json.dumps(wrong_quality, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        out = run(
            [
                PY,
                str(HERE / "prepare_real_evidence_session.py"),
                str(wrong_quality_path),
                "--out-dir",
                str(td / "wrong-quality-out"),
                "--allow-synthetic",
            ],
            expect=1,
        )
        assert "quality argv evaluation args do not exactly match quality identity" in out

    print("REAL EVIDENCE SESSION PREPARE SELFTEST: PASS")
    print("- model SHA/bytes, profile SHA, corpus SHA and prompt identity are materialized from real bytes")
    print("- source manifest and quality identity are never modified in place")
    print("- runtime/device/model-source/execution semantics are preserved, not inferred")
    print("- unresolved semantic placeholders block before benchmark launch")
    print("- quality argv must exactly match explicit quality identity evaluation_args")
    print("- synthetic fixture identities require explicit test allowance")


if __name__ == "__main__":
    main()

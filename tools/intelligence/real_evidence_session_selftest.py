#!/usr/bin/env python3
import hashlib
import json
import os
import stat
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


def write_executable(path, text):
    path.write_text(text, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


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
        model.write_bytes(b"synthetic-i52-model\n")
        profile = td / "profile.txt"
        profile.write_bytes(b"synthetic-i52-profile\n")
        prompt = td / "prompt-manifest.json"
        prompt.write_bytes((exp / "prompt-manifest.json").read_bytes())
        corpus = td / "quality-corpus.txt"
        corpus.write_bytes((exp / "quality-corpus.txt").read_bytes())

        identity_obj = json.loads(
            (exp / "quality-identity.json").read_text(encoding="utf-8")
        )
        identity_obj["corpus_sha256"] = sha(corpus.read_bytes())
        identity = td / "quality-identity.json"
        identity.write_text(
            json.dumps(identity_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        manifest_obj = json.loads(
            (exp / "manifest.json").read_text(encoding="utf-8")
        )
        manifest_obj["variant"]["hardware"]["profile_sha256"] = sha(
            profile.read_bytes()
        )
        manifest_obj["variant"]["model"]["artifact_sha256"] = sha(
            model.read_bytes()
        )
        manifest_obj["variant"]["model"]["artifact_bytes"] = model.stat().st_size
        manifest_obj["fixed"]["quality_eval"]["corpus_sha256"] = sha(
            corpus.read_bytes()
        )
        manifest_obj["fixed"]["quality_eval"]["evaluation_args"] = [
            "--fixture-mode",
            "strict",
        ]
        manifest = td / "manifest.json"
        manifest.write_text(
            json.dumps(manifest_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        fake_bench = td / "fake-llama-bench"
        fake_bench_code = """#!/usr/bin/env python3
import argparse, json
p=argparse.ArgumentParser()
p.add_argument("-m","--model",required=True)
p.add_argument("-p",type=int,required=True)
p.add_argument("-n",type=int,required=True)
p.add_argument("-r",type=int,required=True)
p.add_argument("-t",type=int,required=True)
p.add_argument("--type-k",required=True)
p.add_argument("--type-v",required=True)
p.add_argument("-ngl",type=int,required=True)
p.add_argument("--split-mode",required=True)
p.add_argument("--flash-attn",required=True)
p.add_argument("--tensor-split",default="")
p.add_argument("-o",required=True)
a=p.parse_args()
size=__import__("pathlib").Path(a.model).stat().st_size
common={
 "build_commit":"fixture-commit",
 "gpu_info":"Synthetic Fixture GPU",
 "backends":"FIXTURE",
 "model_size":size,
 "n_threads":a.t,
 "type_k":a.type_k,
 "type_v":a.type_v,
 "n_gpu_layers":a.ngl,
 "split_mode":a.split_mode,
 "flash_attn":a.flash_attn.lower() in ("1","true","on"),
 "tensor_split":a.tensor_split,
}
rows=[
 dict(common,test="pp512",n_prompt=a.p,n_gen=0,avg_ts=1000.0,samples_ts=[1000.0]*a.r),
 dict(common,test="tg128",n_prompt=0,n_gen=a.n,avg_ts=50.0,samples_ts=[50.0]*a.r),
]
print(json.dumps(rows))
"""
        write_executable(fake_bench, fake_bench_code)

        fake_quality = td / "fake-llama-perplexity"
        fake_quality_code = """#!/usr/bin/env python3
import argparse
p=argparse.ArgumentParser()
p.add_argument("-m","--model",required=True)
p.add_argument("-f","--file",required=True)
p.add_argument("--fixture-mode",required=True)
p.parse_args()
print("Final estimate: PPL = 10.5000 +/- 0.10000")
"""
        write_executable(fake_quality, fake_quality_code)

        session = {
            "real_evidence_session_schema_version": 1,
            "working_directory": str(td),
            "catalog": str(catalog),
            "manifest": str(manifest),
            "model_artifact": str(model),
            "hardware_profile": str(profile),
            "prompt_manifest": str(prompt),
            "quality_corpus": str(corpus),
            "quality_identity": str(identity),
            "hardware_id": "hw:fixture:24g",
            "model_id": "model:fixture:8b",
            "runtime_id": "runtime:fixture",
            "observed_at": "2026-08-28",
            "benchmark_argv": [
                str(fake_bench),
                "-m",
                str(model),
                "-p",
                "512",
                "-n",
                "128",
                "-r",
                "5",
                "-t",
                "8",
                "--type-k",
                "f16",
                "--type-v",
                "f16",
                "-ngl",
                "-1",
                "--split-mode",
                "none",
                "--flash-attn",
                "true",
                "--tensor-split",
                "",
                "-o",
                "json",
            ],
            "quality_argv": [
                str(fake_quality),
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

        out_dir = td / "session-out"
        out = run(
            [
                PY,
                str(HERE / "run_real_evidence_session.py"),
                str(session_path),
                "--out-dir",
                str(out_dir),
                "--allow-synthetic",
            ]
        )
        assert "REAL SESSION: READY" in out
        summary = json.loads(
            (out_dir / "session-summary.json").read_text(encoding="utf-8")
        )
        assert summary["status"] == "READY"
        assert summary["allow_synthetic"] is True
        assert len(summary["steps"]) == 4
        assert (out_dir / "quality" / "quality-metric.json").is_file()
        assert (out_dir / "intake-args.json").is_file()

        packet = json.loads(
            (out_dir / "benchmark" / "PACKET.json").read_text(encoding="utf-8")
        )
        packet_shas = {x["sha256"] for x in packet["files"]}
        for source in (profile, prompt, corpus, identity):
            assert sha(source.read_bytes()) in packet_shas

        second = run(
            [
                PY,
                str(HERE / "run_real_evidence_session.py"),
                str(session_path),
                "--out-dir",
                str(out_dir),
                "--allow-synthetic",
            ],
            expect=1,
        )
        assert "out-dir is not empty" in second

        bad_session = dict(session)
        bad_session["quality_argv"] = list(session["quality_argv"])
        bad_session["quality_argv"][-1] = "wrong"
        bad_path = td / "bad-session.json"
        bad_path.write_text(
            json.dumps(bad_session, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        bad_out = td / "bad-out"
        out = run(
            [
                PY,
                str(HERE / "run_real_evidence_session.py"),
                str(bad_path),
                "--out-dir",
                str(bad_out),
                "--allow-synthetic",
            ],
            expect=2,
        )
        assert "QUALITY CAPTURE: BLOCKED" in out or "CAPTURE: FAIL" in out
        bad_summary = json.loads(
            (bad_out / "session-summary.json").read_text(encoding="utf-8")
        )
        assert bad_summary["status"] == "BLOCKED"
        assert bad_summary["failure_step"] == "02-quality-capture"

    print("REAL EVIDENCE SESSION SELFTEST: PASS")
    print("- one explicit session runs benchmark seal, quality seal, PPL extraction and intake")
    print("- benchmark PACKET covers profile, prompt, corpus and quality identity")
    print("- successful session emits machine-readable READY summary and intake argv")
    print("- output directories are append-safe and never overwritten")
    print("- quality argv mismatch blocks and preserves the failed step summary")
    print("- all selftest PP/TG/PPL data are synthetic fixtures only")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TOOL = HERE / "bootstrap_real_evidence_workspace.py"
PY = sys.executable


def run(args, expect=0):
    cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if cp.returncode != expect:
        raise AssertionError(f"expected {expect}, got {cp.returncode}\n{cp.stdout}")
    return cp.stdout


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        generic = td / "generic"
        out = run([PY, str(TOOL), "--out-dir", str(generic)])
        assert "REAL WORKSPACE BOOTSTRAP: READY" in out

        state = json.loads((generic / "workspace.json").read_text(encoding="utf-8"))
        session = json.loads((generic / "real-session.json").read_text(encoding="utf-8"))
        probes = json.loads((generic / "semantic-probes.json").read_text(encoding="utf-8"))
        quality = json.loads((generic / "quality-identity.json").read_text(encoding="utf-8"))

        assert state["status"] == "NEEDS-REAL-INPUTS"
        assert state["automatic_benchmark_launch"] == "NOT-PERMITTED"
        assert state["automatic_catalog_ingestion"] == "NOT-PERMITTED"
        assert session["working_directory"] == str(generic.resolve())
        assert session["catalog"] == str((ROOT / "intelligence" / "catalog").resolve())
        assert session["manifest"] == str((generic / "baseline-manifest.json").resolve())
        assert session["hardware_profile"] == str((generic / "profile.txt").resolve())
        assert session["prompt_manifest"] == str((generic / "prompt-evidence" / "manifest.json").resolve())
        assert session["quality_identity"] == str((generic / "quality-identity.json").resolve())
        assert probes["working_directory"] == str(generic.resolve())
        assert quality["quality_identity_schema_version"] == 2

        assert not (generic / "profile.txt").exists()
        assert not (generic / "prompt-evidence" / "manifest.json").exists()
        assert not (generic / "quality-corpus.txt").exists()
        assert not any(generic.glob("*.gguf"))
        assert not (generic / "semantic-source-evidence").exists()
        assert not (generic / "prepared-session").exists()
        assert not (generic / "real-session-output").exists()

        rerun = run([PY, str(TOOL), "--out-dir", str(generic)], expect=1)
        assert "out-dir is not empty" in rerun

        nvidia = td / "nvidia"
        out = run([
            PY,
            str(TOOL),
            "--out-dir",
            str(nvidia),
            "--profile",
            "rtx3090-qwen3-8b-llamacpp",
        ])
        assert "REAL WORKSPACE BOOTSTRAP: READY" in out
        nsession = json.loads((nvidia / "real-session.json").read_text(encoding="utf-8"))
        nprobes = json.loads((nvidia / "semantic-probes.json").read_text(encoding="utf-8"))
        assert nsession["hardware_id"] == "hw:nvidia:geforce-rtx-3090:24g"
        assert nsession["model_id"] == "model:qwen:qwen3-8b"
        assert nsession["runtime_id"] == "runtime:ggml-org:llama.cpp"
        assert any(p["argv"][0] == "nvidia-smi" for p in nprobes["probes"])

        model = td / "real-model.gguf"
        model.write_bytes(b"real-path-binding-fixture\n")
        corpus = td / "real-corpus.txt"
        corpus.write_text("real path binding fixture\n", encoding="utf-8")
        bound = td / "bound"
        out = run([
            PY,
            str(TOOL),
            "--out-dir",
            str(bound),
            "--profile",
            "rtx3090-qwen3-8b-llamacpp",
            "--model-artifact",
            str(model),
            "--quality-corpus",
            str(corpus),
            "--observed-at",
            "2026-08-28",
        ])
        assert "REAL WORKSPACE BOOTSTRAP: READY" in out
        bsession = json.loads((bound / "real-session.json").read_text(encoding="utf-8"))
        assert bsession["model_artifact"] == str(model.resolve())
        assert bsession["quality_corpus"] == str(corpus.resolve())
        assert bsession["observed_at"] == "2026-08-28"
        assert str(model.resolve()) in bsession["benchmark_argv"]
        assert str(model.resolve()) in bsession["quality_argv"]
        assert str(corpus.resolve()) in bsession["quality_argv"]
        assert "REPLACE_WITH_ABSOLUTE_GGUF_PATH" not in bsession["benchmark_argv"]
        assert "REPLACE_WITH_ABSOLUTE_QUALITY_CORPUS_PATH" not in bsession["quality_argv"]

        invalid_dir = td / "invalid-date"
        invalid = run([
            PY,
            str(TOOL),
            "--out-dir",
            str(invalid_dir),
            "--observed-at",
            "not-a-date",
        ], expect=1)
        assert "observed-at must be YYYY-MM-DD" in invalid
        assert not invalid_dir.exists()

        missing_dir = td / "missing-model"
        missing = run([
            PY,
            str(TOOL),
            "--out-dir",
            str(missing_dir),
            "--model-artifact",
            str(td / "missing.gguf"),
        ], expect=1)
        assert "model artifact is not a file" in missing
        assert not missing_dir.exists()

    print("REAL WORKSPACE BOOTSTRAP SELFTEST: PASS")
    print("- generic and NVIDIA-first workspaces are created only from templates")
    print("- repository/catalog/workspace paths are bound explicitly")
    print("- no fake GGUF/profile/prompt/corpus/output evidence is created")
    print("- explicit existing model/corpus paths can be bound without semantic inference")
    print("- non-empty outputs, invalid dates, and missing bound artifacts are rejected")
    print("- bootstrap launches neither benchmark nor catalog ingestion")


if __name__ == "__main__":
    main()

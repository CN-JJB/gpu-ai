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
    p = subprocess.run(args, text=True, capture_output=True)
    out = p.stdout + p.stderr
    if p.returncode != expect:
        print(out)
        raise AssertionError(f"expected return code {expect}, got {p.returncode}: {args}")
    return out


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def packet_entry(path):
    data = path.read_bytes()
    return {
        "path": path.name,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def copy_catalog_without_synthetic_flag(src, dst):
    dst.mkdir()
    for name in ("hardware.jsonl", "models.jsonl", "runtimes.jsonl"):
        rows = []
        for line in (src / name).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            obj["synthetic"] = False
            rows.append(obj)
        (dst / name).write_text(
            "".join(json.dumps(x, separators=(",", ":")) + "\n" for x in rows),
            encoding="utf-8",
        )


def main():
    fixture_catalog = HERE / "fixtures" / "catalog"
    exp = HERE / "fixtures" / "experiment61"

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        catalog = td / "catalog"
        copy_catalog_without_synthetic_flag(fixture_catalog, catalog)

        model_bytes = b"tiny-local-model-artifact-for-i22\n"
        model = td / "model.gguf"
        model.write_bytes(model_bytes)

        profile_bytes = b"tiny-hardware-profile-for-i22\n"
        profile = td / "profile.txt"
        profile.write_bytes(profile_bytes)
        prompt_manifest = exp / "prompt-manifest.json"
        quality_corpus = exp / "quality-corpus.txt"
        quality_manifest = exp / "quality-identity.json"

        manifest_obj = json.loads((exp / "manifest.json").read_text(encoding="utf-8"))
        manifest_obj["variant"]["hardware"]["profile_sha256"] = sha256_bytes(profile_bytes)
        manifest_obj["variant"]["model"]["artifact_bytes"] = len(model_bytes)
        manifest_obj["variant"]["model"]["artifact_sha256"] = sha256_bytes(model_bytes)
        manifest = td / "manifest.json"
        manifest.write_text(json.dumps(manifest_obj, indent=2) + "\n", encoding="utf-8")

        result_obj = json.loads((exp / "result.json").read_text(encoding="utf-8"))
        for row in result_obj:
            row["model_size"] = len(model_bytes)
        result = td / "result.json"
        result.write_text(json.dumps(result_obj, indent=2) + "\n", encoding="utf-8")

        command_record = td / "command.json"
        command_record.write_text(
            json.dumps({
                "capture_schema_version": 1,
                "started_at": "2026-08-28T00:00:00Z",
                "ended_at": "2026-08-28T00:00:01Z",
                "cwd": str(td),
                "argv": ["llama-bench", "-m", str(model), "-o", "json"],
                "exit_code": 0,
                "launch_error": None,
                "executable": {
                    "requested": "llama-bench",
                    "resolved": None,
                    "bytes": None,
                    "sha256": None,
                },
                "manifest": {
                    "source": str(manifest),
                    "copied_path": "manifest.json",
                    "bytes": manifest.stat().st_size,
                    "sha256": sha256_bytes(manifest.read_bytes()),
                },
                "model_artifact": {
                    "argv_value": str(model),
                    "resolved": str(model.resolve()),
                    "bytes": len(model_bytes),
                    "sha256": sha256_bytes(model_bytes),
                },
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        packet = td / "PACKET.json"
        packet.write_text(
            json.dumps({
                "packet_schema_version": 1,
                "file_count": 7,
                "files": [
                    packet_entry(manifest),
                    packet_entry(result),
                    packet_entry(command_record),
                    packet_entry(profile),
                    packet_entry(prompt_manifest),
                    packet_entry(quality_corpus),
                    packet_entry(quality_manifest),
                ],
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        base = [
            PY,
            str(HERE / "verify_real_intake.py"),
            str(catalog),
            "--manifest",
            str(manifest),
            "--result",
            str(result),
            "--packet",
            str(packet),
            "--hardware-id",
            "hw:fixture:24g",
            "--model-id",
            "model:fixture:8b",
            "--runtime-id",
            "runtime:fixture",
            "--observed-at",
            "2026-08-28",
            "--hardware-profile",
            str(profile),
            "--prompt-manifest",
            str(prompt_manifest),
            "--quality-corpus",
            str(quality_corpus),
            "--quality-manifest",
            str(quality_manifest),
            "--command-record",
            str(command_record),
        ]

        out = run(base, expect=2)
        assert "non-synthetic model intake requires --model-artifact" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

        out = run(base + ["--model-artifact", str(model)])
        assert "MODEL ARTIFACT" in out
        assert "status=PASS" in out
        assert f"sha256={sha256_bytes(model_bytes)}" in out
        assert "RAW IDENTITY: PASS" in out
        assert "INTAKE: READY" in out

        wrong = td / "wrong.gguf"
        wrong.write_bytes(b"x" * len(model_bytes))
        out = run(base + ["--model-artifact", str(wrong)], expect=2)
        assert "local model artifact SHA256 != manifest artifact_sha256" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

    print("MODEL ARTIFACT GATE SELFTEST: PASS")
    print("- non-synthetic intake requires an explicit local model artifact")
    print("- matching local SHA256/bytes closes the file ↔ manifest ↔ raw model_size chain")
    print("- same-size but different-content artifacts are rejected by SHA256")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from quality_execution_test_support import write_quality_execution_fixture

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

        model_bytes = b"tiny-model-for-hardware-profile-i24\n"
        model = td / "model.gguf"
        model.write_bytes(model_bytes)

        profile_bytes = b"synthetic-device-profile-i24\n"
        profile = td / "profile.txt"
        profile.write_bytes(profile_bytes)

        wrong_profile = td / "wrong-profile.txt"
        wrong_profile.write_bytes(b"x" * len(profile_bytes))
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

        command = td / "command.json"
        command.write_text(
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
                    packet_entry(command),
                    packet_entry(profile),
                    packet_entry(prompt_manifest),
                    packet_entry(quality_corpus),
                    packet_entry(quality_manifest),
                ],
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        quality_exec = write_quality_execution_fixture(
            td / "quality-execution",
            model,
            quality_corpus,
            quality_manifest,
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
            "--model-artifact",
            str(model),
            "--command-record",
            str(command),
            "--prompt-manifest",
            str(prompt_manifest),
            "--quality-corpus",
            str(quality_corpus),
            "--quality-manifest",
            str(quality_manifest),
            "--quality-command-record",
            str(quality_exec["command"]),
            "--quality-stdout",
            str(quality_exec["stdout"]),
            "--quality-stderr",
            str(quality_exec["stderr"]),
            "--quality-packet",
            str(quality_exec["packet"]),
        ]

        out = run(base, expect=2)
        assert "non-synthetic hardware intake requires --hardware-profile" in out
        assert "HARDWARE PROFILE" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

        out = run(base + ["--hardware-profile", str(profile)])
        assert "HARDWARE PROFILE" in out
        assert "status=PASS" in out
        assert f"sha256={sha256_bytes(profile_bytes)}" in out
        assert "RAW IDENTITY: PASS" in out
        assert "INTAKE: READY" in out

        bad_packet = td / "bad-PACKET.json"
        bad_packet.write_text(
            json.dumps({
                "packet_schema_version": 1,
                "file_count": 4,
                "files": [
                    packet_entry(manifest),
                    packet_entry(result),
                    packet_entry(command),
                    packet_entry(wrong_profile),
                    packet_entry(prompt_manifest),
                    packet_entry(quality_corpus),
                ],
            }, indent=2) + "\n",
            encoding="utf-8",
        )

        bad_base = list(base)
        packet_index = bad_base.index(str(packet))
        bad_base[packet_index] = str(bad_packet)
        out = run(bad_base + ["--hardware-profile", str(wrong_profile)], expect=2)
        assert "hardware profile SHA256 != manifest variant.hardware.profile_sha256" in out
        assert "INTAKE: BLOCKED" in out

    print("HARDWARE PROFILE GATE SELFTEST: PASS")
    print("- non-synthetic intake requires a concrete hardware profile artifact")
    print("- matching profile SHA256 and PACKET coverage pass")
    print("- a same-size wrong profile remains blocked even when PACKET is recomputed")


if __name__ == "__main__":
    main()

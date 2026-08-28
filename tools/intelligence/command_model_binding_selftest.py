#!/usr/bin/env python3
import hashlib
import json
import shutil
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


def packet_entry(root, path):
    data = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
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

        model_bytes = b"tiny-command-bound-model-artifact-i23\n"
        model = td / "model.gguf"
        model.write_bytes(model_bytes)

        profile_bytes = b"tiny-hardware-profile-for-i23\n"
        profile = td / "profile.txt"
        profile.write_bytes(profile_bytes)
        prompt_manifest = exp / "prompt-manifest.json"
        quality_corpus = exp / "quality-corpus.txt"
        quality_manifest = exp / "quality-identity.json"

        wrong_model = td / "wrong.gguf"
        wrong_model.write_bytes(b"x" * len(model_bytes))

        manifest_obj = json.loads((exp / "manifest.json").read_text(encoding="utf-8"))
        manifest_obj["variant"]["hardware"]["profile_sha256"] = sha256_bytes(profile_bytes)
        manifest_obj["variant"]["model"]["artifact_bytes"] = len(model_bytes)
        manifest_obj["variant"]["model"]["artifact_sha256"] = sha256_bytes(model_bytes)
        manifest = td / "source-manifest.json"
        manifest.write_text(json.dumps(manifest_obj, indent=2) + "\n", encoding="utf-8")

        result_obj = json.loads((exp / "result.json").read_text(encoding="utf-8"))
        for row in result_obj:
            row["model_size"] = len(model_bytes)
        raw_source = td / "raw-source.json"
        raw_source.write_text(json.dumps(result_obj, indent=2) + "\n", encoding="utf-8")

        fake = td / "fake_llama_bench.py"
        fake.write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "sys.stdout.write(Path(sys.argv[-1]).read_text(encoding='utf-8'))\n"
            "sys.stderr.write('i23 synthetic diagnostic\\n')\n",
            encoding="utf-8",
        )

        sealed = td / "sealed"
        out = run([
            PY,
            str(HERE / "capture_real_benchmark.py"),
            "--manifest",
            str(manifest),
            "--out-dir",
            str(sealed),
            "--model-artifact",
            str(model),
            "--include",
            str(profile),
            "--include",
            str(prompt_manifest),
            "--include",
            str(quality_corpus),
            "--include",
            str(quality_manifest),
            "--",
            PY,
            str(fake),
            "-m",
            str(model),
            str(raw_source),
        ])
        assert "CAPTURE: SEALED" in out
        assert "model_binding=PASS" in out

        command = json.loads((sealed / "command.json").read_text(encoding="utf-8"))
        assert command["model_artifact"]["sha256"] == sha256_bytes(model_bytes)
        assert command["model_artifact"]["bytes"] == len(model_bytes)
        assert command["model_artifact"]["resolved"] == str(model.resolve())

        quality_exec = write_quality_execution_fixture(
            td / "quality-execution",
            model,
            sealed / "evidence" / "quality-corpus.txt",
            sealed / "evidence" / "quality-identity.json",
        )

        verify_base = [
            PY,
            str(HERE / "verify_real_intake.py"),
            str(catalog),
            "--manifest",
            str(sealed / "manifest.json"),
            "--result",
            str(sealed / "result.json"),
            "--packet",
            str(sealed / "PACKET.json"),
            "--hardware-id",
            "hw:fixture:24g",
            "--model-id",
            "model:fixture:8b",
            "--runtime-id",
            "runtime:fixture",
            "--observed-at",
            "2026-08-28",
            "--hardware-profile",
            str(sealed / "evidence" / "profile.txt"),
            "--prompt-manifest",
            str(sealed / "evidence" / "prompt-manifest.json"),
            "--quality-corpus",
            str(sealed / "evidence" / "quality-corpus.txt"),
            "--quality-manifest",
            str(sealed / "evidence" / "quality-identity.json"),
            "--model-artifact",
            str(model),
            "--command-record",
            str(sealed / "command.json"),
            "--quality-command-record",
            str(quality_exec["command"]),
            "--quality-stdout",
            str(quality_exec["stdout"]),
            "--quality-stderr",
            str(quality_exec["stderr"]),
            "--quality-packet",
            str(quality_exec["packet"]),
            "--quality-metric",
            str(quality_exec["metric"]),
        ]
        out = run(verify_base)
        assert "MODEL ARTIFACT" in out
        assert "COMMAND ↔ ARTIFACT BINDING" in out
        assert "RAW IDENTITY: PASS" in out
        assert "INTAKE: READY" in out

        mismatch_out = td / "mismatch"
        out = run([
            PY,
            str(HERE / "capture_real_benchmark.py"),
            "--manifest",
            str(manifest),
            "--out-dir",
            str(mismatch_out),
            "--model-artifact",
            str(model),
            "--",
            PY,
            str(fake),
            "-m",
            str(wrong_model),
            str(raw_source),
        ], expect=1)
        assert "command model path does not match --model-artifact" in out
        assert not mismatch_out.exists()

        tampered = td / "tampered"
        tampered.mkdir()
        for name in ("manifest.json", "result.json", "stderr.txt", "command.json"):
            shutil.copy2(sealed / name, tampered / name)
        (tampered / "evidence").mkdir()
        shutil.copy2(sealed / "evidence" / "profile.txt", tampered / "evidence" / "profile.txt")
        shutil.copy2(sealed / "evidence" / "prompt-manifest.json", tampered / "evidence" / "prompt-manifest.json")
        shutil.copy2(sealed / "evidence" / "quality-corpus.txt", tampered / "evidence" / "quality-corpus.txt")
        shutil.copy2(sealed / "evidence" / "quality-identity.json", tampered / "evidence" / "quality-identity.json")

        tampered_command_path = tampered / "command.json"
        tampered_command = json.loads(tampered_command_path.read_text(encoding="utf-8"))
        argv = tampered_command["argv"]
        model_index = argv.index(str(model))
        argv[model_index] = str(wrong_model)
        tampered_command_path.write_text(
            json.dumps(tampered_command, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        packet = {
            "packet_schema_version": 1,
            "file_count": 8,
            "files": [
                packet_entry(tampered, tampered / "manifest.json"),
                packet_entry(tampered, tampered / "result.json"),
                packet_entry(tampered, tampered / "stderr.txt"),
                packet_entry(tampered, tampered / "command.json"),
                packet_entry(tampered, tampered / "evidence" / "profile.txt"),
                packet_entry(tampered, tampered / "evidence" / "prompt-manifest.json"),
                packet_entry(tampered, tampered / "evidence" / "quality-corpus.txt"),
                packet_entry(tampered, tampered / "evidence" / "quality-identity.json"),
            ],
        }
        (tampered / "PACKET.json").write_text(
            json.dumps(packet, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        out = run([
            PY,
            str(HERE / "verify_real_intake.py"),
            str(catalog),
            "--manifest",
            str(tampered / "manifest.json"),
            "--result",
            str(tampered / "result.json"),
            "--packet",
            str(tampered / "PACKET.json"),
            "--hardware-id",
            "hw:fixture:24g",
            "--model-id",
            "model:fixture:8b",
            "--runtime-id",
            "runtime:fixture",
            "--observed-at",
            "2026-08-28",
            "--hardware-profile",
            str(tampered / "evidence" / "profile.txt"),
            "--prompt-manifest",
            str(tampered / "evidence" / "prompt-manifest.json"),
            "--quality-corpus",
            str(tampered / "evidence" / "quality-corpus.txt"),
            "--quality-manifest",
            str(tampered / "evidence" / "quality-identity.json"),
            "--model-artifact",
            str(model),
            "--command-record",
            str(tampered / "command.json"),
        ], expect=2)
        assert "command model path does not match --model-artifact" in out
        assert "INTAKE: BLOCKED" in out

    print("COMMAND MODEL BINDING SELFTEST: PASS")
    print("- capture refuses a supplied artifact that differs from exact -m/--model argv")
    print("- command.json records the bound artifact SHA256/bytes")
    print("- intake independently reparses argv and requires the command record to be PACKET-indexed")
    print("- tampered argv with a freshly recomputed PACKET remains blocked")


if __name__ == "__main__":
    main()

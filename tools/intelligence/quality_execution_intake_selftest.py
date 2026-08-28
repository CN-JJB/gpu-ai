#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from quality_execution_test_support import (
    write_packet,
    write_quality_execution_fixture,
)


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

        model_bytes = b"tiny-model-for-quality-intake-i29\n"
        model = td / "model.gguf"
        model.write_bytes(model_bytes)

        profile_bytes = b"tiny-profile-for-quality-intake-i29\n"
        profile = td / "profile.txt"
        profile.write_bytes(profile_bytes)

        prompt = td / "prompt-manifest.json"
        prompt.write_bytes((exp / "prompt-manifest.json").read_bytes())

        corpus = td / "quality-corpus.txt"
        corpus.write_bytes((exp / "quality-corpus.txt").read_bytes())
        corpus_bytes = corpus.read_bytes()

        quality_manifest = td / "quality-identity.json"
        quality_manifest.write_bytes((exp / "quality-identity.json").read_bytes())

        manifest_obj = json.loads((exp / "manifest.json").read_text(encoding="utf-8"))
        manifest_obj["variant"]["hardware"]["profile_sha256"] = sha256_bytes(profile_bytes)
        manifest_obj["variant"]["model"]["artifact_bytes"] = len(model_bytes)
        manifest_obj["variant"]["model"]["artifact_sha256"] = sha256_bytes(model_bytes)
        manifest_obj["fixed"]["quality_eval"]["corpus_sha256"] = sha256_bytes(corpus_bytes)
        manifest = td / "manifest.json"
        manifest.write_text(json.dumps(manifest_obj, indent=2) + "\n", encoding="utf-8")

        result_obj = json.loads((exp / "result.json").read_text(encoding="utf-8"))
        for row in result_obj:
            row["model_size"] = len(model_bytes)
        result = td / "result.json"
        result.write_text(json.dumps(result_obj, indent=2) + "\n", encoding="utf-8")

        command = td / "command.json"
        command.write_text(
            json.dumps(
                {
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
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        packet = td / "PACKET.json"
        packet.write_text(
            json.dumps(
                {
                    "packet_schema_version": 1,
                    "file_count": 7,
                    "files": [
                        packet_entry(manifest),
                        packet_entry(result),
                        packet_entry(command),
                        packet_entry(profile),
                        packet_entry(prompt),
                        packet_entry(corpus),
                        packet_entry(quality_manifest),
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        quality_exec = write_quality_execution_fixture(
            td / "quality-execution",
            model,
            corpus,
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
            "--hardware-profile",
            str(profile),
            "--prompt-manifest",
            str(prompt),
            "--quality-corpus",
            str(corpus),
            "--quality-manifest",
            str(quality_manifest),
            "--model-artifact",
            str(model),
            "--command-record",
            str(command),
        ]

        out = run(base, expect=2)
        assert "non-synthetic intake requires quality execution evidence" in out
        assert "QUALITY EXECUTION" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

        exec_args = [
            "--quality-command-record",
            str(quality_exec["command"]),
            "--quality-stdout",
            str(quality_exec["stdout"]),
            "--quality-stderr",
            str(quality_exec["stderr"]),
            "--quality-packet",
            str(quality_exec["packet"]),
        ]
        out = run(base + exec_args, expect=2)
        assert "non-synthetic intake requires --quality-metric" in out
        assert "QUALITY METRIC" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

        full_args = exec_args + [
            "--quality-metric",
            str(quality_exec["metric"]),
        ]
        out = run(base + full_args)
        assert "QUALITY EXECUTION" in out
        assert "QUALITY METRIC" in out
        assert "status=PASS" in out
        assert "RAW IDENTITY: PASS" in out
        assert "INTAKE: READY" in out

        wrong_corpus = td / "wrong-corpus.txt"
        wrong_corpus.write_bytes(b"x" * corpus.stat().st_size)

        tampered_command = td / "tampered-quality-command.json"
        bad_obj = json.loads(
            quality_exec["command"].read_text(encoding="utf-8")
        )
        argv = list(bad_obj["argv"])
        idx = argv.index("-f")
        argv[idx + 1] = str(wrong_corpus)
        bad_obj["argv"] = argv
        tampered_command.write_text(
            json.dumps(bad_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        tampered_packet = td / "tampered-quality-PACKET.json"
        write_packet(
            tampered_packet,
            [
                tampered_command,
                quality_exec["stdout"],
                quality_exec["stderr"],
                quality_exec["identity"],
            ],
        )

        tampered_args = [
            "--quality-command-record",
            str(tampered_command),
            "--quality-stdout",
            str(quality_exec["stdout"]),
            "--quality-stderr",
            str(quality_exec["stderr"]),
            "--quality-packet",
            str(tampered_packet),
            "--quality-metric",
            str(quality_exec["metric"]),
        ]
        out = run(base + tampered_args, expect=2)
        assert (
            "quality execution: quality command corpus path does not match --quality-corpus"
            in out
        )
        assert "QUALITY EXECUTION" in out
        assert "status=BLOCKED" in out
        assert "INTAKE: BLOCKED" in out

    print("QUALITY EXECUTION INTAKE SELFTEST: PASS")
    print("- non-synthetic intake cannot reach READY without I28 execution evidence")
    print("- valid quality execution plus machine metric admits the existing I26/I27 contract")
    print("- missing quality metric blocks non-synthetic intake")
    print("- recomputed quality PACKET cannot hide semantic corpus-argv tampering")
    print("- synthetic fixture output is not a measured PPL or production benchmark")


if __name__ == "__main__":
    main()

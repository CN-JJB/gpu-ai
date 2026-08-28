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


def packet_entry(path):
    data = path.read_bytes()
    return {
        "path": path.name,
        "bytes": len(data),
        "sha256": sha256_bytes(data),
    }


def write_packet(path, files):
    path.write_text(
        json.dumps(
            {
                "packet_schema_version": 1,
                "file_count": len(files),
                "files": [packet_entry(x) for x in files],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def verify_args(sealed, model, corpus, quality_manifest, packet=None, command=None):
    return [
        PY,
        str(HERE / "verify_quality_execution.py"),
        "--quality-command-record",
        str(command or (sealed / "quality-command.json")),
        "--stdout",
        str(sealed / "stdout.txt"),
        "--stderr",
        str(sealed / "stderr.txt"),
        "--packet",
        str(packet or (sealed / "PACKET.json")),
        "--model-artifact",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(quality_manifest),
    ]


def write_fake(path, exit_code=0):
    path.write_text(
        "#!/usr/bin/env python3\n"
        "import argparse, sys\n"
        "p = argparse.ArgumentParser()\n"
        "p.add_argument('-m', '--model', required=True)\n"
        "p.add_argument('-f', '--file', required=True)\n"
        "p.add_argument('--fixture-eval', required=True)\n"
        "p.add_argument('--fixture-repeat', required=True)\n"
        "p.parse_args()\n"
        "print('synthetic raw quality output; not a measured PPL')\n"
        f"sys.exit({exit_code})\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"tiny-quality-model-i28-i30\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"quality corpus bytes for i28-i30\n")

        evaluation_args = [
            "--fixture-eval",
            "strict",
            "--fixture-repeat",
            "2",
        ]
        quality_manifest = td / "quality-identity.json"
        quality_manifest.write_text(
            json.dumps(
                {
                    "quality_identity_schema_version": 2,
                    "tokenizer_identity": "fixture-tokenizer",
                    "corpus_sha256": sha256_bytes(corpus.read_bytes()),
                    "fixture_revision": "fixture-i28-i30",
                    "evaluation_args": evaluation_args,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        fake = td / "fake-perplexity"
        write_fake(fake)

        sealed = td / "sealed"
        out = run(
            [
                PY,
                str(HERE / "capture_quality_eval.py"),
                "--out-dir",
                str(sealed),
                "--model-artifact",
                str(model),
                "--quality-corpus",
                str(corpus),
                "--quality-manifest",
                str(quality_manifest),
                "--",
                str(fake),
                "-m",
                str(model),
                "-f",
                str(corpus),
                *evaluation_args,
            ]
        )
        assert "QUALITY CAPTURE: SEALED" in out
        assert "evaluation_args_binding=PASS" in out

        for name in (
            "quality-identity.json",
            "stdout.txt",
            "stderr.txt",
            "quality-command.json",
            "PACKET.json",
        ):
            assert (sealed / name).is_file()

        command_obj = json.loads(
            (sealed / "quality-command.json").read_text(encoding="utf-8")
        )
        assert command_obj["quality_capture_schema_version"] == 2
        assert command_obj["evaluation_args"] == evaluation_args
        assert command_obj["model_artifact"]["sha256"] == sha256_bytes(model.read_bytes())
        assert command_obj["quality_corpus"]["sha256"] == sha256_bytes(corpus.read_bytes())
        assert command_obj["quality_identity"]["sha256"] == sha256_bytes(
            quality_manifest.read_bytes()
        )

        out = run(
            verify_args(
                sealed,
                model,
                corpus,
                sealed / "quality-identity.json",
            )
        )
        assert "QUALITY EXECUTION: PASS" in out
        assert "evaluation_args_binding=PASS" in out

        wrong_corpus = td / "wrong-corpus.txt"
        wrong_corpus.write_bytes(b"x" * corpus.stat().st_size)
        mismatch_out = td / "mismatch"
        out = run(
            [
                PY,
                str(HERE / "capture_quality_eval.py"),
                "--out-dir",
                str(mismatch_out),
                "--model-artifact",
                str(model),
                "--quality-corpus",
                str(corpus),
                "--quality-manifest",
                str(quality_manifest),
                "--",
                str(fake),
                "-m",
                str(model),
                "-f",
                str(wrong_corpus),
                *evaluation_args,
            ],
            expect=1,
        )
        assert "command corpus path does not match --quality-corpus" in out
        assert not mismatch_out.exists()

        tampered_command = td / "tampered-quality-command.json"
        bad_command_obj = json.loads(
            (sealed / "quality-command.json").read_text(encoding="utf-8")
        )
        argv = list(bad_command_obj["argv"])
        idx = argv.index("-f")
        argv[idx + 1] = str(wrong_corpus)
        bad_command_obj["argv"] = argv
        tampered_command.write_text(
            json.dumps(bad_command_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        tampered_packet = td / "tampered-PACKET.json"
        write_packet(
            tampered_packet,
            [
                tampered_command,
                sealed / "stdout.txt",
                sealed / "stderr.txt",
                sealed / "quality-identity.json",
            ],
        )
        out = run(
            verify_args(
                sealed,
                model,
                corpus,
                sealed / "quality-identity.json",
                packet=tampered_packet,
                command=tampered_command,
            ),
            expect=2,
        )
        assert "quality command corpus path does not match --quality-corpus" in out
        assert "QUALITY EXECUTION: BLOCKED" in out

        tampered_identity = td / "tampered-quality-identity.json"
        bad_identity_obj = json.loads(
            quality_manifest.read_text(encoding="utf-8")
        )
        bad_identity_obj["evaluation_args"] = [
            "--fixture-eval",
            "loose",
            "--fixture-repeat",
            "2",
        ]
        tampered_identity.write_text(
            json.dumps(bad_identity_obj, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        identity_packet = td / "identity-PACKET.json"
        write_packet(
            identity_packet,
            [
                sealed / "quality-command.json",
                sealed / "stdout.txt",
                sealed / "stderr.txt",
                tampered_identity,
            ],
        )
        out = run(
            verify_args(
                sealed,
                model,
                corpus,
                tampered_identity,
                packet=identity_packet,
            ),
            expect=2,
        )
        assert (
            "quality command quality_identity SHA256 does not match supplied quality manifest"
            in out
        )
        assert "executed evaluation_args do not match quality manifest" in out
        assert "QUALITY EXECUTION: BLOCKED" in out

        fail_script = td / "fail-quality"
        write_fake(fail_script, exit_code=3)
        failed = td / "failed"
        out = run(
            [
                PY,
                str(HERE / "capture_quality_eval.py"),
                "--out-dir",
                str(failed),
                "--model-artifact",
                str(model),
                "--quality-corpus",
                str(corpus),
                "--quality-manifest",
                str(quality_manifest),
                "--",
                str(fail_script),
                "-m",
                str(model),
                "-f",
                str(corpus),
                *evaluation_args,
            ],
            expect=2,
        )
        assert "QUALITY CAPTURE: BLOCKED" in out
        assert (failed / "quality-command.json").is_file()
        assert (failed / "PACKET.json").is_file()

    print("QUALITY EXECUTION SELFTEST: PASS")
    print("- exact model, corpus and evaluation argv are bound before launch")
    print("- raw stdout/stderr, exact argv and identity artifact are sealed")
    print("- recomputed PACKET cannot hide semantic argv or identity tampering")
    print("- non-zero quality execution remains auditable but blocked")


if __name__ == "__main__":
    main()

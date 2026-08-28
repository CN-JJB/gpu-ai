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


def verify_args(sealed, model, corpus, identity, packet=None, command=None):
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
        str(identity),
    ]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        model = td / "model.gguf"
        model.write_bytes(b"i30-model\n")

        corpus = td / "corpus.txt"
        corpus.write_bytes(b"i30-corpus\n")

        declared = ["--mode", "strict", "--repeat", "2"]
        identity = td / "quality-identity.json"
        identity.write_text(
            json.dumps(
                {
                    "quality_identity_schema_version": 2,
                    "tokenizer_identity": "fixture-tokenizer-i30",
                    "corpus_sha256": sha256_bytes(corpus.read_bytes()),
                    "fixture_revision": "fixture-i30",
                    "evaluation_args": declared,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        fake = td / "fake-quality"
        fake.write_text(
            "#!/usr/bin/env python3\n"
            "import argparse\n"
            "p = argparse.ArgumentParser()\n"
            "p.add_argument('-m', '--model', required=True)\n"
            "p.add_argument('-f', '--file', required=True)\n"
            "p.add_argument('--mode', required=True)\n"
            "p.add_argument('--repeat', required=True)\n"
            "p.parse_args()\n"
            "print('synthetic i30 output; no measured PPL')\n",
            encoding="utf-8",
        )
        fake.chmod(0o755)

        mismatch = td / "mismatch"
        out = run(
            [
                PY,
                str(HERE / "capture_quality_eval.py"),
                "--out-dir",
                str(mismatch),
                "--model-artifact",
                str(model),
                "--quality-corpus",
                str(corpus),
                "--quality-manifest",
                str(identity),
                "--",
                str(fake),
                "-m",
                str(model),
                "-f",
                str(corpus),
                "--mode",
                "loose",
                "--repeat",
                "2",
            ],
            expect=1,
        )
        assert "declared evaluation_args do not match executed quality argv" in out
        assert not mismatch.exists()

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
                str(identity),
                "--",
                str(fake),
                "-m",
                str(model),
                "-f",
                str(corpus),
                *declared,
            ]
        )
        assert "evaluation_args_binding=PASS" in out
        assert "QUALITY CAPTURE: SEALED" in out

        out = run(verify_args(sealed, model, corpus, sealed / "quality-identity.json"))
        assert "evaluation_args_binding=PASS" in out
        assert "QUALITY EXECUTION: PASS" in out

        tampered_command = td / "tampered-command.json"
        obj = json.loads(
            (sealed / "quality-command.json").read_text(encoding="utf-8")
        )
        argv = list(obj["argv"])
        idx = argv.index("--mode")
        argv[idx + 1] = "loose"
        obj["argv"] = argv
        obj["evaluation_args"] = ["--mode", "loose", "--repeat", "2"]
        tampered_command.write_text(
            json.dumps(obj, indent=2, sort_keys=True) + "\n",
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
        assert "executed evaluation_args do not match quality manifest" in out
        assert "evaluation_args_binding=BLOCKED" in out
        assert "QUALITY EXECUTION: BLOCKED" in out

    print("QUALITY EVALUATION ARGS SELFTEST: PASS")
    print("- v2 evaluation_args are exact argv tokens, not a shell string")
    print("- model/corpus selectors are excluded from the evaluation token list")
    print("- capture blocks mismatched declared vs executed evaluation args before launch")
    print("- recomputed PACKET cannot hide semantic evaluation-argv tampering")


if __name__ == "__main__":
    main()

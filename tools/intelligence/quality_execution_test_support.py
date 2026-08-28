#!/usr/bin/env python3
"""Synthetic-only support for Intelligence gate self-tests.

This module writes tiny quality-execution evidence fixtures. It must never be
used as measured model-quality evidence or copied into the production catalog.
"""

import hashlib
import json
from pathlib import Path


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


def write_quality_execution_fixture(root, model, corpus, quality_manifest):
    root.mkdir(parents=True, exist_ok=False)

    model = Path(model).resolve()
    corpus = Path(corpus).resolve()
    quality_manifest = Path(quality_manifest).resolve()

    quality_obj = json.loads(quality_manifest.read_text(encoding="utf-8"))
    evaluation_args = quality_obj.get("evaluation_args")
    if (
        quality_obj.get("quality_identity_schema_version") != 2
        or not isinstance(evaluation_args, list)
        or not all(isinstance(x, str) and x != "" for x in evaluation_args)
    ):
        raise ValueError("synthetic quality fixture requires v2 evaluation_args token list")

    identity = root / "quality-identity.json"
    identity.write_bytes(quality_manifest.read_bytes())

    stdout = root / "stdout.txt"
    stdout.write_text(
        "SYNTHETIC QUALITY EXECUTION FIXTURE ONLY; no measured PPL or task score.\n",
        encoding="utf-8",
    )
    stderr = root / "stderr.txt"
    stderr.write_bytes(b"")

    argv = [
        "llama-perplexity",
        "-m",
        str(model),
        "-f",
        str(corpus),
    ] + list(evaluation_args)

    command = root / "quality-command.json"
    command_obj = {
        "quality_capture_schema_version": 2,
        "started_at": "2026-08-28T00:00:00Z",
        "ended_at": "2026-08-28T00:00:01Z",
        "cwd": str(root.resolve()),
        "argv": argv,
        "evaluation_args": list(evaluation_args),
        "exit_code": 0,
        "launch_error": None,
        "executable": {
            "requested": "llama-perplexity",
            "resolved": None,
            "bytes": None,
            "sha256": None,
        },
        "model_artifact": {
            "argv_value": str(model),
            "resolved": str(model),
            "bytes": model.stat().st_size,
            "sha256": sha256_bytes(model.read_bytes()),
        },
        "quality_corpus": {
            "argv_value": str(corpus),
            "resolved": str(corpus),
            "bytes": corpus.stat().st_size,
            "sha256": sha256_bytes(corpus.read_bytes()),
        },
        "quality_identity": {
            "source": str(quality_manifest),
            "copied_path": "quality-identity.json",
            "bytes": identity.stat().st_size,
            "sha256": sha256_bytes(identity.read_bytes()),
        },
    }
    command.write_text(
        json.dumps(command_obj, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    packet = root / "PACKET.json"
    write_packet(packet, [command, stdout, stderr, identity])

    return {
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "packet": packet,
        "identity": identity,
    }

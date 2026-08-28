#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A"}


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def valid_evaluation_args(value):
    return (
        isinstance(value, list)
        and all(isinstance(item, str) and item != "" for item in value)
    )


def resolve_executable(value):
    candidate = Path(value)
    if candidate.is_file():
        return candidate.resolve()
    found = shutil.which(value)
    return Path(found).resolve() if found else None


def parse_quality_argv(command):
    if not isinstance(command, list) or not command:
        raise ValueError("quality command argv must be a non-empty list")
    if not all(isinstance(item, str) and item != "" for item in command):
        raise ValueError("quality command argv must contain only non-empty strings")

    model_paths = []
    corpus_paths = []
    evaluation_args = []

    i = 1
    while i < len(command):
        arg = command[i]

        if arg in ("-m", "--model"):
            if i + 1 >= len(command):
                raise ValueError(f"{arg} is missing its model path")
            model_paths.append(command[i + 1])
            i += 2
            continue
        if arg.startswith("--model="):
            model_paths.append(arg.split("=", 1)[1])
            i += 1
            continue

        if arg in ("-f", "--file"):
            if i + 1 >= len(command):
                raise ValueError(f"{arg} is missing its quality corpus path")
            corpus_paths.append(command[i + 1])
            i += 2
            continue
        if arg.startswith("--file="):
            corpus_paths.append(arg.split("=", 1)[1])
            i += 1
            continue

        evaluation_args.append(arg)
        i += 1

    if len(model_paths) != 1:
        raise ValueError(
            f"expected exactly one -m/--model path; found {len(model_paths)}"
        )
    if len(corpus_paths) != 1:
        raise ValueError(
            f"expected exactly one -f/--file path; found {len(corpus_paths)}"
        )

    return model_paths[0], corpus_paths[0], evaluation_args


def resolve_recorded_path(value, cwd):
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = Path(cwd) / path
    return path.resolve()


def packet_entry(root, path):
    rel = path.relative_to(root)
    return {
        "path": rel.as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def build_packet(root, files):
    records = [packet_entry(root, path) for path in files]
    return {
        "packet_schema_version": 1,
        "file_count": len(records),
        "files": records,
    }


def ensure_output_dir(path):
    if path.exists():
        if not path.is_dir():
            raise SystemExit(f"CAPTURE: FAIL\nout-dir is not a directory: {path}")
        if any(path.iterdir()):
            raise SystemExit(f"CAPTURE: FAIL\nout-dir is not empty: {path}")
    else:
        path.mkdir(parents=True)


def main():
    p = argparse.ArgumentParser(
        description=(
            "Run an explicit quality-evaluation argv, bind model/corpus/evaluation config, "
            "preserve raw output, and seal an integrity packet."
        )
    )
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--model-artifact", type=Path, required=True)
    p.add_argument("--quality-corpus", type=Path, required=True)
    p.add_argument("--quality-manifest", type=Path, required=True)
    p.add_argument(
        "--include",
        action="append",
        default=[],
        type=Path,
        help="Additional evidence file copied under out-dir/evidence/ (repeatable).",
    )
    p.add_argument("command", nargs=argparse.REMAINDER)
    a = p.parse_args()

    command = list(a.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("CAPTURE: FAIL\nmissing command after --")

    for label, path in (
        ("model artifact", a.model_artifact),
        ("quality corpus", a.quality_corpus),
        ("quality manifest", a.quality_manifest),
    ):
        if not path.is_file():
            raise SystemExit(f"CAPTURE: FAIL\n{label} is not a file: {path}")

    quality_bytes = a.quality_manifest.read_bytes()
    try:
        quality_obj = json.loads(quality_bytes.decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"CAPTURE: FAIL\nquality manifest is not valid UTF-8 JSON: {exc}")
    if not isinstance(quality_obj, dict):
        raise SystemExit("CAPTURE: FAIL\nquality manifest must be one JSON object")
    if quality_obj.get("quality_identity_schema_version") != 2:
        raise SystemExit("CAPTURE: FAIL\nquality_identity_schema_version must be 2")

    for field in ("tokenizer_identity", "corpus_sha256", "fixture_revision"):
        if not present(quality_obj.get(field)):
            raise SystemExit(f"CAPTURE: FAIL\nquality manifest missing/placeholder {field}")

    declared_evaluation_args = quality_obj.get("evaluation_args")
    if not valid_evaluation_args(declared_evaluation_args):
        raise SystemExit(
            "CAPTURE: FAIL\n"
            "quality manifest evaluation_args must be a JSON list of non-empty strings"
        )

    try:
        argv_model, argv_corpus, executed_evaluation_args = parse_quality_argv(command)
    except ValueError as exc:
        raise SystemExit(f"CAPTURE: FAIL\n{exc}")

    if executed_evaluation_args != declared_evaluation_args:
        raise SystemExit(
            "CAPTURE: FAIL\n"
            "declared evaluation_args do not match executed quality argv: "
            f"declared={declared_evaluation_args!r} actual={executed_evaluation_args!r}"
        )

    cwd = Path.cwd()
    supplied_model = a.model_artifact.expanduser().resolve()
    supplied_corpus = a.quality_corpus.expanduser().resolve()
    argv_model_resolved = resolve_recorded_path(argv_model, cwd)
    argv_corpus_resolved = resolve_recorded_path(argv_corpus, cwd)

    if argv_model_resolved != supplied_model:
        raise SystemExit(
            "CAPTURE: FAIL\n"
            "command model path does not match --model-artifact: "
            f"argv={argv_model_resolved} supplied={supplied_model}"
        )
    if argv_corpus_resolved != supplied_corpus:
        raise SystemExit(
            "CAPTURE: FAIL\n"
            "command corpus path does not match --quality-corpus: "
            f"argv={argv_corpus_resolved} supplied={supplied_corpus}"
        )

    model_binding = {
        "argv_value": argv_model,
        "resolved": str(supplied_model),
        "bytes": supplied_model.stat().st_size,
        "sha256": sha256_file(supplied_model),
    }
    corpus_binding = {
        "argv_value": argv_corpus,
        "resolved": str(supplied_corpus),
        "bytes": supplied_corpus.stat().st_size,
        "sha256": sha256_file(supplied_corpus),
    }

    expected_corpus_sha = str(quality_obj.get("corpus_sha256", "")).strip().lower()
    if corpus_binding["sha256"].lower() != expected_corpus_sha:
        raise SystemExit(
            "CAPTURE: FAIL\n"
            "quality manifest corpus_sha256 does not match --quality-corpus: "
            f"{expected_corpus_sha} vs {corpus_binding['sha256']}"
        )

    include_sources = []
    seen_names = set()
    for src in a.include:
        if not src.is_file():
            raise SystemExit(f"CAPTURE: FAIL\ninclude is not a file: {src}")
        if src.name in seen_names:
            raise SystemExit(f"CAPTURE: FAIL\nduplicate include basename: {src.name}")
        seen_names.add(src.name)
        include_sources.append(src)

    ensure_output_dir(a.out_dir)

    identity_out = a.out_dir / "quality-identity.json"
    stdout_out = a.out_dir / "stdout.txt"
    stderr_out = a.out_dir / "stderr.txt"
    command_out = a.out_dir / "quality-command.json"
    packet_out = a.out_dir / "PACKET.json"

    identity_out.write_bytes(quality_bytes)

    included = []
    if include_sources:
        evidence_dir = a.out_dir / "evidence"
        evidence_dir.mkdir()
        for src in include_sources:
            dst = evidence_dir / src.name
            shutil.copy2(src, dst)
            included.append(dst)

    resolved = resolve_executable(command[0])
    executable = {
        "requested": command[0],
        "resolved": str(resolved) if resolved else None,
        "bytes": None,
        "sha256": None,
    }
    if resolved and resolved.is_file():
        executable["bytes"] = resolved.stat().st_size
        executable["sha256"] = sha256_file(resolved)

    started_at = iso_now()
    launch_error = None
    try:
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=False,
        )
        exit_code = proc.returncode
        stdout = proc.stdout
        stderr = proc.stderr
    except OSError as exc:
        exit_code = None
        stdout = b""
        stderr = str(exc).encode("utf-8", errors="replace")
        launch_error = f"{type(exc).__name__}: {exc}"
    ended_at = iso_now()

    stdout_out.write_bytes(stdout)
    stderr_out.write_bytes(stderr)

    command_record = {
        "quality_capture_schema_version": 2,
        "started_at": started_at,
        "ended_at": ended_at,
        "cwd": str(cwd),
        "argv": command,
        "evaluation_args": executed_evaluation_args,
        "exit_code": exit_code,
        "launch_error": launch_error,
        "executable": executable,
        "model_artifact": model_binding,
        "quality_corpus": corpus_binding,
        "quality_identity": {
            "source": str(a.quality_manifest),
            "copied_path": "quality-identity.json",
            "bytes": len(quality_bytes),
            "sha256": sha256_bytes(quality_bytes),
        },
    }
    command_out.write_text(
        json.dumps(command_record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    files = [identity_out, stdout_out, stderr_out, command_out] + included
    packet = build_packet(a.out_dir, files)
    packet_out.write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    errors = []
    if launch_error:
        errors.append(f"command launch failed: {launch_error}")
    elif exit_code != 0:
        errors.append(f"command exited non-zero: {exit_code}")
    if not stdout and not stderr:
        errors.append("command produced no stdout or stderr evidence")

    print("QUALITY EVALUATION CAPTURE")
    print(f"out_dir={a.out_dir}")
    print(f"quality_identity={identity_out}")
    print(f"stdout={stdout_out}")
    print(f"stderr={stderr_out}")
    print(f"command_record={command_out}")
    print(f"packet={packet_out}")
    print(f"files={packet['file_count']}")
    print(f"exit_code={exit_code}")
    print("model_binding=PASS")
    print("corpus_binding=PASS")
    print("quality_identity_binding=PASS")
    print("evaluation_args_binding=PASS")

    if errors:
        print("ERRORS")
        for error in errors:
            print("- " + error)
        print("QUALITY CAPTURE: BLOCKED")
        print("Evidence was preserved for audit; do not treat this as a valid quality run.")
        raise SystemExit(2)

    print("QUALITY CAPTURE: SEALED")
    print("Next: run verify_quality_execution.py against the sealed evidence and original model/corpus.")
    print("SEALED proves evidence preservation and binding, not metric correctness or model quality.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


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


def load_json_or_jsonl(data):
    text = data.decode("utf-8").strip()
    if not text:
        raise ValueError("stdout is empty")
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, list) else [obj]
    except json.JSONDecodeError:
        rows = []
        for lineno, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"stdout line {lineno} is not JSON: {exc}") from exc
            rows.extend(obj if isinstance(obj, list) else [obj])
        if not rows:
            raise ValueError("stdout contains no JSON rows")
        return rows


def resolve_executable(value):
    candidate = Path(value)
    if candidate.is_file():
        return candidate.resolve()
    found = shutil.which(value)
    return Path(found).resolve() if found else None


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
        description="Run an explicit benchmark argv, preserve raw evidence, and seal an Experiment 61 packet."
    )
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument(
        "--include",
        action="append",
        default=[],
        type=Path,
        help="Additional evidence file to copy under out-dir/evidence/ (repeatable).",
    )
    p.add_argument("command", nargs=argparse.REMAINDER)
    a = p.parse_args()

    command = list(a.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("CAPTURE: FAIL\nmissing command after --")

    if not a.manifest.is_file():
        raise SystemExit(f"CAPTURE: FAIL\nmanifest is not a file: {a.manifest}")

    manifest_bytes = a.manifest.read_bytes()
    try:
        manifest_obj = json.loads(manifest_bytes.decode("utf-8"))
    except Exception as exc:
        raise SystemExit(f"CAPTURE: FAIL\nmanifest is not valid UTF-8 JSON: {exc}")
    if not isinstance(manifest_obj, dict):
        raise SystemExit("CAPTURE: FAIL\nmanifest must be one JSON object")

    include_sources = []
    seen_names = set()
    for src in a.include:
        if not src.is_file():
            raise SystemExit(f"CAPTURE: FAIL\ninclude is not a file: {src}")
        name = src.name
        if name in seen_names:
            raise SystemExit(f"CAPTURE: FAIL\nduplicate include basename: {name}")
        seen_names.add(name)
        include_sources.append(src)

    ensure_output_dir(a.out_dir)

    manifest_out = a.out_dir / "manifest.json"
    result_out = a.out_dir / "result.json"
    stderr_out = a.out_dir / "stderr.txt"
    command_out = a.out_dir / "command.json"
    packet_out = a.out_dir / "PACKET.json"

    manifest_out.write_bytes(manifest_bytes)

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

    result_out.write_bytes(stdout)
    stderr_out.write_bytes(stderr)

    command_record = {
        "capture_schema_version": 1,
        "started_at": started_at,
        "ended_at": ended_at,
        "cwd": str(Path.cwd()),
        "argv": command,
        "exit_code": exit_code,
        "launch_error": launch_error,
        "executable": executable,
        "manifest": {
            "source": str(a.manifest),
            "copied_path": "manifest.json",
            "bytes": len(manifest_bytes),
            "sha256": sha256_bytes(manifest_bytes),
        },
    }
    command_out.write_text(
        json.dumps(command_record, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    files = [manifest_out, result_out, stderr_out, command_out] + included
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

    try:
        rows = load_json_or_jsonl(stdout)
        if not rows:
            errors.append("stdout contains no JSON rows")
    except Exception as exc:
        errors.append(f"stdout is not valid JSON/JSONL: {exc}")

    print("REAL BENCHMARK CAPTURE")
    print(f"out_dir={a.out_dir}")
    print(f"manifest={manifest_out}")
    print(f"result={result_out}")
    print(f"stderr={stderr_out}")
    print(f"command_record={command_out}")
    print(f"packet={packet_out}")
    print(f"files={packet['file_count']}")
    print(f"exit_code={exit_code}")

    if errors:
        print("ERRORS")
        for error in errors:
            print("- " + error)
        print("CAPTURE: BLOCKED")
        print("Evidence was preserved for audit; do not ingest this run.")
        raise SystemExit(2)

    print("CAPTURE: SEALED")
    print("Next: run verify_real_intake.py with canonical IDs.")
    print("SEALED is not INTAKE: READY and not a benchmark-truth or purchase claim.")


if __name__ == "__main__":
    main()

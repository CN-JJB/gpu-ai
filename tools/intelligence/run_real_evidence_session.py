#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
PY = sys.executable
SCHEMA_VERSION = 1


def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_session(path):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"REAL SESSION: FAIL\ninvalid session JSON: {exc}")
    if not isinstance(obj, dict):
        raise SystemExit("REAL SESSION: FAIL\nsession must be one JSON object")
    return obj


def resolve_path(value, base, label, required=True):
    if value is None:
        if required:
            raise SystemExit(f"REAL SESSION: FAIL\nmissing session field {label}")
        return None
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(
            f"REAL SESSION: FAIL\nsession field {label} must be a non-empty path string"
        )
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    return path.resolve()


def require_file(path, label):
    if not path.is_file():
        raise SystemExit(f"REAL SESSION: FAIL\n{label} is not a file: {path}")


def require_string(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(
            f"REAL SESSION: FAIL\nsession field {key} must be a non-empty string"
        )
    return value.strip()


def require_argv(obj, key):
    value = obj.get(key)
    if not (
        isinstance(value, list)
        and value
        and all(isinstance(x, str) and x != "" for x in value)
    ):
        raise SystemExit(
            f"REAL SESSION: FAIL\nsession field {key} must be a non-empty JSON argv list"
        )
    return list(value)


def run_step(name, args, cwd, log_dir):
    proc = subprocess.run(
        args,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=False,
        check=False,
    )
    stdout_path = log_dir / f"{name}.stdout.txt"
    stderr_path = log_dir / f"{name}.stderr.txt"
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    return {
        "name": name,
        "argv": args,
        "returncode": proc.returncode,
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "stdout_text": proc.stdout,
        "stderr_text": proc.stderr,
    }


def public_step(step):
    return {
        "name": step["name"],
        "returncode": step["returncode"],
        "stdout": step["stdout"],
        "stderr": step["stderr"],
    }


def write_summary(path, summary):
    path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main():
    p = argparse.ArgumentParser(
        description=(
            "Run one fully specified Experiment 61 real-evidence session through "
            "benchmark capture, quality capture, PPL extraction and verify_real_intake."
        )
    )
    p.add_argument("session", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument(
        "--allow-synthetic",
        action="store_true",
        help="Test-only: allow synthetic catalog identities for the dedicated self-test.",
    )
    a = p.parse_args()

    session_path = a.session.expanduser().resolve()
    require_file(session_path, "session")
    obj = load_session(session_path)

    if obj.get("real_evidence_session_schema_version") != SCHEMA_VERSION:
        raise SystemExit(
            "REAL SESSION: FAIL\nreal_evidence_session_schema_version must be 1"
        )

    session_base = session_path.parent
    working_directory = resolve_path(
        obj.get("working_directory", "."),
        session_base,
        "working_directory",
    )
    if not working_directory.is_dir():
        raise SystemExit(
            f"REAL SESSION: FAIL\nworking_directory is not a directory: {working_directory}"
        )

    catalog = resolve_path(obj.get("catalog"), session_base, "catalog")
    manifest = resolve_path(obj.get("manifest"), session_base, "manifest")
    model = resolve_path(obj.get("model_artifact"), session_base, "model_artifact")
    profile = resolve_path(
        obj.get("hardware_profile"), session_base, "hardware_profile"
    )
    prompt = resolve_path(obj.get("prompt_manifest"), session_base, "prompt_manifest")
    corpus = resolve_path(obj.get("quality_corpus"), session_base, "quality_corpus")
    identity = resolve_path(
        obj.get("quality_identity"), session_base, "quality_identity"
    )

    if not catalog.is_dir():
        raise SystemExit(f"REAL SESSION: FAIL\ncatalog is not a directory: {catalog}")
    for label, path in (
        ("manifest", manifest),
        ("model_artifact", model),
        ("hardware_profile", profile),
        ("prompt_manifest", prompt),
        ("quality_corpus", corpus),
        ("quality_identity", identity),
    ):
        require_file(path, label)

    hardware_id = require_string(obj, "hardware_id")
    model_id = require_string(obj, "model_id")
    runtime_id = require_string(obj, "runtime_id")
    observed_at = require_string(obj, "observed_at")
    benchmark_argv = require_argv(obj, "benchmark_argv")
    quality_argv = require_argv(obj, "quality_argv")

    include_files = [profile, prompt, corpus, identity]
    include_names = [x.name for x in include_files]
    if len(include_names) != len(set(include_names)):
        raise SystemExit(
            "REAL SESSION: FAIL\nhardware/prompt/corpus/quality include basenames must be unique"
        )

    out_dir = a.out_dir.expanduser().resolve()
    if out_dir.exists():
        if not out_dir.is_dir():
            raise SystemExit(f"REAL SESSION: FAIL\nout-dir is not a directory: {out_dir}")
        if any(out_dir.iterdir()):
            raise SystemExit(f"REAL SESSION: FAIL\nout-dir is not empty: {out_dir}")
    else:
        out_dir.mkdir(parents=True)

    benchmark_dir = out_dir / "benchmark"
    quality_dir = out_dir / "quality"
    logs_dir = out_dir / "logs"
    logs_dir.mkdir()
    summary_path = out_dir / "session-summary.json"
    intake_args_path = out_dir / "intake-args.json"

    started_at = iso_now()
    steps = []

    summary = {
        "real_evidence_session_result_schema_version": 1,
        "session_source": str(session_path),
        "started_at": started_at,
        "ended_at": None,
        "status": "BLOCKED",
        "allow_synthetic": bool(a.allow_synthetic),
        "paths": {
            "benchmark_dir": str(benchmark_dir),
            "quality_dir": str(quality_dir),
            "summary": str(summary_path),
            "intake_args": str(intake_args_path),
        },
        "steps": [],
        "boundary": (
            "READY means existing intake gates accepted the captured evidence. "
            "It is not benchmark truth or a purchase recommendation."
        ),
    }

    benchmark_cmd = [
        PY,
        str(HERE / "capture_real_benchmark.py"),
        "--manifest",
        str(manifest),
        "--out-dir",
        str(benchmark_dir),
        "--model-artifact",
        str(model),
    ]
    for include in include_files:
        benchmark_cmd.extend(["--include", str(include)])
    benchmark_cmd.append("--")
    benchmark_cmd.extend(benchmark_argv)

    step = run_step("01-benchmark-capture", benchmark_cmd, working_directory, logs_dir)
    steps.append(step)
    summary["steps"] = [public_step(x) for x in steps]
    if step["returncode"] != 0:
        summary["ended_at"] = iso_now()
        summary["failure_step"] = step["name"]
        write_summary(summary_path, summary)
        print(step["stdout_text"], end="")
        print(step["stderr_text"], end="", file=sys.stderr)
        print(f"session_summary={summary_path}")
        print("REAL SESSION: BLOCKED")
        raise SystemExit(2)

    quality_cmd = [
        PY,
        str(HERE / "capture_quality_eval.py"),
        "--out-dir",
        str(quality_dir),
        "--model-artifact",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(identity),
        "--",
        *quality_argv,
    ]
    step = run_step("02-quality-capture", quality_cmd, working_directory, logs_dir)
    steps.append(step)
    summary["steps"] = [public_step(x) for x in steps]
    if step["returncode"] != 0:
        summary["ended_at"] = iso_now()
        summary["failure_step"] = step["name"]
        write_summary(summary_path, summary)
        print(step["stdout_text"], end="")
        print(step["stderr_text"], end="", file=sys.stderr)
        print(f"session_summary={summary_path}")
        print("REAL SESSION: BLOCKED")
        raise SystemExit(2)

    metric_path = quality_dir / "quality-metric.json"
    metric_cmd = [
        PY,
        str(HERE / "extract_quality_metric.py"),
        "--quality-command-record",
        str(quality_dir / "quality-command.json"),
        "--stdout",
        str(quality_dir / "stdout.txt"),
        "--stderr",
        str(quality_dir / "stderr.txt"),
        "--packet",
        str(quality_dir / "PACKET.json"),
        "--model-artifact",
        str(model),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(quality_dir / "quality-identity.json"),
        "--out",
        str(metric_path),
    ]
    step = run_step("03-quality-metric", metric_cmd, working_directory, logs_dir)
    steps.append(step)
    summary["steps"] = [public_step(x) for x in steps]
    if step["returncode"] != 0:
        summary["ended_at"] = iso_now()
        summary["failure_step"] = step["name"]
        write_summary(summary_path, summary)
        print(step["stdout_text"], end="")
        print(step["stderr_text"], end="", file=sys.stderr)
        print(f"session_summary={summary_path}")
        print("REAL SESSION: BLOCKED")
        raise SystemExit(2)

    intake_args = [
        str(catalog),
        "--manifest",
        str(benchmark_dir / "manifest.json"),
        "--result",
        str(benchmark_dir / "result.json"),
        "--packet",
        str(benchmark_dir / "PACKET.json"),
        "--hardware-id",
        hardware_id,
        "--model-id",
        model_id,
        "--runtime-id",
        runtime_id,
        "--observed-at",
        observed_at,
        "--hardware-profile",
        str(profile),
        "--prompt-manifest",
        str(prompt),
        "--quality-corpus",
        str(corpus),
        "--quality-manifest",
        str(identity),
        "--model-artifact",
        str(model),
        "--command-record",
        str(benchmark_dir / "command.json"),
        "--quality-command-record",
        str(quality_dir / "quality-command.json"),
        "--quality-stdout",
        str(quality_dir / "stdout.txt"),
        "--quality-stderr",
        str(quality_dir / "stderr.txt"),
        "--quality-packet",
        str(quality_dir / "PACKET.json"),
        "--quality-metric",
        str(metric_path),
    ]
    if a.allow_synthetic:
        intake_args.append("--allow-synthetic")

    intake_args_path.write_text(
        json.dumps(
            {
                "verify_real_intake_argv": [
                    PY,
                    str(HERE / "verify_real_intake.py"),
                    *intake_args,
                ]
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    intake_cmd = [PY, str(HERE / "verify_real_intake.py"), *intake_args]
    step = run_step("04-real-intake", intake_cmd, working_directory, logs_dir)
    steps.append(step)
    summary["steps"] = [public_step(x) for x in steps]
    summary["ended_at"] = iso_now()
    if step["returncode"] != 0:
        summary["failure_step"] = step["name"]
        write_summary(summary_path, summary)
        print(step["stdout_text"], end="")
        print(step["stderr_text"], end="", file=sys.stderr)
        print(f"intake_args={intake_args_path}")
        print(f"session_summary={summary_path}")
        print("REAL SESSION: BLOCKED")
        raise SystemExit(2)

    if "INTAKE: READY" not in step["stdout_text"]:
        summary["failure_step"] = step["name"]
        summary["failure_reason"] = "verify_real_intake returned zero without INTAKE: READY"
        write_summary(summary_path, summary)
        print(step["stdout_text"], end="")
        print(f"session_summary={summary_path}")
        print("REAL SESSION: BLOCKED")
        raise SystemExit(2)

    summary["status"] = "READY"
    summary["artifacts"] = {
        "manifest": str(benchmark_dir / "manifest.json"),
        "benchmark_result": str(benchmark_dir / "result.json"),
        "benchmark_packet": str(benchmark_dir / "PACKET.json"),
        "benchmark_command": str(benchmark_dir / "command.json"),
        "quality_identity": str(quality_dir / "quality-identity.json"),
        "quality_stdout": str(quality_dir / "stdout.txt"),
        "quality_stderr": str(quality_dir / "stderr.txt"),
        "quality_command": str(quality_dir / "quality-command.json"),
        "quality_packet": str(quality_dir / "PACKET.json"),
        "quality_metric": str(metric_path),
    }
    write_summary(summary_path, summary)

    print("REAL EVIDENCE SESSION")
    print(f"benchmark_dir={benchmark_dir}")
    print(f"quality_dir={quality_dir}")
    print(f"intake_args={intake_args_path}")
    print(f"session_summary={summary_path}")
    print("REAL SESSION: READY")
    print(
        "READY means the existing I20–I32 admission chain accepted this captured session. "
        "Review and ingest deliberately; READY is not benchmark truth or purchase approval."
    )


if __name__ == "__main__":
    main()

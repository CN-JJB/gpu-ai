#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
BUNDLE_SCHEMA_VERSION = 1
PROBE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN", "N/A", "..."}


def now_utc():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_object(path, label):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}: invalid JSON: {exc}")
    if not isinstance(obj, dict):
        raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}: expected one JSON object")
    return obj


def resolve_dir(value, base, label):
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label} must be a non-empty path string")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base / path
    path = path.resolve()
    if not path.is_dir():
        raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label} is not a directory: {path}")
    return path


def ensure_empty_dir(path):
    path = Path(path).expanduser().resolve()
    if path.exists():
        if not path.is_dir():
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\nout-dir is not a directory: {path}")
        if any(path.iterdir()):
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\nout-dir is not empty: {path}")
    else:
        path.mkdir(parents=True)
    return path


def validate_plan(plan, base):
    if plan.get("semantic_source_probe_schema_version") != SCHEMA_VERSION:
        raise SystemExit(
            "SEMANTIC SOURCE CAPTURE: FAIL\nsemantic_source_probe_schema_version must be 1"
        )
    working_directory = resolve_dir(plan.get("working_directory", "."), base, "working_directory")
    probes = plan.get("probes")
    if not isinstance(probes, list) or not probes:
        raise SystemExit("SEMANTIC SOURCE CAPTURE: FAIL\nprobes must be a non-empty JSON list")

    seen = set()
    normalized = []
    for index, probe in enumerate(probes):
        label = f"probes[{index}]"
        if not isinstance(probe, dict):
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label} must be an object")
        probe_id = probe.get("probe_id")
        if not isinstance(probe_id, str) or not PROBE_ID_RE.fullmatch(probe_id):
            raise SystemExit(
                f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.probe_id must match {PROBE_ID_RE.pattern}"
            )
        if probe_id in seen:
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\nduplicate probe_id: {probe_id}")
        seen.add(probe_id)

        purpose = probe.get("purpose")
        if not isinstance(purpose, str) or purpose.strip().upper() in PLACEHOLDERS:
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.purpose must be explicit")

        argv = probe.get("argv")
        if not (
            isinstance(argv, list)
            and argv
            and all(isinstance(x, str) and x != "" for x in argv)
        ):
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.argv must be a non-empty argv list")
        for token in argv:
            if token.strip().upper() in PLACEHOLDERS:
                raise SystemExit(
                    f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.argv contains placeholder token {token!r}"
                )

        required = probe.get("required", True)
        if not isinstance(required, bool):
            raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.required must be boolean")

        accepted = probe.get("accepted_returncodes", [0])
        if not (
            isinstance(accepted, list)
            and accepted
            and all(isinstance(x, int) and not isinstance(x, bool) for x in accepted)
        ):
            raise SystemExit(
                f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.accepted_returncodes must be a non-empty integer list"
            )
        accepted = sorted(set(accepted))

        timeout_seconds = probe.get("timeout_seconds", 30)
        if not (
            isinstance(timeout_seconds, (int, float))
            and not isinstance(timeout_seconds, bool)
            and timeout_seconds > 0
            and timeout_seconds <= 600
        ):
            raise SystemExit(
                f"SEMANTIC SOURCE CAPTURE: FAIL\n{label}.timeout_seconds must be > 0 and <= 600"
            )

        normalized.append(
            {
                "probe_id": probe_id,
                "purpose": purpose.strip(),
                "argv": list(argv),
                "required": required,
                "accepted_returncodes": accepted,
                "timeout_seconds": timeout_seconds,
            }
        )
    return working_directory, normalized


def run_probe(probe, working_directory, probes_dir):
    probe_id = probe["probe_id"]
    stdout_path = probes_dir / f"{probe_id}.stdout.txt"
    stderr_path = probes_dir / f"{probe_id}.stderr.txt"
    started_at = now_utc()
    returncode = None
    timed_out = False
    launch_error = None
    stdout = b""
    stderr = b""

    try:
        cp = subprocess.run(
            probe["argv"],
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=probe["timeout_seconds"],
            check=False,
            shell=False,
        )
        returncode = cp.returncode
        stdout = cp.stdout or b""
        stderr = cp.stderr or b""
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        launch_error = f"TimeoutExpired: exceeded {probe['timeout_seconds']} seconds"
    except (FileNotFoundError, PermissionError, OSError) as exc:
        launch_error = f"{type(exc).__name__}: {exc}"

    if launch_error:
        if stderr and not stderr.endswith(b"\n"):
            stderr += b"\n"
        stderr += (launch_error + "\n").encode("utf-8", errors="replace")

    stdout_path.write_bytes(stdout)
    stderr_path.write_bytes(stderr)
    completed_at = now_utc()

    passed = (
        launch_error is None
        and not timed_out
        and returncode in probe["accepted_returncodes"]
    )

    return {
        "probe_id": probe_id,
        "purpose": probe["purpose"],
        "required": probe["required"],
        "argv": probe["argv"],
        "working_directory": str(working_directory),
        "accepted_returncodes": probe["accepted_returncodes"],
        "timeout_seconds": probe["timeout_seconds"],
        "started_at": started_at,
        "completed_at": completed_at,
        "returncode": returncode,
        "timed_out": timed_out,
        "launch_error": launch_error,
        "passed": passed,
        "stdout_path": str(stdout_path.relative_to(probes_dir.parent)),
        "stdout_bytes": len(stdout),
        "stdout_sha256": sha256_bytes(stdout),
        "stderr_path": str(stderr_path.relative_to(probes_dir.parent)),
        "stderr_bytes": len(stderr),
        "stderr_sha256": sha256_bytes(stderr),
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Capture raw machine/runtime semantic evidence from an explicit argv probe plan. "
            "This tool never infers or rewrites Experiment 61 manifest fields."
        )
    )
    p.add_argument("plan", type=Path)
    p.add_argument("--out-dir", type=Path, required=True)
    a = p.parse_args()

    plan_path = a.plan.expanduser().resolve()
    if not plan_path.is_file():
        raise SystemExit(f"SEMANTIC SOURCE CAPTURE: FAIL\nplan is not a file: {plan_path}")
    plan = load_object(plan_path, "plan")
    working_directory, probes = validate_plan(plan, plan_path.parent)
    out_dir = ensure_empty_dir(a.out_dir)
    probes_dir = out_dir / "probes"
    probes_dir.mkdir()

    records = []
    for probe in probes:
        records.append(run_probe(probe, working_directory, probes_dir))

    blocking = [x["probe_id"] for x in records if x["required"] and not x["passed"]]
    status = "READY-FOR-SEMANTIC-REVIEW" if not blocking else "BLOCKED"
    bundle = {
        "semantic_source_bundle_schema_version": BUNDLE_SCHEMA_VERSION,
        "status": status,
        "captured_at": now_utc(),
        "source_plan": str(plan_path),
        "working_directory": str(working_directory),
        "probe_count": len(records),
        "required_failures": blocking,
        "automatic_manifest_update": "NOT-PERMITTED",
        "records": records,
    }
    (out_dir / "bundle.json").write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"semantic_source_bundle={out_dir / 'bundle.json'}")
    for rec in records:
        print(
            f"probe={rec['probe_id']} required={str(rec['required']).lower()} "
            f"passed={str(rec['passed']).lower()} returncode={rec['returncode']}"
        )
    if blocking:
        print("required_failures=" + ",".join(blocking))
        raise SystemExit("SEMANTIC SOURCE CAPTURE: BLOCKED")
    print("SEMANTIC SOURCE CAPTURE: READY-FOR-SEMANTIC-REVIEW")


if __name__ == "__main__":
    main()

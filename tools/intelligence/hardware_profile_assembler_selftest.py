#!/usr/bin/env python3
import base64
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
TOOL = HERE / "assemble_hardware_profile.py"
PY = sys.executable


def sha(data):
    return hashlib.sha256(data).hexdigest()


def run(args, expect=0):
    cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if cp.returncode != expect:
        raise AssertionError(f"expected {expect}, got {cp.returncode}\n{cp.stdout}")
    return cp.stdout


def stream_record(path, rel):
    data = path.read_bytes()
    return {
        "path": rel,
        "bytes": len(data),
        "sha256": sha(data),
    }


def write_bundle(root, *, status="READY-FOR-SEMANTIC-REVIEW", escape=False):
    probes = root / "probes"
    probes.mkdir(parents=True)
    out1 = probes / "runtime.stdout.txt"
    err1 = probes / "runtime.stderr.txt"
    out2 = probes / "optional.stdout.txt"
    err2 = probes / "optional.stderr.txt"
    out1.write_bytes(b"runtime-build-abc\n")
    err1.write_bytes(b"")
    out2.write_bytes(b"\xff\x00binary\n")
    err2.write_bytes(b"optional tool missing\n")

    s1o = stream_record(out1, "probes/runtime.stdout.txt")
    s1e = stream_record(err1, "probes/runtime.stderr.txt")
    s2o = stream_record(out2, "probes/optional.stdout.txt")
    s2e = stream_record(err2, "probes/optional.stderr.txt")

    records = [
        {
            "probe_id": "runtime",
            "purpose": "capture runtime identity",
            "required": True,
            "argv": ["llama-bench", "--version"],
            "working_directory": str(root.parent),
            "accepted_returncodes": [0],
            "timeout_seconds": 20,
            "started_at": "2026-08-28T00:00:00Z",
            "completed_at": "2026-08-28T00:00:01Z",
            "returncode": 0,
            "timed_out": False,
            "launch_error": None,
            "passed": True,
            "stdout_path": "../escape.txt" if escape else s1o["path"],
            "stdout_bytes": s1o["bytes"],
            "stdout_sha256": s1o["sha256"],
            "stderr_path": s1e["path"],
            "stderr_bytes": s1e["bytes"],
            "stderr_sha256": s1e["sha256"],
        },
        {
            "probe_id": "optional",
            "purpose": "preserve optional failed probe",
            "required": False,
            "argv": ["optional-tool", "--version"],
            "working_directory": str(root.parent),
            "accepted_returncodes": [0],
            "timeout_seconds": 20,
            "started_at": "2026-08-28T00:00:02Z",
            "completed_at": "2026-08-28T00:00:03Z",
            "returncode": None,
            "timed_out": False,
            "launch_error": "FileNotFoundError: optional-tool",
            "passed": False,
            "stdout_path": s2o["path"],
            "stdout_bytes": s2o["bytes"],
            "stdout_sha256": s2o["sha256"],
            "stderr_path": s2e["path"],
            "stderr_bytes": s2e["bytes"],
            "stderr_sha256": s2e["sha256"],
        },
    ]

    bundle = {
        "semantic_source_bundle_schema_version": 1,
        "status": status,
        "captured_at": "2026-08-28T00:00:03Z",
        "source_plan": str(root.parent / "semantic-probes.json"),
        "working_directory": str(root.parent),
        "probe_count": len(records),
        "required_failures": [] if status == "READY-FOR-SEMANTIC-REVIEW" else ["runtime"],
        "automatic_manifest_update": "NOT-PERMITTED",
        "records": records,
    }
    path = root / "bundle.json"
    path.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    return path, out1, out2


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        bundle_dir = td / "semantic-source-evidence"
        bundle, runtime_stdout, optional_stdout = write_bundle(bundle_dir)
        source_bundle_bytes = bundle.read_bytes()
        runtime_bytes = runtime_stdout.read_bytes()
        optional_bytes = optional_stdout.read_bytes()

        profile = td / "profile.txt"
        out = run([PY, str(TOOL), str(bundle), "--out", str(profile)])
        assert "HARDWARE PROFILE ASSEMBLER: READY" in out

        obj = json.loads(profile.read_text(encoding="utf-8"))
        assert obj["hardware_profile_assembler_schema_version"] == 1
        assert obj["automatic_semantic_inference"] == "NOT-PERMITTED"
        assert obj["automatic_manifest_update"] == "NOT-PERMITTED"
        assert len(obj["records"]) == 2

        by_id = {x["probe_id"]: x for x in obj["records"]}
        assert base64.b64decode(by_id["runtime"]["stdout"]["data"]) == runtime_bytes
        assert base64.b64decode(by_id["optional"]["stdout"]["data"]) == optional_bytes
        assert by_id["runtime"]["stdout"]["sha256"] == sha(runtime_bytes)
        assert by_id["optional"]["passed"] is False

        assert bundle.read_bytes() == source_bundle_bytes
        assert runtime_stdout.read_bytes() == runtime_bytes
        assert optional_stdout.read_bytes() == optional_bytes
        assert not (td / "manifest.json").exists()

        exists = run([PY, str(TOOL), str(bundle), "--out", str(profile)], expect=1)
        assert "out already exists" in exists

        tampered_dir = td / "tampered"
        tampered, tampered_stdout, _ = write_bundle(tampered_dir)
        tampered_stdout.write_bytes(b"changed after capture\n")
        tampered_profile = td / "tampered-profile.txt"
        blocked = run(
            [PY, str(TOOL), str(tampered), "--out", str(tampered_profile)],
            expect=1,
        )
        assert "stdout" in blocked and "mismatch" in blocked
        assert not tampered_profile.exists()

        escape_dir = td / "escape"
        escape_bundle, _, _ = write_bundle(escape_dir, escape=True)
        escape_profile = td / "escape-profile.txt"
        blocked = run(
            [PY, str(TOOL), str(escape_bundle), "--out", str(escape_profile)],
            expect=1,
        )
        assert "escapes the semantic bundle directory" in blocked
        assert not escape_profile.exists()

        blocked_dir = td / "blocked"
        blocked_bundle, _, _ = write_bundle(blocked_dir, status="BLOCKED")
        blocked_profile = td / "blocked-profile.txt"
        out = run(
            [PY, str(TOOL), str(blocked_bundle), "--out", str(blocked_profile)],
            expect=1,
        )
        assert "must be READY-FOR-SEMANTIC-REVIEW" in out
        assert not blocked_profile.exists()

    print("HARDWARE PROFILE ASSEMBLER SELFTEST: PASS")
    print("- READY I54 bundle streams are re-hashed before assembly")
    print("- raw stdout/stderr bytes are embedded losslessly as base64")
    print("- optional failed probes remain visible and auditable")
    print("- source bundle and raw streams are never modified")
    print("- tampering, path escape, blocked bundles, and existing output are rejected")
    print("- no device/runtime semantic inference or manifest update occurs")


if __name__ == "__main__":
    main()

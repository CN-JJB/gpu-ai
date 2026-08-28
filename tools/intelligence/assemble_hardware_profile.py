#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import re
from pathlib import Path


BUNDLE_SCHEMA_VERSION = 1
PROFILE_SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def fail(message):
    raise SystemExit(f"HARDWARE PROFILE ASSEMBLER: FAIL\n{message}")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_object(path, label):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label}: invalid JSON: {exc}")
    if not isinstance(obj, dict):
        fail(f"{label}: expected one JSON object")
    return obj


def resolve_member(bundle_dir, value, label):
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty relative path string")
    rel = Path(value)
    if rel.is_absolute():
        fail(f"{label} must be relative to the semantic bundle directory")
    root = bundle_dir.resolve()
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        fail(f"{label} escapes the semantic bundle directory: {value}")
    if not path.is_file():
        fail(f"{label} is not a file: {path}")
    return path


def require_sha(value, label):
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(f"{label} must be lowercase SHA256 hex")
    return value


def require_bytes(value, label):
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        fail(f"{label} must be a non-negative integer")
    return value


def verify_stream(bundle_dir, record, prefix):
    path = resolve_member(bundle_dir, record.get(f"{prefix}_path"), f"{prefix}_path")
    expected_bytes = require_bytes(record.get(f"{prefix}_bytes"), f"{prefix}_bytes")
    expected_sha = require_sha(record.get(f"{prefix}_sha256"), f"{prefix}_sha256")
    data = path.read_bytes()
    if len(data) != expected_bytes:
        fail(
            f"{prefix} byte count mismatch for {record.get('probe_id')}: "
            f"bundle={expected_bytes} actual={len(data)}"
        )
    actual_sha = sha256_bytes(data)
    if actual_sha != expected_sha:
        fail(
            f"{prefix} SHA256 mismatch for {record.get('probe_id')}: "
            f"bundle={expected_sha} actual={actual_sha}"
        )
    return {
        "bytes": len(data),
        "sha256": actual_sha,
        "encoding": "base64",
        "data": base64.b64encode(data).decode("ascii"),
    }


def normalize_record(bundle_dir, record, index):
    if not isinstance(record, dict):
        fail(f"records[{index}] must be an object")

    probe_id = record.get("probe_id")
    purpose = record.get("purpose")
    argv = record.get("argv")
    required = record.get("required")
    passed = record.get("passed")

    if not isinstance(probe_id, str) or not probe_id:
        fail(f"records[{index}].probe_id must be a non-empty string")
    if not isinstance(purpose, str) or not purpose:
        fail(f"records[{index}].purpose must be a non-empty string")
    if not (
        isinstance(argv, list)
        and argv
        and all(isinstance(x, str) and x != "" for x in argv)
    ):
        fail(f"records[{index}].argv must be a non-empty string list")
    if not isinstance(required, bool):
        fail(f"records[{index}].required must be boolean")
    if not isinstance(passed, bool):
        fail(f"records[{index}].passed must be boolean")

    return {
        "probe_id": probe_id,
        "purpose": purpose,
        "required": required,
        "passed": passed,
        "argv": list(argv),
        "working_directory": record.get("working_directory"),
        "accepted_returncodes": record.get("accepted_returncodes"),
        "timeout_seconds": record.get("timeout_seconds"),
        "started_at": record.get("started_at"),
        "completed_at": record.get("completed_at"),
        "returncode": record.get("returncode"),
        "timed_out": record.get("timed_out"),
        "launch_error": record.get("launch_error"),
        "stdout": verify_stream(bundle_dir, record, "stdout"),
        "stderr": verify_stream(bundle_dir, record, "stderr"),
    }


def main():
    p = argparse.ArgumentParser(
        description=(
            "Assemble a single hardware-profile artifact from a verified I54 semantic-source "
            "bundle without interpreting device/runtime semantics."
        )
    )
    p.add_argument("bundle", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    bundle_path = a.bundle.expanduser().resolve()
    if not bundle_path.is_file():
        fail(f"bundle is not a file: {bundle_path}")
    out = a.out.expanduser().resolve()
    if out.exists():
        fail(f"out already exists: {out}")
    if not out.parent.is_dir():
        fail(f"out parent is not a directory: {out.parent}")

    bundle = load_object(bundle_path, "semantic source bundle")
    if bundle.get("semantic_source_bundle_schema_version") != BUNDLE_SCHEMA_VERSION:
        fail("semantic_source_bundle_schema_version must be 1")
    if bundle.get("status") != "READY-FOR-SEMANTIC-REVIEW":
        fail(
            "semantic source bundle must be READY-FOR-SEMANTIC-REVIEW before profile assembly"
        )
    required_failures = bundle.get("required_failures")
    if required_failures != []:
        fail("semantic source bundle required_failures must be an empty list")

    records = bundle.get("records")
    if not isinstance(records, list) or not records:
        fail("semantic source bundle records must be a non-empty list")
    probe_count = bundle.get("probe_count")
    if probe_count != len(records):
        fail(
            f"semantic source bundle probe_count mismatch: declared={probe_count} actual={len(records)}"
        )

    normalized = [
        normalize_record(bundle_path.parent, record, index)
        for index, record in enumerate(records)
    ]

    profile = {
        "hardware_profile_assembler_schema_version": PROFILE_SCHEMA_VERSION,
        "source": {
            "semantic_source_bundle_schema_version": BUNDLE_SCHEMA_VERSION,
            "bundle_status": bundle.get("status"),
            "captured_at": bundle.get("captured_at"),
            "source_plan": bundle.get("source_plan"),
            "working_directory": bundle.get("working_directory"),
            "probe_count": len(normalized),
        },
        "automatic_semantic_inference": "NOT-PERMITTED",
        "automatic_manifest_update": "NOT-PERMITTED",
        "records": normalized,
    }
    payload = (
        json.dumps(profile, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    ).encode("utf-8")
    out.write_bytes(payload)

    print(f"hardware_profile={out}")
    print(f"bytes={len(payload)}")
    print(f"sha256={sha256_bytes(payload)}")
    print(f"probes={len(normalized)}")
    print("automatic_semantic_inference=NOT-PERMITTED")
    print("HARDWARE PROFILE ASSEMBLER: READY")


if __name__ == "__main__":
    main()

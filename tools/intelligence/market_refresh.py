#!/usr/bin/env python3
import argparse
import json
import os
import tempfile
from datetime import date
from pathlib import Path


def load_jsonl(path: Path):
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"REFRESH: FAIL\n{path}:{lineno}: invalid JSON: {exc}")
        if not isinstance(obj, dict):
            raise SystemExit(f"REFRESH: FAIL\n{path}:{lineno}: record must be an object")
        rows.append(obj)
    return rows


def load_object(path: Path):
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"REFRESH: FAIL\n{path}: invalid JSON: {exc}")
    if not isinstance(obj, dict):
        raise SystemExit(f"REFRESH: FAIL\n{path}: candidate must be one JSON object")
    return obj


def parse_iso(value, label):
    try:
        return date.fromisoformat(str(value))
    except Exception:
        raise SystemExit(f"REFRESH: FAIL\n{label}: invalid ISO date {value!r}")


def fail(message):
    raise SystemExit(f"REFRESH: FAIL\n{message}")


def validate_candidate(rows, old, candidate):
    old_id = str(old.get("record_id", "")).strip()
    new_id = str(candidate.get("record_id", "")).strip()

    if old.get("superseded_by"):
        fail(f"old record already superseded by {old.get('superseded_by')!r}; refresh the active tail instead")
    if old.get("record_type") != "market":
        fail("old record is not market")
    if candidate.get("record_type") != "market":
        fail("candidate record_type must be market")
    if not new_id:
        fail("candidate record_id is required")
    if new_id == old_id:
        fail("candidate record_id must differ from old record_id")

    existing_ids = {str(r.get("record_id", "")).strip() for r in rows}
    if new_id in existing_ids:
        fail(f"candidate record_id already exists: {new_id}")

    if candidate.get("hardware_id") != old.get("hardware_id"):
        fail(
            "hardware_id mismatch: "
            f"old={old.get('hardware_id')!r} candidate={candidate.get('hardware_id')!r}"
        )

    old_date = parse_iso(old.get("observed_at"), "old observed_at")
    new_date = parse_iso(candidate.get("observed_at"), "candidate observed_at")
    if new_date <= old_date:
        fail(
            "candidate observed_at must be newer than old observation: "
            f"old={old_date.isoformat()} candidate={new_date.isoformat()}"
        )

    if candidate.get("superseded_by"):
        fail("candidate must be the active tail and cannot already have superseded_by")
    if candidate.get("supersedes") not in (None, "", old_id):
        fail(
            "candidate supersedes conflicts with requested old record: "
            f"{candidate.get('supersedes')!r}"
        )

    for field in (
        "geography",
        "channel",
        "cohort",
        "condition",
        "price_state",
        "price",
        "source",
        "market_evidence_grade",
        "market_evidence_scope",
        "revalidate_after",
    ):
        if candidate.get(field) in (None, ""):
            fail(f"candidate missing required refresh field {field}")


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows)

    # Safe even when --out points at the catalog's existing market.jsonl.
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def main():
    p = argparse.ArgumentParser(
        description="Create one append-only market refresh lineage step without overwriting history."
    )
    p.add_argument("catalog", type=Path)
    p.add_argument("--old-record-id", required=True)
    p.add_argument("--candidate", required=True, type=Path, help="JSON object for the new observation")
    p.add_argument("--out", required=True, type=Path, help="Output market.jsonl; may equal the input market.jsonl")
    p.add_argument("--check-only", action="store_true", help="Validate lineage but do not write output")
    a = p.parse_args()

    market_path = a.catalog / "market.jsonl"
    rows = load_jsonl(market_path)
    by_id = {str(r.get("record_id", "")).strip(): r for r in rows}

    old = by_id.get(a.old_record_id)
    if old is None:
        fail(f"old record not found: {a.old_record_id}")

    candidate = load_object(a.candidate)
    validate_candidate(rows, old, candidate)

    new_id = str(candidate["record_id"]).strip()
    old["superseded_by"] = new_id
    candidate["supersedes"] = a.old_record_id
    rows.append(candidate)

    print("MARKET REFRESH")
    print(f"old={a.old_record_id}")
    print(f"new={new_id}")
    print(f"hardware_id={candidate.get('hardware_id')}")
    print(f"observed_at={old.get('observed_at')} -> {candidate.get('observed_at')}")
    print(f"revalidate_after={candidate.get('revalidate_after')}")
    print("lineage=old.superseded_by <-> new.supersedes")

    if a.check_only:
        print("REFRESH: READY-NO-WRITE")
        return

    write_jsonl(a.out, rows)
    print(f"out={a.out}")
    print("REFRESH: WRITTEN")


if __name__ == "__main__":
    main()

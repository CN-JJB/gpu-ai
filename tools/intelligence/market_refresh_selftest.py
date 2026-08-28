#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PYTHON = sys.executable


def run(args, expect=0):
    p = subprocess.run(args, text=True, capture_output=True)
    out = p.stdout + p.stderr
    if p.returncode != expect:
        print(out)
        raise AssertionError(f"expected return code {expect}, got {p.returncode}: {args}")
    return out


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(x, separators=(",", ":")) + "\n" for x in rows), encoding="utf-8")


def source(day):
    return {
        "evidence_class": "SECONDARY",
        "source_path": "tools/intelligence/fixtures/market-refresh-selftest-source.md",
        "observed_at": day,
        "notes": "Self-test fixture only; not production market evidence."
    }


def secondary(record_id, hardware_id, day, value, *, supersedes=None, superseded_by=None):
    r = {
        "schema_version": 1,
        "record_type": "market",
        "record_id": record_id,
        "hardware_id": hardware_id,
        "geography": "CN",
        "channel": "secondary-summary",
        "cohort": "used-consumer",
        "condition": "working-unverified",
        "price_state": "SECONDARY_REPORTED",
        "price": {"currency": "CNY", "value": value},
        "observed_at": day,
        "revalidate_after": "2026-09-04",
        "source": source(day),
        "report": {
            "reported_market": "self-test secondary summary",
            "direct_listing_capture": False,
            "confirmed_sale": False,
            "sample_size": None
        },
        "market_evidence_grade": "M1",
        "market_evidence_scope": "self-test secondary reported signal; not a direct listing sample or confirmed sale"
    }
    if supersedes:
        r["supersedes"] = supersedes
    if superseded_by:
        r["superseded_by"] = superseded_by
    return r


def build_catalog(path):
    path.mkdir()
    hw3090 = "hw:nvidia:geforce-rtx-3090:24g"
    hwa770 = "hw:intel:arc-a770:16g"
    write_jsonl(path / "hardware.jsonl", [
        {
            "schema_version": 1,
            "record_type": "hardware",
            "record_id": hw3090,
            "hardware_id": hw3090,
            "canonical_name": "NVIDIA GeForce RTX 3090 24GB",
            "vendor": "NVIDIA",
            "accelerator_kind": "GPU",
            "memory_gib": 24,
            "source": {"evidence_class": "OFFICIAL", "source_path": "fixture", "observed_at": "2026-08-28"}
        },
        {
            "schema_version": 1,
            "record_type": "hardware",
            "record_id": hwa770,
            "hardware_id": hwa770,
            "canonical_name": "Intel Arc A770 16GB",
            "vendor": "Intel",
            "accelerator_kind": "GPU",
            "memory_gib": 16,
            "source": {"evidence_class": "OFFICIAL", "source_path": "fixture", "observed_at": "2026-08-28"}
        }
    ])
    old_3090 = "market:cn:rtx3090:secondary:2026-08-22"
    old_a770 = "market:cn:a770:secondary:2026-08-21"
    new_a770 = "market:cn:a770:secondary:2026-08-25"
    write_jsonl(path / "market.jsonl", [
        secondary(old_3090, hw3090, "2026-08-22", 7400),
        secondary(old_a770, hwa770, "2026-08-21", 1450, superseded_by=new_a770),
        secondary(new_a770, hwa770, "2026-08-25", 1400, supersedes=old_a770),
    ])
    return old_3090, old_a770, hw3090, hwa770


def read_market(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        catalog = td / "catalog"
        old_id, old_a770, hw3090, hwa770 = build_catalog(catalog)
        original_count = len(read_market(catalog / "market.jsonl"))

        candidate = td / "candidate.json"
        candidate.write_text(json.dumps(secondary(
            "market:cn:rtx3090:secondary:2026-08-28-test",
            hw3090,
            "2026-08-28",
            7350,
        )), encoding="utf-8")

        out = run([
            PYTHON, str(HERE / "market_refresh.py"), str(catalog),
            "--old-record-id", old_id,
            "--candidate", str(candidate),
            "--out", str(catalog / "market.jsonl"),
        ])
        assert "REFRESH: WRITTEN" in out

        rows = read_market(catalog / "market.jsonl")
        by_id = {r["record_id"]: r for r in rows}
        new_id = "market:cn:rtx3090:secondary:2026-08-28-test"
        assert by_id[old_id]["superseded_by"] == new_id
        assert by_id[new_id]["supersedes"] == old_id
        assert len(rows) == original_count + 1

        validator = HERE / "validate_catalog.py"
        if validator.exists():
            out = run([PYTHON, str(validator), str(catalog), "--as-of", "2026-08-28"])
            assert "VALIDATION: PASS" in out

        # A historical row that already has a successor cannot fork into a second active tail.
        candidate.write_text(json.dumps(secondary("market:test:a770:fork", hwa770, "2026-08-28", 1390)), encoding="utf-8")
        out = run([
            PYTHON, str(HERE / "market_refresh.py"), str(catalog),
            "--old-record-id", old_a770,
            "--candidate", str(candidate),
            "--out", str(td / "unused.jsonl"),
        ], expect=1)
        assert "already superseded" in out

        # Cross-hardware lineage is rejected before writing.
        fresh_catalog = td / "catalog-cross"
        old_id2, _, _, hwa7702 = build_catalog(fresh_catalog)
        candidate.write_text(json.dumps(secondary("market:test:wrong-hardware", hwa7702, "2026-08-28", 1400)), encoding="utf-8")
        out = run([
            PYTHON, str(HERE / "market_refresh.py"), str(fresh_catalog),
            "--old-record-id", old_id2,
            "--candidate", str(candidate),
            "--out", str(td / "unused2.jsonl"),
        ], expect=1)
        assert "hardware_id mismatch" in out

        # Equal/older timestamps cannot supersede a newer observation.
        candidate.write_text(json.dumps(secondary("market:test:old-date", hw3090, "2026-08-22", 7350)), encoding="utf-8")
        out = run([
            PYTHON, str(HERE / "market_refresh.py"), str(fresh_catalog),
            "--old-record-id", old_id2,
            "--candidate", str(candidate),
            "--out", str(td / "unused3.jsonl"),
        ], expect=1)
        assert "must be newer" in out

    print("MARKET REFRESH SELFTEST: PASS")
    print("- helper creates reciprocal append-only lineage and preserves the old record")
    print("- generated catalog passes validate_catalog.py when run in the repository")
    print("- already-superseded tails, cross-hardware links and non-newer dates are rejected")


if __name__ == "__main__":
    main()

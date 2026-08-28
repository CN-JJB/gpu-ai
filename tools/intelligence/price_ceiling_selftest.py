#!/usr/bin/env python3
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


def write_jsonl(path, rows):
    path.write_text(
        "".join(
            json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def policy(path, policy_id, market_record_id, hardware_id, ceiling, band):
    path.write_text(
        json.dumps(
            {
                "price_ceiling_policy_schema_version": 1,
                "policy_id": policy_id,
                "market_record_id": market_record_id,
                "hardware_id": hardware_id,
                "max_sticker": {"currency": "USD", "value": ceiling},
                "watch_band_pct": band,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        catalog = td / "catalog"
        catalog.mkdir()
        hardware_id = "hw:fixture:i48"
        market_id = "market:synthetic:i48"
        record = {
            "schema_version": 1,
            "record_type": "market",
            "record_id": market_id,
            "hardware_id": hardware_id,
            "geography": "TEST",
            "channel": "synthetic",
            "cohort": "synthetic",
            "condition": "synthetic",
            "price_state": "MEDIAN_ASK",
            "price": {"currency": "USD", "value": 950},
            "observed_at": "2026-08-28",
            "revalidate_after": "2026-09-04",
            "market_evidence_grade": "M0",
            "market_evidence_scope": "synthetic I48 arithmetic fixture",
            "synthetic": True,
        }
        write_jsonl(catalog / "market.jsonl", [record])

        within_policy = td / "within-policy.json"
        policy(within_policy, "i48-within", market_id, hardware_id, 1000, 10)
        within = td / "within.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_price_ceiling.py"),
                str(catalog),
                "--policy",
                str(within_policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
                "--out",
                str(within),
            ]
        )
        assert "PRICE CEILING: WITHIN-CEILING" in out
        obj = json.loads(within.read_text(encoding="utf-8"))
        assert obj["synthetic_input"] is True
        assert obj["market"]["market_gate"] == "SYNTHETIC-TEST-ONLY"
        assert obj["decision"] == "WITHIN-CEILING"

        out = run(
            [
                PY,
                str(HERE / "verify_price_ceiling.py"),
                str(catalog),
                "--result",
                str(within),
                "--policy",
                str(within_policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
            ]
        )
        assert "PRICE CEILING ARTIFACT: PASS" in out

        watch_policy = td / "watch-policy.json"
        policy(watch_policy, "i48-watch", market_id, hardware_id, 900, 10)
        watch = td / "watch.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_price_ceiling.py"),
                str(catalog),
                "--policy",
                str(watch_policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
                "--out",
                str(watch),
            ]
        )
        assert "PRICE CEILING: WATCH-BAND" in out

        above_policy = td / "above-policy.json"
        policy(above_policy, "i48-above", market_id, hardware_id, 800, 10)
        above = td / "above.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_price_ceiling.py"),
                str(catalog),
                "--policy",
                str(above_policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
                "--out",
                str(above),
            ]
        )
        assert "PRICE CEILING: ABOVE-BAND" in out

        tampered = td / "tampered.json"
        bad = json.loads(above.read_text(encoding="utf-8"))
        bad["decision"] = "WITHIN-CEILING"
        tampered.write_text(json.dumps(bad, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        out = run(
            [
                PY,
                str(HERE / "verify_price_ceiling.py"),
                str(catalog),
                "--result",
                str(tampered),
                "--policy",
                str(above_policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
            ],
            expect=2,
        )
        assert "does not exactly match independently rebuilt" in out

        blocked = td / "blocked.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_price_ceiling.py"),
                str(catalog),
                "--policy",
                str(within_policy),
                "--as-of",
                "2026-08-28",
                "--out",
                str(blocked),
            ],
            expect=2,
        )
        assert "synthetic market record requires explicit --allow-synthetic" in out
        assert not blocked.exists()

    print("PRICE CEILING SELFTEST: PASS")
    print("- explicit max sticker and watch band reproduce Experiment 38 price bands")
    print("- output is neutral WITHIN-CEILING/WATCH-BAND/ABOVE-BAND, not BUY")
    print("- edited price result is blocked")
    print("- synthetic market evidence requires explicit test allowance")
    print("- no FX conversion or automatic fair-price inference is performed")


if __name__ == "__main__":
    main()

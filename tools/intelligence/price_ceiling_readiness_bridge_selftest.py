#!/usr/bin/env python3
import json
import sys
import tempfile
from pathlib import Path

from joint_tradeoff_selftest import run
from unified_tradeoff_route_selftest import build_model_fixture


HERE = Path(__file__).resolve().parent
PY = sys.executable


def write_jsonl(path, rows):
    path.write_text(
        "".join(
            json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        fixture = build_model_fixture(td)
        candidate = json.loads(fixture["cb"].read_text(encoding="utf-8"))

        catalog = td / "catalog"
        catalog.mkdir()
        write_jsonl(catalog / "compatibility.jsonl", [])
        market_id = "market:synthetic:i49"
        market = {
            "schema_version": 1,
            "record_type": "market",
            "record_id": market_id,
            "hardware_id": candidate["hardware_id"],
            "geography": "TEST",
            "channel": "synthetic",
            "cohort": "synthetic",
            "condition": "synthetic",
            "price_state": "MEDIAN_ASK",
            "price": {"currency": "USD", "value": 950},
            "observed_at": "2026-08-28",
            "revalidate_after": "2026-09-04",
            "market_evidence_grade": "M0",
            "market_evidence_scope": "synthetic I49 fixture",
            "synthetic": True,
        }
        write_jsonl(catalog / "market.jsonl", [market])

        policy = td / "price-policy.json"
        policy.write_text(
            json.dumps(
                {
                    "price_ceiling_policy_schema_version": 1,
                    "policy_id": "synthetic-i49",
                    "market_record_id": market_id,
                    "hardware_id": candidate["hardware_id"],
                    "max_sticker": {"currency": "USD", "value": 1000},
                    "watch_band_pct": 10,
                },
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )

        price_result = td / "price-result.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_price_ceiling.py"),
                str(catalog),
                "--policy",
                str(policy),
                "--as-of",
                "2026-08-28",
                "--allow-synthetic",
                "--out",
                str(price_result),
            ]
        )
        assert "PRICE CEILING: WITHIN-CEILING" in out

        report = td / "report.json"
        out = run(
            [
                PY,
                str(HERE / "decision_evidence_gap.py"),
                str(catalog),
                "--joint-tradeoff",
                str(fixture["joint"]),
                "--baseline-manifest",
                str(fixture["bm"]),
                "--candidate-manifest",
                str(fixture["cm"]),
                "--baseline-benchmark",
                str(fixture["bb"]),
                "--candidate-benchmark",
                str(fixture["cb"]),
                "--quality-comparison",
                str(fixture["comparison"]),
                "--baseline-quality-dir",
                str(fixture["bq"]),
                "--candidate-quality-dir",
                str(fixture["cq"]),
                "--baseline-model-artifact",
                str(fixture["baseline_model"]),
                "--candidate-model-artifact",
                str(fixture["candidate_model"]),
                "--quality-corpus",
                str(fixture["corpus"]),
                "--market-record-id",
                market_id,
                "--price-ceiling-result",
                str(price_result),
                "--price-ceiling-policy",
                str(policy),
                "--as-of",
                "2026-08-28",
                "--out",
                str(report),
            ]
        )
        obj = json.loads(report.read_text(encoding="utf-8"))
        pc = obj["components"]["price_ceiling"]
        assert pc["status"] == "BLOCKED"
        assert pc["decision"] == "WITHIN-CEILING"
        assert "synthetic" in pc["reason"]
        assert obj["decision_readiness"] == "BLOCKED"
        assert "AUTOMATIC PURCHASE DECISION: NOT-PERMITTED" in out

        other_policy = td / "other-policy.json"
        other_policy.write_text(
            json.dumps(
                {
                    "price_ceiling_policy_schema_version": 1,
                    "policy_id": "synthetic-i49-other",
                    "market_record_id": market_id,
                    "hardware_id": candidate["hardware_id"],
                    "max_sticker": {"currency": "USD", "value": 1000},
                    "watch_band_pct": 10,
                },
                indent=2,
                sort_keys=True,
            ) + "\n",
            encoding="utf-8",
        )
        mismatched = json.loads(price_result.read_text(encoding="utf-8"))
        mismatched["market_record_id"] = "market:other"
        mismatch_result = td / "mismatch-result.json"
        mismatch_result.write_text(json.dumps(mismatched,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        report2=td/"report2.json"
        out=run([
            PY,str(HERE/"decision_evidence_gap.py"),str(catalog),
            "--joint-tradeoff",str(fixture["joint"]),
            "--baseline-manifest",str(fixture["bm"]),
            "--candidate-manifest",str(fixture["cm"]),
            "--baseline-benchmark",str(fixture["bb"]),
            "--candidate-benchmark",str(fixture["cb"]),
            "--quality-comparison",str(fixture["comparison"]),
            "--baseline-quality-dir",str(fixture["bq"]),
            "--candidate-quality-dir",str(fixture["cq"]),
            "--baseline-model-artifact",str(fixture["baseline_model"]),
            "--candidate-model-artifact",str(fixture["candidate_model"]),
            "--quality-corpus",str(fixture["corpus"]),
            "--market-record-id",market_id,
            "--price-ceiling-result",str(mismatch_result),
            "--price-ceiling-policy",str(other_policy),
            "--as-of","2026-08-28",
            "--out",str(report2)
        ])
        obj2=json.loads(report2.read_text(encoding="utf-8"))
        assert obj2["components"]["price_ceiling"]["status"]=="BLOCKED"
        assert "does not exactly match independently rebuilt" in obj2["components"]["price_ceiling"]["reason"]

    print("PRICE CEILING READINESS BRIDGE SELFTEST: PASS")
    print("- I43 independently verifies I48 price evidence")
    print("- synthetic WITHIN-CEILING remains blocked as production evidence")
    print("- price result must reproduce the selected market record and explicit policy")
    print("- no neutral price band is converted into an automatic BUY")


if __name__ == "__main__":
    main()

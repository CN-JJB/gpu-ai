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

        catalog = td / "catalog"
        catalog.mkdir()
        write_jsonl(catalog / "compatibility.jsonl", [])
        write_jsonl(catalog / "market.jsonl", [])

        policy = td / "policy.json"
        policy.write_text(
            json.dumps(
                {
                    "performance_target_policy_schema_version": 1,
                    "policy_id": "synthetic-i47-pass",
                    "comparison_id": "fixture-i42-model",
                    "requirements": {
                        "min_pp_tok_s": 1100,
                        "min_tg_tok_s": 55,
                        "max_candidate_ppl": 11,
                        "max_ppl_percent_change": 10,
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        result = td / "performance-target-result.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_performance_target.py"),
                "--policy",
                str(policy),
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
                "--out",
                str(result),
            ]
        )
        assert "PERFORMANCE TARGET: PASS" in out

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
                "missing-market",
                "--performance-target-result",
                str(result),
                "--performance-target-policy",
                str(policy),
                "--as-of",
                "2026-08-28",
                "--out",
                str(report),
            ]
        )

        obj = json.loads(report.read_text(encoding="utf-8"))
        component = obj["components"]["performance_target"]
        assert component["status"] == "BLOCKED"
        assert component["decision"] == "PASS"
        assert "synthetic" in component["reason"]
        assert obj["decision_readiness"] == "BLOCKED"
        assert "AUTOMATIC PURCHASE DECISION: NOT-PERMITTED" in out

        tampered = td / "tampered-result.json"
        bad = json.loads(result.read_text(encoding="utf-8"))
        bad["actual"]["tg_tok_s"] = 9999.0
        tampered.write_text(
            json.dumps(bad, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        report2 = td / "report2.json"
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
                "missing-market",
                "--performance-target-result",
                str(tampered),
                "--performance-target-policy",
                str(policy),
                "--as-of",
                "2026-08-28",
                "--out",
                str(report2),
            ]
        )
        obj2 = json.loads(report2.read_text(encoding="utf-8"))
        assert obj2["components"]["performance_target"]["status"] == "BLOCKED"
        assert "does not exactly match independently rebuilt" in obj2["components"]["performance_target"]["reason"]

    print("PERFORMANCE TARGET READINESS BRIDGE SELFTEST: PASS")
    print("- I43 independently verifies I46 target evidence")
    print("- synthetic PASS remains blocked as production performance evidence")
    print("- tampered target artifact remains blocked")
    print("- performance target can no longer be satisfied by a descriptive tradeoff alone")


if __name__ == "__main__":
    main()

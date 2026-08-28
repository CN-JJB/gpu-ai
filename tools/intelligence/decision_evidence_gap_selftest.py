#!/usr/bin/env python3
import json
import sys
import tempfile
from pathlib import Path

from unified_tradeoff_route_selftest import build_model_fixture
from joint_tradeoff_selftest import run


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

        candidate_benchmark = json.loads(
            fixture["cb"].read_text(encoding="utf-8")
        )

        compatibility = {
            "schema_version": 1,
            "record_type": "compatibility",
            "record_id": "compat:synthetic:i43",
            "hardware_id": candidate_benchmark["hardware_id"],
            "model_id": candidate_benchmark["model_id"],
            "runtime_id": candidate_benchmark["runtime_id"],
            "backend": candidate_benchmark["runtime"]["backend"],
            "status": "MEASURED_SUPPORTED",
            "observed_at": "2026-08-28",
            "revalidate_after": "2026-09-04",
            "scope": {
                "artifact_sha256": candidate_benchmark["artifact"]["sha256"],
                "runtime_build": candidate_benchmark["runtime"]["build_identity"],
            },
            "source": {"evidence_class": "SYNTHETIC"},
            "synthetic": True,
        }
        write_jsonl(catalog / "compatibility.jsonl", [compatibility])

        market = {
            "schema_version": 1,
            "record_type": "market",
            "record_id": "market:synthetic:i43",
            "hardware_id": candidate_benchmark["hardware_id"],
            "observed_at": "2026-08-28",
            "revalidate_after": "2026-09-04",
            "price_state": "MEDIAN_ASK",
            "market_evidence_grade": "M0",
            "market_evidence_scope": "synthetic readiness fixture",
            "price": {"amount": 1, "currency": "USD"},
            "synthetic": True,
        }
        write_jsonl(catalog / "market.jsonl", [market])

        feasibility = td / "feasibility.json"
        feasibility.write_text(
            json.dumps(
                {
                    "case_id": "synthetic-i43",
                    "model": {"required_runtime_vram_gib": 1},
                    "gpu": {
                        "runtime_available_vram_gib": 2,
                        "multi_gpu": False,
                    },
                    "software": {"target_backend_supported": True},
                    "host": {
                        "required_ram_gib": 1,
                        "available_ram_gib": 2,
                    },
                    "storage": {
                        "required_free_gib": 1,
                        "available_free_gib": 2,
                    },
                    "psu": {
                        "capacity_policy_pass": True,
                        "cable_compatibility_confirmed": True,
                    },
                    "thermal": {"sustained_target_pass": True},
                    "serving": {"required": False, "slo_pass": None},
                    "network": {
                        "wider_than_loopback": False,
                        "controls_pass": None,
                    },
                    "budget": {"max_total": 2, "estimated_total": 1},
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

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
                "market:synthetic:i43",
                "--feasibility-case",
                str(feasibility),
                "--as-of",
                "2026-08-28",
                "--out",
                str(report),
            ]
        )

        assert "DECISION READINESS: BLOCKED" in out
        assert "AUTOMATIC PURCHASE DECISION: NOT-PERMITTED" in out

        obj = json.loads(report.read_text(encoding="utf-8"))
        assert obj["components"]["verified_tradeoff"]["status"] == "PASS"
        assert obj["components"]["real_benchmark_provenance"]["status"] == "BLOCKED"
        assert obj["components"]["exact_measured_compatibility"]["status"] == "BLOCKED"
        assert obj["components"]["current_market_evidence"]["status"] == "BLOCKED"
        assert obj["components"]["whole_machine_feasibility"]["status"] == "PASS"
        assert obj["components"]["condition_acceptance"]["status"] == "BLOCKED"
        assert obj["components"]["performance_target"]["status"] == "BLOCKED"
        assert obj["components"]["price_ceiling"]["status"] == "BLOCKED"
        assert obj["automatic_purchase_decision"] == "NOT-PERMITTED"

    print("DECISION EVIDENCE GAP SELFTEST: PASS")
    print("- verified synthetic tradeoff does not become real benchmark evidence")
    print("- synthetic compatibility/market records cannot satisfy production readiness")
    print("- Experiment 90 ACCEPT can satisfy only the feasibility component")
    print("- condition, target-performance policy and price ceiling remain explicit blockers")
    print("- no BUY/WATCH/REJECT result is emitted")


if __name__ == "__main__":
    main()

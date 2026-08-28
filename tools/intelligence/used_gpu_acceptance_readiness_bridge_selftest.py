#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from unified_tradeoff_route_selftest import build_model_fixture
from joint_tradeoff_selftest import run


HERE = Path(__file__).resolve().parent
PY = sys.executable


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_jsonl(path, rows):
    path.write_text(
        "".join(
            json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
            for row in rows
        ),
        encoding="utf-8",
    )


def write_packet(root, files):
    entries = []
    for path in files:
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "sha256": sha(data),
            }
        )
    packet = root / "acceptance-PACKET.json"
    packet.write_text(
        json.dumps(
            {
                "packet_schema_version": 1,
                "file_count": len(entries),
                "files": entries,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return packet


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        fixture = build_model_fixture(td)
        candidate = json.loads(fixture["cb"].read_text(encoding="utf-8"))

        catalog = td / "catalog"
        catalog.mkdir()
        write_jsonl(catalog / "compatibility.jsonl", [])
        write_jsonl(catalog / "market.jsonl", [])

        feasibility = td / "feasibility.json"
        feasibility.write_text(
            json.dumps(
                {
                    "case_id": "synthetic-i45",
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

        case = td / "acceptance-case.json"
        case.write_text(
            json.dumps(
                {
                    "acceptance_case_schema_version": 1,
                    "case_id": "synthetic-i45",
                    "hardware_id": candidate["hardware_id"],
                    "synthetic": True,
                    "claim": {"vram_gib": 24},
                    "observed": {
                        "vram_gib": 24,
                        "driver_recognized": True,
                        "target_runtime_recognized": True,
                    },
                    "workload": {
                        "sustained_completed": True,
                        "tg_first": 50.0,
                        "tg_last": 49.0,
                    },
                    "errors": {"uncorrectable": None},
                    "pcie": {
                        "max_width": 16,
                        "current_width": 16,
                        "expected_platform_width": 16,
                        "observed_under_load": True,
                    },
                    "physical": {
                        "display_required": False,
                        "display_outputs_tested": False,
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        raw = td / "acceptance-raw.txt"
        raw.write_text("SYNTHETIC I45 ACCEPTANCE RAW FIXTURE\n", encoding="utf-8")
        packet = write_packet(td, [case, raw])
        acceptance = td / "acceptance.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_used_gpu_acceptance.py"),
                "--case",
                str(case),
                "--packet",
                str(packet),
                "--out",
                str(acceptance),
            ]
        )
        assert "decision=ACCEPT" in out

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
                "--feasibility-case",
                str(feasibility),
                "--used-gpu-acceptance",
                str(acceptance),
                "--used-gpu-acceptance-case",
                str(case),
                "--used-gpu-acceptance-packet",
                str(packet),
                "--as-of",
                "2026-08-28",
                "--out",
                str(report),
            ]
        )

        obj = json.loads(report.read_text(encoding="utf-8"))
        assert obj["components"]["used_gpu_acceptance"]["status"] == "BLOCKED"
        assert "synthetic" in obj["components"]["used_gpu_acceptance"]["reason"]
        assert obj["components"]["used_gpu_acceptance"]["decision"] == "ACCEPT"
        assert obj["components"]["condition_acceptance"]["status"] == "BLOCKED"
        assert "no I50 condition evidence artifact supplied" in obj["components"]["condition_acceptance"]["reason"]
        assert obj["decision_readiness"] == "BLOCKED"
        assert "AUTOMATIC PURCHASE DECISION: NOT-PERMITTED" in out

    print("USED GPU ACCEPTANCE READINESS BRIDGE SELFTEST: PASS")
    print("- I43 independently verifies the I44 acceptance artifact")
    print("- synthetic ACCEPT remains blocked as production condition evidence")
    print("- ACCEPT does not satisfy the separate Experiment 38 C3/C4 gate")
    print("- no C-grade mapping is inferred")


if __name__ == "__main__":
    main()

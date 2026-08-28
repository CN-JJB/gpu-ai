#!/usr/bin/env python3
import hashlib
import json
import sys
import tempfile
from pathlib import Path

from joint_tradeoff_selftest import run
from unified_tradeoff_route_selftest import build_model_fixture


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

        case = td / "acceptance-case.json"
        case.write_text(
            json.dumps(
                {
                    "acceptance_case_schema_version": 1,
                    "case_id": "synthetic-i51",
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
            ) + "\n",
            encoding="utf-8",
        )
        raw = td / "raw.txt"
        raw.write_text("SYNTHETIC I51 CONDITION FIXTURE\n", encoding="utf-8")
        packet = write_packet(td, [case, raw])

        acceptance = td / "acceptance.json"
        out = run([
            PY,str(HERE/"evaluate_used_gpu_acceptance.py"),
            "--case",str(case),"--packet",str(packet),"--out",str(acceptance)
        ])
        assert "decision=ACCEPT" in out

        condition = td / "condition.json"
        out = run([
            PY,str(HERE/"derive_condition_evidence_grade.py"),
            "--acceptance",str(acceptance),
            "--case",str(case),
            "--packet",str(packet),
            "--out",str(condition)
        ])
        assert "grade=C0" in out

        report = td / "report.json"
        out = run([
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
            "--market-record-id","missing-market",
            "--used-gpu-acceptance",str(acceptance),
            "--used-gpu-acceptance-case",str(case),
            "--used-gpu-acceptance-packet",str(packet),
            "--condition-evidence-result",str(condition),
            "--as-of","2026-08-28",
            "--out",str(report)
        ])

        obj=json.loads(report.read_text(encoding="utf-8"))
        cond=obj["components"]["condition_acceptance"]
        used=obj["components"]["used_gpu_acceptance"]
        assert cond["status"]=="BLOCKED"
        assert cond["grade"]=="C0"
        assert cond["acceptance_decision"]=="ACCEPT"
        assert "synthetic" in cond["reason"]
        assert used["status"]=="BLOCKED"
        assert obj["decision_readiness"]=="BLOCKED"
        assert "AUTOMATIC PURCHASE DECISION: NOT-PERMITTED" in out

        tampered = td / "tampered-condition.json"
        bad=json.loads(condition.read_text(encoding="utf-8"))
        bad["evidence_grade"]="C3"
        tampered.write_text(json.dumps(bad,indent=2,sort_keys=True)+"\n",encoding="utf-8")
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
            "--market-record-id","missing-market",
            "--used-gpu-acceptance",str(acceptance),
            "--used-gpu-acceptance-case",str(case),
            "--used-gpu-acceptance-packet",str(packet),
            "--condition-evidence-result",str(tampered),
            "--as-of","2026-08-28",
            "--out",str(report2)
        ])
        obj2=json.loads(report2.read_text(encoding="utf-8"))
        assert obj2["components"]["condition_acceptance"]["status"]=="BLOCKED"
        assert "does not exactly match independently rebuilt" in obj2["components"]["condition_acceptance"]["reason"]

    print("CONDITION EVIDENCE READINESS BRIDGE SELFTEST: PASS")
    print("- I43 independently verifies I50 condition provenance")
    print("- synthetic C0 remains blocked")
    print("- ACCEPT remains separate from C-grade provenance")
    print("- edited C0 -> C3 evidence is blocked")
    print("- real C3/C4 provenance can satisfy only the condition-evidence-strength component")


if __name__ == "__main__":
    main()

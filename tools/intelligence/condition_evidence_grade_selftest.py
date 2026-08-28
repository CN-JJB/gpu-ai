#!/usr/bin/env python3
import hashlib
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


def sha(data):
    return hashlib.sha256(data).hexdigest()


def packet(root, files):
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
    out = root / "PACKET.json"
    out.write_text(
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
    return out


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        case = td / "case.json"
        case.write_text(
            json.dumps(
                {
                    "acceptance_case_schema_version": 1,
                    "case_id": "synthetic-i50",
                    "hardware_id": "hw:fixture:i50",
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
        raw = td / "raw.txt"
        raw.write_text("SYNTHETIC I50 RAW FIXTURE\n", encoding="utf-8")
        pkt = packet(td, [case, raw])

        acceptance = td / "acceptance.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_used_gpu_acceptance.py"),
                "--case",
                str(case),
                "--packet",
                str(pkt),
                "--out",
                str(acceptance),
            ]
        )
        assert "decision=ACCEPT" in out

        grade = td / "condition-grade.json"
        out = run(
            [
                PY,
                str(HERE / "derive_condition_evidence_grade.py"),
                "--acceptance",
                str(acceptance),
                "--case",
                str(case),
                "--packet",
                str(pkt),
                "--out",
                str(grade),
            ]
        )
        assert "grade=C0" in out
        assert "acceptance_decision=ACCEPT" in out
        obj = json.loads(grade.read_text(encoding="utf-8"))
        assert obj["synthetic_input"] is True
        assert obj["evidence_grade"] == "C0"
        assert obj["acceptance_decision"] == "ACCEPT"
        assert obj["health_decision_is_separate"] is True
        assert obj["c4_status"] == "RESERVED-NOT-EMITTED"

        out = run(
            [
                PY,
                str(HERE / "verify_condition_evidence_grade.py"),
                "--result",
                str(grade),
                "--acceptance",
                str(acceptance),
                "--case",
                str(case),
                "--packet",
                str(pkt),
            ]
        )
        assert "CONDITION EVIDENCE ARTIFACT: PASS" in out

        tampered = td / "tampered.json"
        bad = json.loads(grade.read_text(encoding="utf-8"))
        bad["evidence_grade"] = "C3"
        tampered.write_text(
            json.dumps(bad, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        out = run(
            [
                PY,
                str(HERE / "verify_condition_evidence_grade.py"),
                "--result",
                str(tampered),
                "--acceptance",
                str(acceptance),
                "--case",
                str(case),
                "--packet",
                str(pkt),
            ],
            expect=2,
        )
        assert "does not exactly match independently rebuilt" in out

    print("CONDITION EVIDENCE GRADE SELFTEST: PASS")
    print("- synthetic I44 evidence remains effective C0, never production C3")
    print("- ACCEPT is kept separate from evidence provenance grade")
    print("- edited C0 -> C3 artifacts are blocked")
    print("- C4 is reserved and not emitted by I50")
    print("- real independently reproducible I44 evidence is the defined C3 production path")


if __name__ == "__main__":
    main()

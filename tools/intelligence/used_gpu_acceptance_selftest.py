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
    packet = root / "PACKET.json"
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


def case(case_id, hardware_id, synthetic, vram_claim=24, vram_seen=24):
    return {
        "acceptance_case_schema_version": 1,
        "case_id": case_id,
        "hardware_id": hardware_id,
        "synthetic": synthetic,
        "claim": {"vram_gib": vram_claim},
        "observed": {
            "vram_gib": vram_seen,
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
    }


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        healthy = td / "healthy.json"
        healthy.write_text(
            json.dumps(
                case("synthetic-healthy", "hw:fixture:i44", True),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        raw = td / "raw-evidence.txt"
        raw.write_text(
            "SYNTHETIC I44 RAW EVIDENCE FIXTURE ONLY\n",
            encoding="utf-8",
        )
        packet = write_packet(td, [healthy, raw])

        acceptance = td / "acceptance.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_used_gpu_acceptance.py"),
                "--case",
                str(healthy),
                "--packet",
                str(packet),
                "--out",
                str(acceptance),
            ]
        )
        assert "decision=ACCEPT" in out
        assert "condition_grade_mapping=UNDEFINED" in out
        obj = json.loads(acceptance.read_text(encoding="utf-8"))
        assert obj["decision"] == "ACCEPT"
        assert obj["synthetic"] is True
        assert obj["condition_grade_mapping"] == "UNDEFINED"
        assert any("unsupported/unknown" in x for x in obj["info"])

        out = run(
            [
                PY,
                str(HERE / "verify_used_gpu_acceptance.py"),
                "--acceptance",
                str(acceptance),
                "--case",
                str(healthy),
                "--packet",
                str(packet),
            ]
        )
        assert "USED GPU ACCEPTANCE ARTIFACT: PASS" in out

        rejected = td / "rejected.json"
        rejected.write_text(
            json.dumps(
                case(
                    "synthetic-reject",
                    "hw:fixture:i44",
                    True,
                    vram_claim=24,
                    vram_seen=12,
                ),
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        reject_packet = write_packet(td, [rejected, raw])
        reject_artifact = td / "reject-acceptance.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_used_gpu_acceptance.py"),
                "--case",
                str(rejected),
                "--packet",
                str(reject_packet),
                "--out",
                str(reject_artifact),
            ]
        )
        assert "decision=REJECT" in out

        tampered = td / "tampered-acceptance.json"
        bad = json.loads(reject_artifact.read_text(encoding="utf-8"))
        bad["decision"] = "ACCEPT"
        bad["reject"] = []
        tampered.write_text(
            json.dumps(bad, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        out = run(
            [
                PY,
                str(HERE / "verify_used_gpu_acceptance.py"),
                "--acceptance",
                str(tampered),
                "--case",
                str(rejected),
                "--packet",
                str(reject_packet),
            ],
            expect=2,
        )
        assert "does not exactly match independently rebuilt" in out
        assert "USED GPU ACCEPTANCE ARTIFACT: BLOCKED" in out

        broken_packet = json.loads(packet.read_text(encoding="utf-8"))
        broken_packet["files"][0]["sha256"] = "0" * 64
        broken = td / "broken-PACKET.json"
        broken.write_text(
            json.dumps(broken_packet, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        blocked_out = td / "blocked.json"
        out = run(
            [
                PY,
                str(HERE / "evaluate_used_gpu_acceptance.py"),
                "--case",
                str(healthy),
                "--packet",
                str(broken),
                "--out",
                str(blocked_out),
            ],
            expect=2,
        )
        assert "PACKET SHA256 mismatch" in out
        assert "USED GPU ACCEPTANCE: BLOCKED" in out
        assert not blocked_out.exists()

    print("USED GPU ACCEPTANCE SELFTEST: PASS")
    print("- Experiment 86-compatible ACCEPT is packet-bound and reproducible")
    print("- null unsupported error telemetry stays explicit instead of becoming fake zero")
    print("- VRAM mismatch produces REJECT")
    print("- edited acceptance decision is blocked by independent reconstruction")
    print("- broken PACKET integrity is blocked")
    print("- no ACCEPT/REVIEW/REJECT is mapped to C3/C4")


if __name__ == "__main__":
    main()

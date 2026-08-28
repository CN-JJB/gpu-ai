#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable


def run(args, expect=0):
    p = subprocess.run(args, text=True, capture_output=True)
    out = p.stdout + p.stderr
    if p.returncode != expect:
        print(out)
        raise AssertionError(f"expected return code {expect}, got {p.returncode}: {args}")
    return out


def main():
    fixture_catalog = HERE / "fixtures" / "catalog"
    exp = HERE / "fixtures" / "experiment61"

    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)

        fake = td / "fake_bench.py"
        fake.write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "sys.stdout.write(Path(sys.argv[1]).read_text(encoding='utf-8'))\n"
            "sys.stderr.write('fixture diagnostic\\n')\n",
            encoding="utf-8",
        )

        profile = td / "profile.txt"
        profile.write_text("synthetic capture self-test profile\n", encoding="utf-8")

        sealed = td / "sealed"
        out = run([
            PY,
            str(HERE / "capture_real_benchmark.py"),
            "--manifest",
            str(exp / "manifest.json"),
            "--out-dir",
            str(sealed),
            "--include",
            str(profile),
            "--",
            PY,
            str(fake),
            str(exp / "result.json"),
        ])
        assert "CAPTURE: SEALED" in out
        assert "SEALED is not INTAKE: READY" in out

        for name in ("manifest.json", "result.json", "stderr.txt", "command.json", "PACKET.json"):
            assert (sealed / name).is_file(), name
        assert (sealed / "evidence" / "profile.txt").is_file()

        command = json.loads((sealed / "command.json").read_text(encoding="utf-8"))
        assert command["exit_code"] == 0
        assert command["argv"][0] == PY
        assert command["executable"]["sha256"]
        assert "fixture diagnostic" in (sealed / "stderr.txt").read_text(encoding="utf-8")

        packet = json.loads((sealed / "PACKET.json").read_text(encoding="utf-8"))
        assert packet["packet_schema_version"] == 1
        assert packet["file_count"] == 5
        packet_paths = {x["path"] for x in packet["files"]}
        assert {
            "manifest.json",
            "result.json",
            "stderr.txt",
            "command.json",
            "evidence/profile.txt",
        } == packet_paths

        out = run([
            PY,
            str(HERE / "verify_real_intake.py"),
            str(fixture_catalog),
            "--manifest",
            str(sealed / "manifest.json"),
            "--result",
            str(sealed / "result.json"),
            "--packet",
            str(sealed / "PACKET.json"),
            "--hardware-id",
            "hw:fixture:24g",
            "--model-id",
            "model:fixture:8b",
            "--runtime-id",
            "runtime:fixture",
            "--observed-at",
            "2026-08-27",
            "--allow-synthetic",
        ])
        assert "RAW IDENTITY: PASS" in out
        assert "INTAKE: READY" in out

        fail_script = td / "fail_bench.py"
        fail_script.write_text(
            "import sys\n"
            "print('{}')\n"
            "sys.stderr.write('intentional failure\\n')\n"
            "raise SystemExit(3)\n",
            encoding="utf-8",
        )

        failed = td / "failed"
        out = run([
            PY,
            str(HERE / "capture_real_benchmark.py"),
            "--manifest",
            str(exp / "manifest.json"),
            "--out-dir",
            str(failed),
            "--",
            PY,
            str(fail_script),
        ], expect=2)
        assert "CAPTURE: BLOCKED" in out
        assert "command exited non-zero: 3" in out
        assert (failed / "PACKET.json").is_file()

        failed_command = json.loads((failed / "command.json").read_text(encoding="utf-8"))
        assert failed_command["exit_code"] == 3

        nonempty = td / "nonempty"
        nonempty.mkdir()
        (nonempty / "keep.txt").write_text("do not overwrite\n", encoding="utf-8")
        out = run([
            PY,
            str(HERE / "capture_real_benchmark.py"),
            "--manifest",
            str(exp / "manifest.json"),
            "--out-dir",
            str(nonempty),
            "--",
            PY,
            str(fake),
            str(exp / "result.json"),
        ], expect=1)
        assert "out-dir is not empty" in out
        assert (nonempty / "keep.txt").read_text(encoding="utf-8") == "do not overwrite\n"

    print("REAL BENCHMARK CAPTURE SELFTEST: PASS")
    print("- successful explicit argv is sealed without shell interpolation")
    print("- manifest/result/stderr/command/additional evidence are indexed in PACKET.json")
    print("- sealed synthetic fixture passes the strengthened I07/I20 verifier")
    print("- non-zero benchmark exit remains auditable but CAPTURE: BLOCKED")
    print("- non-empty output directories are never overwritten")


if __name__ == "__main__":
    main()

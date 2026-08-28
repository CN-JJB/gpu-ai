#!/usr/bin/env python3
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "capture_semantic_sources.py"
PY = sys.executable


def run(args, expect=0):
    cp = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if cp.returncode != expect:
        raise AssertionError(f"expected {expect}, got {cp.returncode}\n{cp.stdout}")
    return cp.stdout


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    with tempfile.TemporaryDirectory() as td_raw:
        td = Path(td_raw)
        marker = td / "shell-marker"
        plan = {
            "semantic_source_probe_schema_version": 1,
            "working_directory": ".",
            "probes": [
                {
                    "probe_id": "runtime-version",
                    "purpose": "capture exact runtime/build observation",
                    "argv": [PY, "-c", "import sys; print('build-abc'); print('warn', file=sys.stderr)"],
                    "required": True,
                },
                {
                    "probe_id": "literal-argv",
                    "purpose": "prove shell metacharacters stay literal argv tokens",
                    "argv": [PY, "-c", "import sys; print(sys.argv[1])", f"x; touch {marker}"],
                    "required": True,
                },
                {
                    "probe_id": "optional-missing",
                    "purpose": "preserve an unavailable optional vendor probe",
                    "argv": [str(td / "does-not-exist"), "--version"],
                    "required": False,
                },
            ],
        }
        plan_path = td / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        out_dir = td / "out"
        out = run([PY, str(TOOL), str(plan_path), "--out-dir", str(out_dir)])
        assert "SEMANTIC SOURCE CAPTURE: READY-FOR-SEMANTIC-REVIEW" in out
        assert not marker.exists(), "shell metacharacters must never be executed"

        bundle = json.loads((out_dir / "bundle.json").read_text(encoding="utf-8"))
        assert bundle["status"] == "READY-FOR-SEMANTIC-REVIEW"
        assert bundle["automatic_manifest_update"] == "NOT-PERMITTED"
        assert bundle["required_failures"] == []
        by_id = {x["probe_id"]: x for x in bundle["records"]}
        assert by_id["runtime-version"]["passed"] is True
        assert by_id["optional-missing"]["passed"] is False
        assert by_id["optional-missing"]["launch_error"].startswith("FileNotFoundError:")
        raw = (out_dir / "probes" / "runtime-version.stdout.txt").read_bytes()
        err = (out_dir / "probes" / "runtime-version.stderr.txt").read_bytes()
        assert raw == b"build-abc\n"
        assert err == b"warn\n"
        assert by_id["runtime-version"]["stdout_sha256"] == sha(raw)
        assert by_id["runtime-version"]["stderr_sha256"] == sha(err)
        literal = (out_dir / "probes" / "literal-argv.stdout.txt").read_text(encoding="utf-8")
        assert f"x; touch {marker}" in literal

        blocking_plan = dict(plan)
        blocking_plan["probes"] = [
            {
                "probe_id": "required-failure",
                "purpose": "prove required failure blocks while preserving output",
                "argv": [PY, "-c", "import sys; print('captured'); sys.exit(7)"],
                "required": True,
            }
        ]
        blocking_path = td / "blocking.json"
        blocking_path.write_text(json.dumps(blocking_plan), encoding="utf-8")
        blocked_dir = td / "blocked"
        blocked = run([PY, str(TOOL), str(blocking_path), "--out-dir", str(blocked_dir)], expect=1)
        assert "SEMANTIC SOURCE CAPTURE: BLOCKED" in blocked
        blocked_bundle = json.loads((blocked_dir / "bundle.json").read_text(encoding="utf-8"))
        assert blocked_bundle["status"] == "BLOCKED"
        assert blocked_bundle["required_failures"] == ["required-failure"]
        assert (blocked_dir / "probes" / "required-failure.stdout.txt").read_text() == "captured\n"

        invalid = dict(plan)
        invalid["probes"] = [
            {
                "probe_id": "../escape",
                "purpose": "invalid",
                "argv": [PY, "--version"],
            }
        ]
        invalid_path = td / "invalid.json"
        invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
        invalid_out = run([PY, str(TOOL), str(invalid_path), "--out-dir", str(td / "invalid-out")], expect=1)
        assert "probe_id must match" in invalid_out
        assert not (td / "escape.stdout.txt").exists()

        nonempty = td / "nonempty"
        nonempty.mkdir()
        (nonempty / "keep.txt").write_text("keep", encoding="utf-8")
        out_nonempty = run([PY, str(TOOL), str(plan_path), "--out-dir", str(nonempty)], expect=1)
        assert "out-dir is not empty" in out_nonempty
        assert (nonempty / "keep.txt").read_text() == "keep"

    print("SEMANTIC SOURCE CAPTURE SELFTEST: PASS")
    print("- explicit argv probes are captured without shell interpretation")
    print("- stdout/stderr hashes reproduce captured bytes")
    print("- optional failure is preserved without blocking")
    print("- required failure blocks but keeps raw evidence")
    print("- unsafe probe ids and non-empty output directories are rejected")
    print("- no Experiment 61 manifest is rewritten automatically")


if __name__ == "__main__":
    main()

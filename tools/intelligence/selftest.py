#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PY = sys.executable


def run(args, expect=0):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode != expect:
        print("COMMAND FAILED:", " ".join(map(str, args)))
        print("expected:", expect, "actual:", p.returncode)
        print("STDOUT")
        print(p.stdout)
        print("STDERR")
        print(p.stderr)
        raise SystemExit(2)
    return p.stdout + p.stderr


def main():
    prod = ROOT / "intelligence" / "catalog"
    fixture = HERE / "fixtures" / "catalog"
    exp = HERE / "fixtures" / "experiment61"

    out = run([
        PY, str(HERE / "validate_catalog.py"),
        str(prod),
        "--as-of", "2026-08-27",
    ])
    assert "VALIDATION: PASS" in out

    out = run([
        PY, str(HERE / "validate_catalog.py"),
        str(fixture),
        "--allow-synthetic",
        "--as-of", "2026-08-27",
    ])
    assert "VALIDATION: PASS" in out

    out = run([
        PY, str(HERE / "query_bridge.py"),
        str(fixture),
        "--hardware-id", "hw:fixture:24g",
        "--model-id", "model:fixture:8b",
        "--include-synthetic",
    ])
    assert "TG=50.000" in out
    assert "NOTE: no cross-workload ranking" in out

    out = run([
        PY, str(HERE / "comparable_benchmarks.py"),
        str(fixture),
        "--model-id", "model:fixture:8b",
        "--runtime-id", "runtime:fixture",
        "--include-synthetic",
        "--sort-metric", "tg_tok_s",
    ])
    assert "observations=2" in out
    assert "TG=50.000" in out
    assert "TG=40.000" in out
    assert "comparison_status=DESCRIPTIVE_ONLY" in out
    assert "No cross-group ranking is performed." in out

    out = run([
        PY, str(HERE / "compatibility_preflight.py"),
        str(fixture),
        "--hardware-id", "hw:fixture:24g",
        "--model-id", "model:fixture:8b",
        "--runtime-id", "runtime:fixture",
        "--backend", "FIXTURE",
        "--as-of", "2026-08-27",
        "--include-synthetic",
    ])
    assert "PREFLIGHT: NEEDS-TEST" in out

    out = run([
        PY, str(HERE / "compatibility_preflight.py"),
        str(prod),
        "--hardware-id", "hw:nvidia:geforce-rtx-3090:24g",
        "--model-id", "model:qwen:qwen3-8b",
        "--runtime-id", "runtime:ggml-org:llama.cpp",
        "--backend", "CUDA",
        "--as-of", "2026-08-27",
    ])
    assert "PREFLIGHT: NEEDS-TEST" in out

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        generated = td / "generated.jsonl"

        run([
            PY, str(HERE / "ingest_llama_bench.py"),
            "--manifest", str(exp / "manifest.json"),
            "--result", str(exp / "result.json"),
            "--hardware-id", "hw:fixture:24g",
            "--model-id", "model:fixture:8b",
            "--runtime-id", "runtime:fixture",
            "--record-id", "bench:fixture:generated",
            "--observed-at", "2026-08-27",
            "--packet-source", "fixture:PACKET.json",
            "--out", str(generated),
            "--synthetic",
        ])

        generated_record = json.loads(generated.read_text(encoding="utf-8"))
        assert generated_record["metrics"]["pp_tok_s"] == 1000.0
        assert generated_record["metrics"]["tg_tok_s"] == 50.0

        generated_catalog = td / "catalog"
        generated_catalog.mkdir()
        for name in ("hardware.jsonl", "models.jsonl", "runtimes.jsonl", "market.jsonl", "compatibility.jsonl"):
            shutil.copy2(fixture / name, generated_catalog / name)
        shutil.copy2(generated, generated_catalog / "benchmarks.jsonl")

        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(generated_catalog),
            "--allow-synthetic",
            "--as-of", "2026-08-27",
        ])
        assert "VALIDATION: PASS" in out

        measured = td / "measured-compatibility.jsonl"
        run([
            PY, str(HERE / "ingest_measured_compatibility.py"),
            "--benchmark-record", str(generated),
            "--record-id", "compat:fixture:measured",
            "--out", str(measured),
            "--revalidate-after", "2026-09-27",
            "--synthetic",
        ])

        with (generated_catalog / "compatibility.jsonl").open("a", encoding="utf-8") as f:
            f.write(measured.read_text(encoding="utf-8"))

        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(generated_catalog),
            "--allow-synthetic",
            "--as-of", "2026-08-27",
        ])
        assert "VALIDATION: PASS" in out

        out = run([
            PY, str(HERE / "compatibility_preflight.py"),
            str(generated_catalog),
            "--hardware-id", "hw:fixture:24g",
            "--model-id", "model:fixture:8b",
            "--runtime-id", "runtime:fixture",
            "--backend", "FIXTURE",
            "--artifact-sha256", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "--runtime-build", "fixture-build",
            "--as-of", "2026-08-27",
            "--include-synthetic",
        ])
        assert "PREFLIGHT: PASS-MEASURED" in out
        assert "specificity=5" in out

        out = run([
            PY, str(HERE / "compatibility_preflight.py"),
            str(generated_catalog),
            "--hardware-id", "hw:fixture:24g",
            "--model-id", "model:fixture:8b",
            "--runtime-id", "runtime:fixture",
            "--backend", "FIXTURE",
            "--artifact-sha256", "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "--runtime-build", "fixture-build",
            "--as-of", "2026-08-27",
            "--include-synthetic",
        ])
        assert "PREFLIGHT: NEEDS-TEST" in out

        bad = json.loads(generated.read_text(encoding="utf-8"))
        bad["hardware_id"] = "hw:missing"
        (generated_catalog / "benchmarks.jsonl").write_text(
            json.dumps(bad) + "\n",
            encoding="utf-8",
        )

        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(generated_catalog),
            "--allow-synthetic",
            "--as-of", "2026-08-27",
        ], expect=2)
        assert "unknown hardware_id" in out
        assert "VALIDATION: FAIL" in out

    print("SELFTEST: PASS")
    print("- production catalog validates")
    print("- synthetic catalog validates only with explicit allowance")
    print("- Hardware ↔ Model ↔ Benchmark bridge returns the fixture observation")
    print("- same artifact/workload observations form one descriptive comparison group")
    print("- documented compatibility returns NEEDS-TEST, not measured PASS")\n    print("- Experiment 61 importer reproduces PP/TG")
    print("- broken canonical hardware reference is rejected")


if __name__ == "__main__":
    main()

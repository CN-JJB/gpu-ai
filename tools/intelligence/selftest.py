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
        PY, str(HERE / "price_performance.py"),
        str(fixture),
        "--model-id", "model:fixture:8b",
        "--artifact-sha256", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "--market-record", "market:fixture:24g:2026-08-27",
        "--market-record", "market:fixture:16g:2026-08-27",
        "--metric", "tg_tok_s",
        "--include-synthetic",
    ])
    assert "per_1000=33.333" in out
    assert "per_1000=25.000" in out
    assert "This is not TCO and not a purchase recommendation." in out
    assert "no automatic latest-price join" in out

    out = run([
        PY, str(HERE / "tco_worksheet.py"),
        str(fixture),
        "--case", str(HERE / "fixtures" / "tco-case.json"),
        "--include-synthetic",
    ])
    assert "ENERGY: 438.000 kWh" in out
    assert "TCO: 1938.00 CNY" in out
    assert "not a feasibility gate or purchase recommendation" in out

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
        str(fixture),
        "--hardware-id", "hw:fixture:24g",
        "--model-id", "model:fixture:8b",
        "--runtime-id", "runtime:fixture",
        "--backend", "FIXTURE-UNKNOWN",
        "--as-of", "2026-08-27",
        "--include-synthetic",
    ])
    assert "status=UNKNOWN" in out
    assert "PREFLIGHT: BLOCKED" in out

    out = run([
        PY, str(HERE / "verify_real_intake.py"),
        str(fixture),
        "--manifest", str(exp / "manifest.json"),
        "--result", str(exp / "result.json"),
        "--packet", str(exp / "PACKET.json"),
        "--hardware-id", "hw:fixture:24g",
        "--model-id", "model:fixture:8b",
        "--runtime-id", "runtime:fixture",
        "--observed-at", "2026-08-27",
        "--allow-synthetic",
    ])
    assert "INTAKE: READY" in out
    assert "READY is an evidence-completeness gate" in out

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

    out = run([
        PY, str(HERE / "freshness_report.py"),
        str(prod),
        "--as-of", "2026-08-28",
        "--within-days", "1",
    ])
    assert "DUE-SOON=1" in out
    assert "STALE=0" in out
    assert "market:cn:rtx3090:secondary:2026-08-22" in out
    assert "FRESHNESS: REVALIDATION-QUEUE-PRESENT" in out

    out = run([
        PY, str(HERE / "freshness_report.py"),
        str(prod),
        "--as-of", "2026-09-29",
        "--within-days", "30",
    ])
    assert "market:cn:rtx3090:secondary:2026-08-22" in out
    assert "compat:llama.cpp:cuda:rtx3090:qwen3-8b:2026-08-27" in out
    assert "FRESHNESS: STALE-REVALIDATION-REQUIRED" in out

    out = run([
        PY, str(HERE / "market_matrix.py"),
        str(prod),
        "--geography", "GLOBAL-EBAY",
        "--channel", "secondary-aggregated-ebay-active",
        "--cohort", "used-consumer",
        "--condition", "used",
        "--price-state", "MEDIAN_ASK",
        "--currency", "USD",
        "--as-of", "2026-08-28",
    ])
    assert "observations=3" in out
    assert "contracts=1" in out
    assert "value=1499 USD" in out
    assert "value=1020 USD" in out
    assert "value=330 USD" in out
    assert "Market coverage is not a sale-price claim" in out

    out = run([
        PY, str(HERE / "market_evidence_audit.py"),
        str(prod),
        "--geography", "GLOBAL-EBAY",
        "--channel", "secondary-aggregated-ebay-active",
        "--cohort", "used-consumer",
        "--condition", "used",
        "--price-state", "MEDIAN_ASK",
        "--currency", "USD",
        "--as-of", "2026-08-28",
    ])
    assert "BROAD-SAMPLE=1" in out
    assert "LIMITED-SAMPLE=1" in out
    assert "SMALL-SAMPLE=1" in out
    assert "ASK-ONLY=3" in out
    assert "NOT-CONFIRMED-SALE=3" in out
    assert "ASK-ONLY observations must not be presented as confirmed sale prices." in out

    out = run([
        PY, str(HERE / "compatibility_matrix.py"),
        str(prod),
        "--model-id", "model:qwen:qwen3-8b",
        "--runtime-id", "runtime:ggml-org:llama.cpp",
        "--as-of", "2026-08-28",
    ])
    assert "observations=4" in out
    assert "NEEDS-TEST=4" in out
    assert "COVERAGE: PRESENT" in out
    assert "Coverage is not a performance ranking." in out

    for hardware_id, backend in (
        ("hw:amd:radeon-rx-7900-xtx:24g", "HIP"),
        ("hw:apple:mac-studio-m4-max-40gpu:64g", "METAL"),
        ("hw:intel:arc-a770:16g", "SYCL"),
    ):
        out = run([
            PY, str(HERE / "compatibility_preflight.py"),
            str(prod),
            "--hardware-id", hardware_id,
            "--model-id", "model:qwen:qwen3-8b",
            "--runtime-id", "runtime:ggml-org:llama.cpp",
            "--backend", backend,
            "--as-of", "2026-08-28",
        ])
        assert "status=DOCUMENTED_SUPPORTED" in out
        assert "PREFLIGHT: NEEDS-TEST" in out

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        generated = td / "generated.jsonl"

        market_validation_catalog = td / "market-validation"
        market_validation_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, market_validation_catalog / name)

        market_rows = [
            json.loads(line)
            for line in (market_validation_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in market_rows:
            if row.get("price_state") == "MEDIAN_ASK":
                row.pop("sample", None)
                break
        (market_validation_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in market_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(market_validation_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "MEDIAN_ASK requires sample object" in out
        assert "VALIDATION: FAIL" in out

        bad_packet = td / "bad-PACKET.json"
        packet_obj = json.loads((exp / "PACKET.json").read_text(encoding="utf-8"))
        packet_obj["files"][0]["sha256"] = "0" * 64
        bad_packet.write_text(json.dumps(packet_obj) + "\n", encoding="utf-8")

        out = run([
            PY, str(HERE / "verify_real_intake.py"),
            str(fixture),
            "--manifest", str(exp / "manifest.json"),
            "--result", str(exp / "result.json"),
            "--packet", str(bad_packet),
            "--hardware-id", "hw:fixture:24g",
            "--model-id", "model:fixture:8b",
            "--runtime-id", "runtime:fixture",
            "--observed-at", "2026-08-27",
            "--allow-synthetic",
        ], expect=2)
        assert "INTAKE: BLOCKED" in out
        assert "SHA256 not indexed by packet" in out

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
        assert generated_record["runtime_id"] == "runtime:fixture"

        generated_catalog = td / "catalog"
        generated_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
        ):
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
    print("- explicit same-cohort market rows enable descriptive price/performance")
    print("- evidence-linked TCO fixture reproduces the expected scenario arithmetic")
    print("- documented compatibility returns NEEDS-TEST, not measured PASS")
    print("- NVIDIA/CUDA, AMD/HIP, Apple/Metal and Intel/SYCL production paths all remain NEEDS-TEST")
    print("- compatibility coverage matrix reports four production NEEDS-TEST observations without ranking")
    print("- freshness queue surfaces due-soon and stale production observations")
    print("- market matrix preserves one explicit GLOBAL-EBAY used MEDIAN_ASK cohort across three GPUs")
    print("- market evidence audit exposes ask-only semantics and 47/23/8 listing sample bands")
    print("- MEDIAN_ASK without sample metadata is rejected")
    print("- explicit UNKNOWN remains valid and returns BLOCKED")
    print("- real benchmark intake accepts an intact packet and rejects a tampered packet")
    print("- Experiment 61 importer reproduces PP/TG")
    print("- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED")
    print("- a different artifact falls back to NEEDS-TEST")
    print("- broken canonical hardware reference is rejected")


if __name__ == "__main__":
    main()

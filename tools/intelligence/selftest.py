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
    assert "SUPERSEDED=1" in out
    assert "market:cn:rtx3090:secondary:2026-08-22" in out
    assert "market:cn:a770-16g:secondary:2026-08-21" in out
    assert "superseded_by=market:cn:a770-16g:secondary:2026-08-25" in out
    assert "FRESHNESS: REVALIDATION-QUEUE-PRESENT" in out

    out = run([
        PY, str(HERE / "freshness_report.py"),
        str(prod),
        "--as-of", "2026-09-29",
        "--within-days", "30",
    ])
    assert "market:cn:rtx3090:secondary:2026-08-22" in out
    assert "market:cn:a770-16g:secondary:2026-08-21" in out
    assert "SUPERSEDED=1" in out
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
        PY, str(HERE / "market_matrix.py"),
        str(prod),
        "--geography", "CN",
        "--channel", "secondary-summary",
        "--cohort", "used-consumer",
        "--condition", "working-unverified",
        "--price-state", "SECONDARY_REPORTED",
        "--currency", "CNY",
        "--as-of", "2026-08-28",
    ])
    assert "observations=2" in out
    assert "contracts=1" in out
    assert "value=7400 CNY" in out
    assert "value=1400 CNY" in out
    assert "value=1450 CNY" not in out
    assert "Superseded observations are hidden by default" in out

    out = run([
        PY, str(HERE / "market_matrix.py"),
        str(prod),
        "--geography", "CN",
        "--channel", "secondary-summary",
        "--cohort", "used-consumer",
        "--condition", "working-unverified",
        "--price-state", "SECONDARY_REPORTED",
        "--currency", "CNY",
        "--as-of", "2026-08-28",
        "--include-superseded",
    ])
    assert "observations=3" in out
    assert "value=1450 CNY" in out
    assert "superseded_by=market:cn:a770-16g:secondary:2026-08-25" in out

    out = run([
        PY, str(HERE / "market_evidence_gate.py"),
        str(prod),
        "--as-of", "2026-08-28",
    ])
    assert "observations=15" in out
    assert "M0=0" in out
    assert "M1=3" in out
    assert "M2=3" in out
    assert "M3=9" in out
    assert "CURRENT=14" in out
    assert "SUPERSEDED=1" in out
    assert "ELIGIBLE=12" in out
    assert "NEEDS-STRONGER-MARKET-EVIDENCE=2" in out
    assert "SUPERSEDED-USE-NEWER-OBSERVATION=1" in out
    assert "watchlist_market_gate=NEEDS-STRONGER-MARKET-EVIDENCE" in out
    assert "watchlist_market_gate=ELIGIBLE" in out
    assert "watchlist_market_gate=SUPERSEDED-USE-NEWER-OBSERVATION" in out
    assert "M3 is claim-scoped" in out
    assert "GATE: PASS" in out

    out = run([
        PY, str(HERE / "market_evidence_gate.py"),
        str(prod),
        "--record-id", "market:cn:a770-16g:secondary:2026-08-25",
        "--as-of", "2026-09-01",
    ])
    assert "DUE-TODAY=1" in out
    assert "REVALIDATE-NOW=1" in out
    assert "watchlist_market_gate=REVALIDATE-NOW" in out

    out = run([
        PY, str(HERE / "market_evidence_gate.py"),
        str(prod),
        "--as-of", "2026-09-05",
    ])
    assert "STALE=14" in out
    assert "SUPERSEDED=1" in out
    assert "STALE-REVALIDATE=14" in out
    assert "SUPERSEDED-USE-NEWER-OBSERVATION=1" in out
    assert "Due-today, stale or unscheduled market evidence must be revalidated" in out

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
        PY, str(HERE / "sold_marked_market.py"),
        str(prod),
    ])
    assert "observations=9" in out
    assert "hardware_groups=3" in out
    assert "median_displayed=950 USD" in out
    assert "median_displayed=700 USD" in out
    assert "median_displayed=200 USD" in out
    assert "confirmed_transaction_price=false" in out
    assert "not a confirmed-sale median" in out

    out = run([
        PY, str(HERE / "compare_market_contracts.py"),
        str(prod),
        "--left-geography", "GLOBAL-EBAY",
        "--left-channel", "secondary-aggregated-ebay-active",
        "--left-cohort", "used-consumer",
        "--left-condition", "used",
        "--left-price-state", "MEDIAN_ASK",
        "--left-currency", "USD",
        "--right-geography", "US",
        "--right-channel", "offerup-sold-marked-listing",
        "--right-cohort", "used-consumer",
        "--right-condition", "used",
        "--right-price-state", "SOLD_MARKED_LISTING_PRICE",
        "--right-currency", "USD",
    ])
    assert "common_hardware=3" in out
    assert "left_median=1499" in out
    assert "right_median=950" in out
    assert "right_vs_left_pct=-36.6%" in out
    assert "left_median=1020" in out
    assert "right_median=700" in out
    assert "right_vs_left_pct=-31.4%" in out
    assert "left_median=330" in out
    assert "right_median=200" in out
    assert "right_vs_left_pct=-39.4%" in out
    assert "not a confirmed transaction discount" in out

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

        lineage_catalog = td / "lineage-validation"
        lineage_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, lineage_catalog / name)

        lineage_rows = [
            json.loads(line)
            for line in (lineage_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in lineage_rows:
            if row.get("record_id") == "market:cn:a770-16g:secondary:2026-08-25":
                row["supersedes"] = "market:missing"
                break
        (lineage_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in lineage_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(lineage_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "supersedes references unknown market record" in out
        assert "VALIDATION: FAIL" in out

        revalidation_catalog = td / "revalidation-validation"
        revalidation_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, revalidation_catalog / name)

        revalidation_rows = [
            json.loads(line)
            for line in (revalidation_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in revalidation_rows:
            if row.get("price_state") == "MEDIAN_ASK":
                row.pop("revalidate_after", None)
                break
        (revalidation_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in revalidation_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(revalidation_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "production market record requires revalidate_after" in out
        assert "VALIDATION: FAIL" in out

        grade_validation_catalog = td / "grade-validation"
        grade_validation_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, grade_validation_catalog / name)

        grade_rows = [
            json.loads(line)
            for line in (grade_validation_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in grade_rows:
            if row.get("price_state") == "MEDIAN_ASK":
                row["market_evidence_grade"] = "M3"
                break
        (grade_validation_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in grade_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(grade_validation_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "MEDIAN_ASK market_evidence_grade must be M2" in out
        assert "VALIDATION: FAIL" in out

        secondary_validation_catalog = td / "secondary-validation"
        secondary_validation_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, secondary_validation_catalog / name)

        secondary_rows = [
            json.loads(line)
            for line in (secondary_validation_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in secondary_rows:
            if row.get("price_state") == "SECONDARY_REPORTED":
                row["report"]["confirmed_sale"] = True
                break
        (secondary_validation_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in secondary_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(secondary_validation_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "SECONDARY_REPORTED confirmed_sale must be false" in out
        assert "VALIDATION: FAIL" in out

        sold_validation_catalog = td / "sold-validation"
        sold_validation_catalog.mkdir()
        for name in (
            "hardware.jsonl",
            "models.jsonl",
            "runtimes.jsonl",
            "market.jsonl",
            "compatibility.jsonl",
            "benchmarks.jsonl",
        ):
            shutil.copy2(prod / name, sold_validation_catalog / name)

        sold_rows = [
            json.loads(line)
            for line in (sold_validation_catalog / "market.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for row in sold_rows:
            if row.get("price_state") == "SOLD_MARKED_LISTING_PRICE":
                row["listing"]["confirmed_transaction_price"] = True
                break
        (sold_validation_catalog / "market.jsonl").write_text(
            "\n".join(json.dumps(x) for x in sold_rows) + "\n",
            encoding="utf-8",
        )
        out = run([
            PY, str(HERE / "validate_catalog.py"),
            str(sold_validation_catalog),
            "--as-of", "2026-08-28",
        ], expect=2)
        assert "confirmed_transaction_price must be false" in out
        assert "VALIDATION: FAIL" in out

        watchlist = td / "watchlist.csv"
        watchlist.write_text(
            "candidate,exact_model,ask_cny,price_state,observed_at,revalidate_after,fit,software,performance,market_evidence,condition_evidence,max_sticker_cny,watch_band_pct,source,notes\n"
            "CURRENT,RTX 3090,1000,ASK,2026-08-27,2026-08-29,PASS,PASS,PASS,M2,C3,1200,10,https://example.invalid,current\n"
            "DUE,RTX 3090,1000,ASK,2026-08-27,2026-08-28,PASS,PASS,PASS,M2,C3,1200,10,https://example.invalid,due\n"
            "STALE,RTX 3090,1000,ASK,2026-08-20,2026-08-27,PASS,PASS,PASS,M2,C3,1200,10,https://example.invalid,stale\n"
            "INVALID,RTX 3090,1000,ASK,2026-08-27,not-a-date,PASS,PASS,PASS,M2,C3,1200,10,https://example.invalid,invalid\n",
            encoding="utf-8",
        )
        out = run([
            PY,
            str(ROOT / "labs" / "experiments" / "38-real-candidate-watchlist" / "evaluate_watchlist.py"),
            str(watchlist),
            "--as-of", "2026-08-28T12:00:00+00:00",
        ])
        assert "CURRENT: BUY-CANDIDATE" in out
        assert "freshness=CURRENT" in out
        assert "DUE: NEEDS EVIDENCE" in out
        assert "freshness=DUE-TODAY" in out
        assert "STALE: NEEDS EVIDENCE" in out
        assert "freshness=STALE" in out
        assert "INVALID: NEEDS EVIDENCE" in out
        assert "freshness=INVALID" in out

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
    print("- sold-marked OfferUp pages stay distinct from confirmed transaction prices")
    print("- SOLD_MARKED_LISTING_PRICE falsely claiming confirmed transaction is rejected")
    print("- cross-market comparison exposes eBay-ask vs OfferUp-sold-marked signal gaps without calling them discounts")
    print("- China secondary watch contract preserves 3090/A770 reported signals without claiming direct samples or sales")
    print("- SECONDARY_REPORTED falsely claiming confirmed sale is rejected")
    print("- market evidence gate maps production signals to M1/M2/M3 with claim-scoped watchlist eligibility")
    print("- mismatched market evidence grade is rejected")
    print("- market evidence eligibility is freshness-aware and all real market rows require revalidation dates")
    print("- Experiment 38 blocks due-today, stale and invalid market evidence from BUY-CANDIDATE")
    print("- append-only A770 refresh supersedes the old observation without deleting audit history")
    print("- superseded observations leave active market/freshness/watchlist views by default")
    print("- broken market refresh lineage is rejected")
    print("- explicit UNKNOWN remains valid and returns BLOCKED")
    print("- real benchmark intake accepts an intact packet and rejects a tampered packet")
    print("- Experiment 61 importer reproduces PP/TG")
    print("- exact benchmark Evidence upgrades only the matching path to PASS-MEASURED")
    print("- a different artifact falls back to NEEDS-TEST")
    print("- broken canonical hardware reference is rejected")


if __name__ == "__main__":
    main()

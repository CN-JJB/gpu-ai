#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_one(path):
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if len(rows) != 1:
        raise SystemExit("benchmark record input must contain exactly one JSON object")
    return rows[0]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--benchmark-record", type=Path, required=True)
    p.add_argument("--record-id", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--revalidate-after")
    p.add_argument("--append", action="store_true")
    p.add_argument("--synthetic", action="store_true")
    a = p.parse_args()

    b = load_one(a.benchmark_record)

    if b.get("record_type") != "benchmark":
        raise SystemExit("input is not a benchmark record")
    if not b.get("runtime_id"):
        raise SystemExit("benchmark record missing canonical runtime_id")

    src_class = str((b.get("source") or {}).get("evidence_class", "")).upper()
    if a.synthetic:
        if src_class != "SYNTHETIC":
            raise SystemExit("--synthetic requires a SYNTHETIC benchmark record")
        out_class = "SYNTHETIC"
    else:
        if src_class != "MEASURED" or b.get("synthetic", False):
            raise SystemExit("production measured compatibility requires a non-synthetic MEASURED benchmark record")
        out_class = "MEASURED"

    metrics = b.get("metrics") or {}
    positive = [
        x for x in (metrics.get("pp_tok_s"), metrics.get("tg_tok_s"))
        if isinstance(x, (int, float)) and x > 0
    ]
    if not positive:
        raise SystemExit("benchmark has no positive PP/TG result")

    artifact = b.get("artifact") or {}
    runtime = b.get("runtime") or {}
    hw = b.get("hardware_evidence") or {}
    evidence = b.get("evidence") or {}

    for name, value in (
        ("artifact.sha256", artifact.get("sha256")),
        ("artifact.quant", artifact.get("quant")),
        ("runtime.backend", runtime.get("backend")),
        ("runtime.runtime_identity", runtime.get("runtime_identity")),
        ("runtime.build_identity", runtime.get("build_identity")),
        ("evidence.raw_result_source", evidence.get("raw_result_source")),
        ("evidence.manifest_source", evidence.get("manifest_source")),
        ("evidence.packet_source", evidence.get("packet_source")),
    ):
        if value in (None, "", "REPLACE", "TODO", "TBD"):
            raise SystemExit(f"benchmark missing {name}")

    record = {
        "schema_version": 1,
        "record_type": "compatibility",
        "record_id": a.record_id,
        "hardware_id": b["hardware_id"],
        "model_id": b["model_id"],
        "runtime_id": b["runtime_id"],
        "backend": runtime["backend"],
        "status": "MEASURED_SUPPORTED",
        "observed_at": b["observed_at"],
        "scope": {
            "representation": "exact benchmark artifact",
            "artifact_sha256": artifact["sha256"],
            "quant": artifact["quant"],
            "runtime_identity": runtime["runtime_identity"],
            "runtime_build": runtime["build_identity"],
            "device_identity": hw.get("device_identity"),
            "profile_sha256": hw.get("profile_sha256"),
            "workload": b.get("workload"),
            "measurement_required": False,
            "notes": "Positive benchmark Evidence proves only this exact recorded path; do not generalize to other artifacts/builds/workloads."
        },
        "evidence": {
            "benchmark_record_id": b["record_id"],
            "run_source": evidence["raw_result_source"],
            "manifest_source": evidence["manifest_source"],
            "packet_source": evidence["packet_source"],
        },
        "source": {
            "evidence_class": out_class,
            "source_path": evidence["packet_source"],
            "observed_at": b["observed_at"],
        },
        "synthetic": bool(a.synthetic),
    }

    if a.revalidate_after:
        record["revalidate_after"] = a.revalidate_after

    text = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
    mode = "a" if a.append else "w"
    with a.out.open(mode, encoding="utf-8") as f:
        f.write(text)

    print(f"wrote {a.record_id}")
    print("status=MEASURED_SUPPORTED")
    print(f"artifact={artifact['sha256']} quant={artifact['quant']}")
    print(f"runtime_build={runtime['build_identity']}")
    print("Scope is exact-path only.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path


def load(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--hardware-id", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--runtime-id", required=True)
    p.add_argument("--backend", required=True)
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    models = {x["model_id"]: x for x in load(a.catalog / "models.jsonl")}
    runtimes = {x["runtime_id"]: x for x in load(a.catalog / "runtimes.jsonl")}

    if a.hardware_id not in hardware:
        raise SystemExit(f"unknown hardware_id: {a.hardware_id}")
    if a.model_id not in models:
        raise SystemExit(f"unknown model_id: {a.model_id}")
    if a.runtime_id not in runtimes:
        raise SystemExit(f"unknown runtime_id: {a.runtime_id}")

    observations = []
    for x in load(a.catalog / "compatibility.jsonl"):
        if x.get("hardware_id") != a.hardware_id:
            continue
        if x.get("model_id") != a.model_id:
            continue
        if x.get("runtime_id") != a.runtime_id:
            continue
        if str(x.get("backend", "")).upper() != a.backend.upper():
            continue
        if x.get("synthetic", False) and not a.include_synthetic:
            continue
        observations.append(x)

    observations.sort(key=lambda x: str(x.get("observed_at", "")), reverse=True)

    print("PATH")
    print(f"- hardware: {hardware[a.hardware_id]['canonical_name']}")
    print(f"- model: {models[a.model_id]['canonical_name']}")
    print(f"- runtime: {runtimes[a.runtime_id]['canonical_name']}")
    print(f"- backend: {a.backend.upper()}")

    if not observations:
        print("OBSERVATION: none")
        print("PREFLIGHT: BLOCKED")
        print("Reason: no exact compatibility observation; do not guess support.")
        return

    x = observations[0]
    status = str(x.get("status", "UNKNOWN")).upper()
    stale = False
    if x.get("revalidate_after"):
        stale = date.fromisoformat(str(x["revalidate_after"])) < date.fromisoformat(a.as_of)

    print(f"OBSERVATION: {x.get('record_id')}")
    print(f"status={status} observed={x.get('observed_at')} revalidate_after={x.get('revalidate_after')}")
    print(f"evidence={x.get('source', {}).get('evidence_class')}")
    scope = x.get("scope", {})
    print(f"representation={scope.get('representation')}")
    print(f"measurement_required={scope.get('measurement_required')}")
    print(f"notes={scope.get('notes')}")

    if stale:
        decision = "STALE-REVALIDATE"
    elif status == "MEASURED_SUPPORTED":
        decision = "PASS-MEASURED"
    elif status == "DOCUMENTED_SUPPORTED":
        decision = "NEEDS-TEST"
    elif status in {"PARTIAL", "EXPERIMENTAL"}:
        decision = "REVIEW"
    elif status == "DOCUMENTED_UNSUPPORTED":
        decision = "FAIL"
    else:
        decision = "BLOCKED"

    print(f"PREFLIGHT: {decision}")
    print("A documented support observation is not a measured deployment PASS.")


if __name__ == "__main__":
    main()

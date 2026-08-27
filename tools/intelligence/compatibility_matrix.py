#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

DECISION = {
    "MEASURED_SUPPORTED": "PASS-MEASURED",
    "DOCUMENTED_SUPPORTED": "NEEDS-TEST",
    "PARTIAL": "REVIEW",
    "EXPERIMENTAL": "REVIEW",
    "DOCUMENTED_UNSUPPORTED": "FAIL",
    "UNKNOWN": "BLOCKED",
}


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
    p.add_argument("--model-id", required=True)
    p.add_argument("--runtime-id", required=True)
    p.add_argument("--backend")
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    models = {x["model_id"]: x for x in load(a.catalog / "models.jsonl")}
    runtimes = {x["runtime_id"]: x for x in load(a.catalog / "runtimes.jsonl")}

    if a.model_id not in models:
        raise SystemExit(f"unknown model_id: {a.model_id}")
    if a.runtime_id not in runtimes:
        raise SystemExit(f"unknown runtime_id: {a.runtime_id}")

    as_of = date.fromisoformat(a.as_of)
    rows = []

    for x in load(a.catalog / "compatibility.jsonl"):
        if x.get("model_id") != a.model_id:
            continue
        if x.get("runtime_id") != a.runtime_id:
            continue
        if a.backend and str(x.get("backend", "")).upper() != a.backend.upper():
            continue
        if x.get("synthetic", False) and not a.include_synthetic:
            continue

        h = hardware.get(x.get("hardware_id"))
        if h is None:
            continue

        status = str(x.get("status", "UNKNOWN")).upper()
        stale = False
        if x.get("revalidate_after"):
            stale = date.fromisoformat(str(x["revalidate_after"])) < as_of

        decision = "STALE-REVALIDATE" if stale else DECISION.get(status, "BLOCKED")
        scope = x.get("scope") or {}
        scope_kind = "EXACT" if (
            scope.get("artifact_sha256")
            or scope.get("runtime_build")
            or scope.get("profile_sha256")
        ) else "GENERIC"

        rows.append({
            "vendor": h.get("vendor", "?"),
            "hardware": h.get("canonical_name", x.get("hardware_id")),
            "hardware_id": x.get("hardware_id"),
            "backend": str(x.get("backend", "")).upper(),
            "status": status,
            "decision": decision,
            "scope": scope_kind,
            "observed_at": x.get("observed_at"),
            "revalidate_after": x.get("revalidate_after"),
            "evidence": (x.get("source") or {}).get("evidence_class"),
            "record_id": x.get("record_id"),
        })

    rows.sort(key=lambda x: (x["vendor"], x["hardware"], x["backend"], x["scope"], x["record_id"]))

    print("COMPATIBILITY COVERAGE")
    print(f"model={models[a.model_id]['canonical_name']}")
    print(f"runtime={runtimes[a.runtime_id]['canonical_name']}")
    print(f"as_of={a.as_of}")
    print(f"observations={len(rows)}")

    counts = {}
    for x in rows:
        counts[x["decision"]] = counts.get(x["decision"], 0) + 1
        print(
            f"- vendor={x['vendor']} | hardware={x['hardware']} | "
            f"backend={x['backend']} | status={x['status']} | "
            f"decision={x['decision']} | scope={x['scope']} | "
            f"observed={x['observed_at']} | revalidate_after={x['revalidate_after']} | "
            f"evidence={x['evidence']} | record={x['record_id']}"
        )

    print("DECISION COUNTS")
    for key in sorted(counts):
        print(f"- {key}={counts[key]}")

    if not rows:
        print("COVERAGE: EMPTY")
    else:
        print("COVERAGE: PRESENT")

    print("Coverage is not a performance ranking.")
    print("EXACT measured observations apply only to their recorded artifact/build/device scope.")


if __name__ == "__main__":
    main()

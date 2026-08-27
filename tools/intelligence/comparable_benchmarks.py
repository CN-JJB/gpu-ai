#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def load(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def comparison_payload(b):
    artifact = b.get("artifact") or {}
    return {
        "model_id": b.get("model_id"),
        "artifact_sha256": artifact.get("sha256"),
        "quant": artifact.get("quant"),
        "workload": b.get("workload") or {},
    }


def fingerprint(b):
    raw = json.dumps(
        comparison_payload(b),
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def fmt(v):
    return f"{v:.3f}" if isinstance(v, (int, float)) else "n/a"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--model-id")
    p.add_argument("--runtime-id")
    p.add_argument("--include-synthetic", action="store_true")
    p.add_argument("--sort-metric", choices=("pp_tok_s", "tg_tok_s"))
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    models = {x["model_id"]: x for x in load(a.catalog / "models.jsonl")}
    runtimes = {x["runtime_id"]: x for x in load(a.catalog / "runtimes.jsonl")}
    benches = load(a.catalog / "benchmarks.jsonl")

    filtered = []
    for b in benches:
        if b.get("synthetic", False) and not a.include_synthetic:
            continue
        if a.model_id and b.get("model_id") != a.model_id:
            continue
        if a.runtime_id and b.get("runtime_id") != a.runtime_id:
            continue
        filtered.append(b)

    if not filtered:
        print("NO BENCHMARK OBSERVATIONS")
        return

    groups = {}
    for b in filtered:
        groups.setdefault(fingerprint(b), []).append(b)

    print(f"COMPARISON GROUPS: {len(groups)}")

    for fp in sorted(groups):
        rows = groups[fp]
        first = rows[0]
        payload = comparison_payload(first)
        model = models.get(first.get("model_id"), {})
        print()
        print(f"GROUP {fp}")
        print(f"observations={len(rows)}")
        print(f"model={model.get('canonical_name', first.get('model_id'))}")
        print(f"artifact_sha256={payload['artifact_sha256']}")
        print(f"quant={payload['quant']}")
        print("comparison_type=OBSERVATIONAL_SYSTEM_COMPARISON")
        print("workload=" + json.dumps(payload["workload"], sort_keys=True, separators=(",", ":")))

        if a.sort_metric:
            rows = sorted(
                rows,
                key=lambda x: (
                    (x.get("metrics") or {}).get(a.sort_metric)
                    if isinstance((x.get("metrics") or {}).get(a.sort_metric), (int, float))
                    else float("-inf")
                ),
                reverse=True,
            )
        else:
            rows = sorted(rows, key=lambda x: str(x.get("record_id", "")))

        for b in rows:
            h = hardware.get(b.get("hardware_id"), {})
            rt = runtimes.get(b.get("runtime_id"), {})
            run = b.get("runtime") or {}
            met = b.get("metrics") or {}
            ev = b.get("evidence") or {}
            print(
                f"- {b.get('record_id')} | "
                f"hardware={h.get('canonical_name', b.get('hardware_id'))} | "
                f"runtime={rt.get('canonical_name', b.get('runtime_id'))}/{run.get('backend')} | "
                f"build={run.get('build_identity')} | "
                f"PP={fmt(met.get('pp_tok_s'))} | TG={fmt(met.get('tg_tok_s'))} | "
                f"packet={ev.get('packet_source')}"
            )

        if len(rows) < 2:
            print("comparison_status=INSUFFICIENT_COMPARABLE_OBSERVATIONS")
        else:
            print("comparison_status=DESCRIPTIVE_ONLY")

    print()
    print("No cross-group ranking is performed.")
    print("Sorted PP/TG within one group is not a purchase recommendation or causal claim.")


if __name__ == "__main__":
    main()

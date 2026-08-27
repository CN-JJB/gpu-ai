#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def load(path):
    rows = []
    if not path.exists():
        return rows
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw:
            rows.append(json.loads(raw))
    return rows


def fingerprint(workload):
    raw = json.dumps(workload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def fmt(v):
    if isinstance(v, (int, float)):
        return f"{v:.3f}"
    return "n/a"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--hardware-id", required=True)
    p.add_argument("--model-id", required=True)
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {r["hardware_id"]: r for r in load(a.catalog / "hardware.jsonl")}
    models = {r["model_id"]: r for r in load(a.catalog / "models.jsonl")}
    market = load(a.catalog / "market.jsonl")
    benches = load(a.catalog / "benchmarks.jsonl")

    h = hardware.get(a.hardware_id)
    m = models.get(a.model_id)
    if h is None:
        raise SystemExit(f"unknown hardware_id: {a.hardware_id}")
    if m is None:
        raise SystemExit(f"unknown model_id: {a.model_id}")

    print("HARDWARE")
    print(f"- {h['hardware_id']} — {h['canonical_name']}")
    print(f"- vendor={h.get('vendor')} memory_gib={h.get('memory_gib', 'n/a')} architecture={h.get('architecture', 'n/a')}")
    print("MODEL")
    print(f"- {m['model_id']} — {m['canonical_name']}")
    print(f"- repository={m.get('repository')} architecture={m.get('architecture')}")

    prices = [x for x in market if x.get("hardware_id") == a.hardware_id]
    prices.sort(key=lambda x: str(x.get("observed_at", "")), reverse=True)
    print("MARKET OBSERVATIONS")
    if not prices:
        print("- none")
    else:
        for x in prices[:5]:
            price = x.get("price", {})
            print(
                f"- {x.get('record_id')} observed={x.get('observed_at')} "
                f"{price.get('value')} {price.get('currency')} "
                f"state={x.get('price_state')} evidence={x.get('source', {}).get('evidence_class')}"
            )

    matches = []
    for b in benches:
        if b.get("hardware_id") != a.hardware_id or b.get("model_id") != a.model_id:
            continue
        if b.get("synthetic", False) and not a.include_synthetic:
            continue
        matches.append(b)

    print("BENCHMARK OBSERVATIONS")
    if not matches:
        print("NO MATCHING BENCHMARK OBSERVATIONS")
        return

    groups = {}
    for b in matches:
        fp = fingerprint(b.get("workload", {}))
        groups.setdefault(fp, []).append(b)

    for fp in sorted(groups):
        print(f"[workload {fp}]")
        for b in sorted(groups[fp], key=lambda x: str(x.get("observed_at", ""))):
            rt = b.get("runtime", {})
            art = b.get("artifact", {})
            met = b.get("metrics", {})
            print(
                f"- {b.get('record_id')} observed={b.get('observed_at')} "
                f"runtime={rt.get('name')}/{rt.get('backend')} quant={art.get('quant')} "
                f"PP={fmt(met.get('pp_tok_s'))} TG={fmt(met.get('tg_tok_s'))} "
                f"synthetic={bool(b.get('synthetic', False))}"
            )
            ev = b.get("evidence", {})
            print(f"  evidence: manifest={ev.get('manifest_source')} raw={ev.get('raw_result_source')} packet={ev.get('packet_source')}")

    print("NOTE: no cross-workload ranking or implicit price/performance merge is performed.")


if __name__ == "__main__":
    main()

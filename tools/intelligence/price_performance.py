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


def payload(b):
    a = b.get("artifact") or {}
    return {
        "model_id": b.get("model_id"),
        "artifact_sha256": a.get("sha256"),
        "quant": a.get("quant"),
        "workload": b.get("workload") or {},
    }


def fingerprint(b):
    return hashlib.sha256(
        json.dumps(payload(b), sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()[:12]


def market_contract(m):
    p = m.get("price") or {}
    return {
        "geography": m.get("geography"),
        "channel": m.get("channel"),
        "cohort": m.get("cohort"),
        "condition": m.get("condition"),
        "price_state": m.get("price_state"),
        "currency": p.get("currency"),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--model-id", required=True)
    p.add_argument("--artifact-sha256", required=True)
    p.add_argument("--market-record", action="append", required=True)
    p.add_argument("--metric", choices=("pp_tok_s", "tg_tok_s"), default="tg_tok_s")
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    market_all = {x["record_id"]: x for x in load(a.catalog / "market.jsonl")}
    benches = load(a.catalog / "benchmarks.jsonl")

    selected_market = []
    for rid in a.market_record:
        if rid not in market_all:
            raise SystemExit(f"unknown market record: {rid}")
        m = market_all[rid]
        if m.get("synthetic", False) and not a.include_synthetic:
            raise SystemExit(f"synthetic market record requires --include-synthetic: {rid}")
        selected_market.append(m)

    contracts = {
        json.dumps(market_contract(m), sort_keys=True)
        for m in selected_market
    }
    if len(contracts) != 1:
        raise SystemExit("selected market observations have incompatible market contracts")

    market_by_hw = {}
    for m in selected_market:
        hid = m.get("hardware_id")
        if hid in market_by_hw:
            raise SystemExit(f"multiple selected market observations for hardware {hid}")
        market_by_hw[hid] = m

    candidates = []
    for b in benches:
        if b.get("synthetic", False) and not a.include_synthetic:
            continue
        if b.get("model_id") != a.model_id:
            continue
        if str((b.get("artifact") or {}).get("sha256", "")).lower() != a.artifact_sha256.lower():
            continue
        if b.get("hardware_id") not in market_by_hw:
            continue
        metric = (b.get("metrics") or {}).get(a.metric)
        if not isinstance(metric, (int, float)) or metric <= 0:
            continue
        candidates.append(b)

    if len(candidates) < 2:
        raise SystemExit("need at least two benchmark+explicit-market pairs")

    fps = {fingerprint(b) for b in candidates}
    if len(fps) != 1:
        raise SystemExit("selected observations span multiple benchmark comparison groups")

    rows = []
    for b in candidates:
        m = market_by_hw[b["hardware_id"]]
        price = (m.get("price") or {}).get("value")
        if not isinstance(price, (int, float)) or price <= 0:
            raise SystemExit(f"invalid price in {m.get('record_id')}")
        metric = b["metrics"][a.metric]
        rows.append((metric / price * 1000.0, b, m))

    rows.sort(key=lambda x: x[0], reverse=True)
    contract = market_contract(selected_market[0])
    fp = next(iter(fps))

    print(f"BENCHMARK GROUP: {fp}")
    print("MARKET CONTRACT: " + json.dumps(contract, sort_keys=True, separators=(",", ":")))
    print(f"DERIVED METRIC: {a.metric} per 1000 {contract['currency']}")
    print("comparison_type=DESCRIPTIVE_PRICE_PERFORMANCE")

    for derived, b, m in rows:
        h = hardware.get(b["hardware_id"], {})
        raw = b["metrics"][a.metric]
        price = m["price"]["value"]
        print(
            f"- {h.get('canonical_name', b['hardware_id'])} | "
            f"{a.metric}={raw:.3f} | price={price:g} {contract['currency']} | "
            f"per_1000={derived:.3f} | market={m['record_id']} | "
            f"observed={m.get('observed_at')} | revalidate_after={m.get('revalidate_after')}"
        )

    print("This is not TCO and not a purchase recommendation.")
    print("Market observations were explicitly selected; no automatic latest-price join was used.")


if __name__ == "__main__":
    main()

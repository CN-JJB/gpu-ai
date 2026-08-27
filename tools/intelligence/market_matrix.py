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
    p.add_argument("--geography")
    p.add_argument("--channel")
    p.add_argument("--cohort")
    p.add_argument("--condition")
    p.add_argument("--price-state")
    p.add_argument("--currency")
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    as_of = date.fromisoformat(a.as_of)
    rows = []

    filters = {
        "geography": a.geography,
        "channel": a.channel,
        "cohort": a.cohort,
        "condition": a.condition,
        "price_state": a.price_state,
    }

    for m in load(a.catalog / "market.jsonl"):
        if m.get("synthetic", False) and not a.include_synthetic:
            continue

        reject = False
        for field, wanted in filters.items():
            if wanted is not None and str(m.get(field)) != wanted:
                reject = True
                break
        if reject:
            continue

        price = m.get("price") or {}
        if a.currency is not None and str(price.get("currency")) != a.currency:
            continue

        stale = False
        if m.get("revalidate_after"):
            stale = date.fromisoformat(str(m["revalidate_after"])) < as_of

        rows.append({
            "record_id": m.get("record_id"),
            "hardware_id": m.get("hardware_id"),
            "hardware": (hardware.get(m.get("hardware_id")) or {}).get("canonical_name", m.get("hardware_id")),
            "geography": m.get("geography"),
            "channel": m.get("channel"),
            "cohort": m.get("cohort"),
            "condition": m.get("condition"),
            "price_state": m.get("price_state"),
            "currency": price.get("currency"),
            "value": price.get("value"),
            "observed_at": m.get("observed_at"),
            "revalidate_after": m.get("revalidate_after"),
            "stale": stale,
            "evidence": (m.get("source") or {}).get("evidence_class"),
        })

    rows.sort(key=lambda x: (str(x["geography"]), str(x["channel"]), str(x["hardware"]), str(x["record_id"])))

    contracts = {}
    for x in rows:
        key = (
            x["geography"],
            x["channel"],
            x["cohort"],
            x["condition"],
            x["price_state"],
            x["currency"],
        )
        contracts[key] = contracts.get(key, 0) + 1

    print("MARKET COVERAGE")
    print(f"as_of={a.as_of}")
    print(f"observations={len(rows)}")
    print(f"contracts={len(contracts)}")

    for key in sorted(contracts, key=lambda x: tuple("" if v is None else str(v) for v in x)):
        geography, channel, cohort, condition, price_state, currency = key
        print(
            "CONTRACT "
            f"geography={geography} | channel={channel} | cohort={cohort} | "
            f"condition={condition} | price_state={price_state} | currency={currency} | "
            f"observations={contracts[key]}"
        )
        for x in rows:
            xkey = (
                x["geography"],
                x["channel"],
                x["cohort"],
                x["condition"],
                x["price_state"],
                x["currency"],
            )
            if xkey != key:
                continue
            freshness = "STALE" if x["stale"] else "CURRENT"
            print(
                f"- hardware={x['hardware']} | value={x['value']} {x['currency']} | "
                f"observed={x['observed_at']} | revalidate_after={x['revalidate_after']} | "
                f"freshness={freshness} | evidence={x['evidence']} | record={x['record_id']}"
            )

    if not rows:
        print("COVERAGE: EMPTY")
    else:
        print("COVERAGE: PRESENT")

    print("Market coverage is not a sale-price claim and not a purchase recommendation.")
    print("Never merge different contracts without an explicit comparison rule.")


if __name__ == "__main__":
    main()

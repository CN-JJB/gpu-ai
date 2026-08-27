#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from statistics import median


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
    p.add_argument("--geography", default="US")
    p.add_argument("--channel", default="offerup-sold-marked-listing")
    p.add_argument("--cohort", default="used-consumer")
    p.add_argument("--condition", default="used")
    p.add_argument("--currency", default="USD")
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    rows = []

    for m in load(a.catalog / "market.jsonl"):
        if m.get("synthetic", False) and not a.include_synthetic:
            continue
        price = m.get("price") or {}
        if m.get("geography") != a.geography:
            continue
        if m.get("channel") != a.channel:
            continue
        if m.get("cohort") != a.cohort:
            continue
        if m.get("condition") != a.condition:
            continue
        if price.get("currency") != a.currency:
            continue
        if m.get("price_state") != "SOLD_MARKED_LISTING_PRICE":
            continue

        listing = m.get("listing") or {}
        rows.append({
            "record_id": m.get("record_id"),
            "hardware_id": m.get("hardware_id"),
            "hardware": (hardware.get(m.get("hardware_id")) or {}).get("canonical_name", m.get("hardware_id")),
            "value": price.get("value"),
            "status": listing.get("status"),
            "confirmed": listing.get("confirmed_transaction_price"),
            "location": listing.get("location"),
            "title": listing.get("title"),
            "url": (m.get("source") or {}).get("url"),
        })

    rows.sort(key=lambda x: (str(x["hardware"]), str(x["record_id"])))

    groups = {}
    for x in rows:
        groups.setdefault(x["hardware_id"], []).append(x)

    print("SOLD-MARKED LISTING MARKET")
    print(f"observations={len(rows)}")
    print(f"hardware_groups={len(groups)}")
    print("price_semantics=SOLD-MARKED-LISTING-DISPLAY")
    print("confirmed_transaction_price=false")

    for hardware_id in sorted(groups, key=lambda hid: groups[hid][0]["hardware"]):
        items = groups[hardware_id]
        values = [x["value"] for x in items if isinstance(x["value"], (int, float))]
        if not values:
            continue
        print(
            f"GROUP hardware={items[0]['hardware']} | n={len(values)} | "
            f"median_displayed={median(values):g} {a.currency} | "
            f"min={min(values):g} | max={max(values):g}"
        )
        for x in items:
            print(
                f"- value={x['value']} {a.currency} | status={x['status']} | "
                f"confirmed_transaction_price={x['confirmed']} | "
                f"location={x['location']} | record={x['record_id']}"
            )

    if not rows:
        print("COVERAGE: EMPTY")
    else:
        print("COVERAGE: PRESENT")

    print("A SOLD page label does not prove that the displayed listing price equals the negotiated transaction amount.")
    print("median_displayed is a descriptive listing-page statistic, not a confirmed-sale median.")


if __name__ == "__main__":
    main()

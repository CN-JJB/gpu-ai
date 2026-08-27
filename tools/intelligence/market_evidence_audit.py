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


def sample_band(n):
    if not isinstance(n, (int, float)) or isinstance(n, bool) or n <= 0:
        return "UNKNOWN-SAMPLE"
    if n < 10:
        return "SMALL-SAMPLE"
    if n < 30:
        return "LIMITED-SAMPLE"
    return "BROAD-SAMPLE"


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

    as_of = date.fromisoformat(a.as_of)
    rows = []

    for m in load(a.catalog / "market.jsonl"):
        if m.get("synthetic", False) and not a.include_synthetic:
            continue

        price = m.get("price") or {}
        checks = (
            ("geography", a.geography, m.get("geography")),
            ("channel", a.channel, m.get("channel")),
            ("cohort", a.cohort, m.get("cohort")),
            ("condition", a.condition, m.get("condition")),
            ("price_state", a.price_state, m.get("price_state")),
            ("currency", a.currency, price.get("currency")),
        )
        if any(wanted is not None and str(actual) != wanted for _, wanted, actual in checks):
            continue

        sample = m.get("sample") or {}
        active = sample.get("active_listings")
        low = sample.get("range_low")
        high = sample.get("range_high")
        value = price.get("value")

        flags = [sample_band(active)]

        if m.get("price_state") == "MEDIAN_ASK":
            flags.append("ASK-ONLY")
        if sample.get("confirmed_sale") is False:
            flags.append("NOT-CONFIRMED-SALE")

        if m.get("revalidate_after"):
            stale = date.fromisoformat(str(m["revalidate_after"])) < as_of
            flags.append("STALE" if stale else "CURRENT")
        else:
            flags.append("UNSCHEDULED")

        range_ok = (
            isinstance(low, (int, float))
            and isinstance(high, (int, float))
            and isinstance(value, (int, float))
            and low <= value <= high
        )
        flags.append("MEDIAN-IN-RANGE" if range_ok else "RANGE-UNVERIFIED")

        rows.append({
            "record_id": m.get("record_id"),
            "hardware_id": m.get("hardware_id"),
            "price": value,
            "currency": price.get("currency"),
            "active": active,
            "range_low": low,
            "range_high": high,
            "methodology": sample.get("methodology"),
            "exported_at": (m.get("source") or {}).get("data_exported_at"),
            "flags": flags,
        })

    rows.sort(key=lambda x: str(x["record_id"]))

    print("MARKET EVIDENCE AUDIT")
    print(f"as_of={a.as_of}")
    print(f"observations={len(rows)}")

    counts = {}
    for x in rows:
        for flag in x["flags"]:
            counts[flag] = counts.get(flag, 0) + 1
        print(
            f"- record={x['record_id']} | price={x['price']} {x['currency']} | "
            f"active={x['active']} | range={x['range_low']}-{x['range_high']} | "
            f"method={x['methodology']} | exported_at={x['exported_at']} | "
            f"flags={','.join(x['flags'])}"
        )

    print("FLAG COUNTS")
    for key in sorted(counts):
        print(f"- {key}={counts[key]}")

    if not rows:
        print("AUDIT: EMPTY")
    else:
        print("AUDIT: PRESENT")

    print("Sample bands are descriptive heuristics, not statistical confidence scores.")
    print("ASK-ONLY observations must not be presented as confirmed sale prices.")


if __name__ == "__main__":
    main()

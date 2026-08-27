#!/usr/bin/env python3
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

VALID_STATES = {
    "ASK", "SOLD-CONFIRMED", "DELISTED-ASSUMED",
    "MERCHANT-QUOTE", "BUYBACK", "UNKNOWN"
}

def yes(v):
    return str(v).strip().lower() in {"true", "1", "yes", "y"}

def quartiles(values):
    if len(values) == 1:
        return values[0], values[0]
    q = statistics.quantiles(values, n=4, method="inclusive")
    return q[0], q[2]

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_market.py sample.csv")

    rows = list(csv.DictReader(Path(sys.argv[1]).open(encoding="utf-8")))
    groups = defaultdict(list)
    excluded = []

    for r in rows:
        if not yes(r.get("include_normalized")):
            excluded.append(r)
            continue

        state = r.get("price_state", "").strip()
        if state not in VALID_STATES:
            excluded.append({**r, "exclude_reason": f"invalid_price_state:{state}"})
            continue

        try:
            price = float(r["price_cny"]) + float(r.get("shipping_cny") or 0)
            vram = float(r["vram_gib"])
        except Exception:
            excluded.append({**r, "exclude_reason": "invalid_numeric_field"})
            continue

        key = (
            r["exact_model"].strip(),
            vram,
            r["cohort"].strip(),
            r["condition"].strip(),
            state,
        )
        groups[key].append(price)

    print(f"raw rows={len(rows)} normalized rows={sum(len(v) for v in groups.values())} excluded={len(excluded)}")
    print()

    for key in sorted(groups):
        vals = sorted(groups[key])
        q1, q3 = quartiles(vals)
        model, vram, cohort, condition, state = key
        print(
            f"{model} {vram:g}GiB | {cohort} | {condition} | {state} | "
            f"n={len(vals)} median={statistics.median(vals):.0f} "
            f"Q1={q1:.0f} Q3={q3:.0f} range={min(vals):.0f}-{max(vals):.0f} CNY"
        )

    if excluded:
        print()
        print("excluded rows:")
        for r in excluded:
            print("-", r.get("listing_id"), r.get("exclude_reason") or "<unspecified>")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import csv
import statistics
import sys
from pathlib import Path

TARGET_MODEL = "RTX 3090"
TARGET_VRAM = 24
TARGET_COHORT = "STOCK"
TARGET_CONDITION = "WORKING"

def b(s):
    return str(s).strip().lower() == "true"

def quartiles(values):
    if len(values) < 2:
        return (values[0], values[0]) if values else (None, None)
    qs = statistics.quantiles(values, n=4, method="inclusive")
    return qs[0], qs[2]

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: normalize_market.py sample.csv")

    rows = list(csv.DictReader(Path(sys.argv[1]).open(encoding="utf-8")))
    accepted = []
    excluded = []

    for r in rows:
        reasons = []
        if b(r["multi_sku"]):
            reasons.append("multi_sku")
        if not b(r["product_only"]):
            reasons.append("not_whole_product")
        if r["exact_model"] != TARGET_MODEL:
            reasons.append("wrong_or_unknown_model")
        try:
            vram = int(float(r["vram_gib"]))
        except Exception:
            vram = -1
        if vram != TARGET_VRAM:
            reasons.append("wrong_vram")
        if r["cohort"] != TARGET_COHORT:
            reasons.append("different_cohort")
        if r["condition"] != TARGET_CONDITION:
            reasons.append("condition_not_working")

        if reasons:
            excluded.append((r, reasons))
        else:
            accepted.append(r)

    print("SYNTHETIC MARKET DATA ONLY")
    print(f"raw rows: {len(rows)}")
    print(f"accepted target cohort: {len(accepted)}")
    print(f"excluded: {len(excluded)}")
    print()

    by_state = {}
    for r in accepted:
        by_state.setdefault(r["price_state"], []).append(float(r["price_cny"]))

    for state in sorted(by_state):
        vals = sorted(by_state[state])
        med = statistics.median(vals)
        q1, q3 = quartiles(vals)
        print(f"[{state}] n={len(vals)} median={med:.0f} CNY "
              f"Q1={q1:.0f} Q3={q3:.0f} range={min(vals):.0f}-{max(vals):.0f}")

    print()
    print("Excluded rows:")
    for r, reasons in excluded:
        print(f"- id={r['id']} price={r['price_cny']} reasons={','.join(reasons)} notes={r['notes']}")

if __name__ == "__main__":
    main()

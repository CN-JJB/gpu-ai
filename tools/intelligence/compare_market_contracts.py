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


def contract_key(m):
    p = m.get("price") or {}
    return (
        m.get("geography"),
        m.get("channel"),
        m.get("cohort"),
        m.get("condition"),
        m.get("price_state"),
        p.get("currency"),
    )


def match(m, args, side):
    price = m.get("price") or {}
    return (
        m.get("geography") == getattr(args, f"{side}_geography")
        and m.get("channel") == getattr(args, f"{side}_channel")
        and m.get("cohort") == getattr(args, f"{side}_cohort")
        and m.get("condition") == getattr(args, f"{side}_condition")
        and m.get("price_state") == getattr(args, f"{side}_price_state")
        and price.get("currency") == getattr(args, f"{side}_currency")
    )


def group(rows):
    out = {}
    for m in rows:
        value = (m.get("price") or {}).get("value")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            continue
        out.setdefault(m.get("hardware_id"), []).append(float(value))
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)

    for side in ("left", "right"):
        p.add_argument(f"--{side}-geography", required=True)
        p.add_argument(f"--{side}-channel", required=True)
        p.add_argument(f"--{side}-cohort", required=True)
        p.add_argument(f"--{side}-condition", required=True)
        p.add_argument(f"--{side}-price-state", required=True)
        p.add_argument(f"--{side}-currency", required=True)

    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    if a.left_currency != a.right_currency:
        raise SystemExit("cross-contract comparison requires the same currency")

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    market = [
        x for x in load(a.catalog / "market.jsonl")
        if a.include_synthetic or not x.get("synthetic", False)
    ]

    left_rows = [x for x in market if match(x, a, "left")]
    right_rows = [x for x in market if match(x, a, "right")]

    if not left_rows:
        raise SystemExit("left market contract has no observations")
    if not right_rows:
        raise SystemExit("right market contract has no observations")

    if len({contract_key(x) for x in left_rows}) != 1:
        raise SystemExit("left observations do not form one exact market contract")
    if len({contract_key(x) for x in right_rows}) != 1:
        raise SystemExit("right observations do not form one exact market contract")

    left = group(left_rows)
    right = group(right_rows)
    common = sorted(set(left) & set(right), key=lambda hid: (hardware.get(hid) or {}).get("canonical_name", hid))

    print("CROSS-MARKET SIGNAL COMPARE")
    print("comparison_semantics=CROSS-CONTRACT-DESCRIPTIVE")
    print(f"currency={a.left_currency}")
    print(f"common_hardware={len(common)}")

    for hid in common:
        lv = median(left[hid])
        rv = median(right[hid])
        gap = rv - lv
        pct = (rv / lv - 1.0) * 100.0
        name = (hardware.get(hid) or {}).get("canonical_name", hid)
        print(
            f"- hardware={name} | "
            f"left_n={len(left[hid])} | left_median={lv:g} | "
            f"right_n={len(right[hid])} | right_median={rv:g} | "
            f"gap={gap:g} | right_vs_left_pct={pct:.1f}%"
        )

    if not common:
        print("COMPARISON: NO-COMMON-HARDWARE")
    else:
        print("COMPARISON: PRESENT")

    print("The gap is between two different market contracts, not a confirmed transaction discount.")
    print("Do not use this output as fair value or a purchase recommendation.")


if __name__ == "__main__":
    main()

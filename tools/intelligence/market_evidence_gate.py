#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

VALID_GRADES = {"M0", "M1", "M2", "M3"}


def load(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def expected_grade(record):
    state = str(record.get("price_state", "")).upper()
    if record.get("synthetic", False):
        return "M0"
    if state == "SECONDARY_REPORTED":
        return "M1"
    if state == "MEDIAN_ASK":
        return "M2"
    if state == "SOLD_MARKED_LISTING_PRICE":
        return "M3"
    return None


def watchlist_gate(grade):
    return "ELIGIBLE" if grade in {"M2", "M3"} else "NEEDS-STRONGER-MARKET-EVIDENCE"


def transaction_amount_proven(record):
    state = str(record.get("price_state", "")).upper()
    if state == "SOLD_CONFIRMED":
        tx = record.get("transaction") or {}
        return tx.get("confirmed_price") is True
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--record-id", action="append")
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    hardware = {x["hardware_id"]: x for x in load(a.catalog / "hardware.jsonl")}
    rows = []

    for r in load(a.catalog / "market.jsonl"):
        if r.get("synthetic", False) and not a.include_synthetic:
            continue
        if a.record_id and r.get("record_id") not in set(a.record_id):
            continue

        grade = str(r.get("market_evidence_grade", "")).upper()
        expected = expected_grade(r)
        scope = str(r.get("market_evidence_scope", "")).strip()

        rows.append({
            "record_id": r.get("record_id"),
            "hardware": (hardware.get(r.get("hardware_id")) or {}).get("canonical_name", r.get("hardware_id")),
            "price_state": r.get("price_state"),
            "grade": grade,
            "expected": expected,
            "grade_match": expected is None or grade == expected,
            "scope": scope,
            "watchlist_gate": watchlist_gate(grade),
            "transaction_amount_proven": transaction_amount_proven(r),
        })

    rows.sort(key=lambda x: str(x["record_id"]))

    print("MARKET EVIDENCE GATE")
    print(f"observations={len(rows)}")

    counts = {}
    for x in rows:
        counts[x["grade"]] = counts.get(x["grade"], 0) + 1
        print(
            f"- record={x['record_id']} | hardware={x['hardware']} | "
            f"price_state={x['price_state']} | grade={x['grade']} | "
            f"expected_grade={x['expected']} | grade_match={x['grade_match']} | "
            f"watchlist_market_gate={x['watchlist_gate']} | "
            f"transaction_amount_proven={'YES' if x['transaction_amount_proven'] else 'NO'}"
        )
        print(f"  scope={x['scope']}")

    print("GRADE COUNTS")
    for grade in ("M0", "M1", "M2", "M3"):
        print(f"- {grade}={counts.get(grade, 0)}")

    bad = [x for x in rows if x["grade"] not in VALID_GRADES or not x["grade_match"] or not x["scope"]]
    if bad:
        print("GATE: INVALID")
        raise SystemExit(2)

    if not rows:
        print("GATE: EMPTY")
    else:
        print("GATE: PASS")

    print("M2/M3 may satisfy only the market-evidence component of Experiment 38.")
    print("They do not satisfy FIT, SOFTWARE, PERFORMANCE, CONDITION or price-ceiling gates.")
    print("M3 is claim-scoped: it does not imply a confirmed transaction amount unless that exact amount is independently proven.")


if __name__ == "__main__":
    main()

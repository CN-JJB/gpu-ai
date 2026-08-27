#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

PLACEHOLDERS = {"", "TODO", "TBD", "REPLACE", "UNKNOWN"}


def load(path):
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def present(value):
    return str(value if value is not None else "").strip().upper() not in PLACEHOLDERS


def number(name, value, minimum=None, maximum=None):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise SystemExit(f"{name} must be numeric")
    if minimum is not None and value < minimum:
        raise SystemExit(f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise SystemExit(f"{name} must be <= {maximum}")
    return float(value)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--case", type=Path, required=True)
    p.add_argument("--include-synthetic", action="store_true")
    a = p.parse_args()

    case = json.loads(a.case.read_text(encoding="utf-8"))
    markets = {x["record_id"]: x for x in load(a.catalog / "market.jsonl")}

    market_id = case.get("market_record_id")
    if market_id not in markets:
        raise SystemExit(f"unknown market_record_id: {market_id}")
    market = markets[market_id]

    if market.get("synthetic", False) and not a.include_synthetic:
        raise SystemExit("synthetic market observation requires --include-synthetic")

    if case.get("synthetic", False) and not a.include_synthetic:
        raise SystemExit("synthetic TCO case requires --include-synthetic")

    horizon = number("horizon_months", case.get("horizon_months"), 1)
    power = number("average_system_power_w", case.get("average_system_power_w"), 0)
    hours = number("hours_per_day", case.get("hours_per_day"), 0, 24)
    rate = number("electricity_rate_per_kwh", case.get("electricity_rate_per_kwh"), 0)
    platform = number("platform_delta", case.get("platform_delta"), 0)
    risk = number("risk_reserve", case.get("risk_reserve"), 0)
    resale = number("resale_estimate", case.get("resale_estimate"), 0)

    evidence = case.get("evidence")
    if not isinstance(evidence, dict):
        raise SystemExit("case.evidence object required")

    required_evidence = (
        "average_system_power_w",
        "electricity_rate_per_kwh",
        "platform_delta",
        "risk_reserve",
        "resale_estimate",
    )
    for field in required_evidence:
        if not present(evidence.get(field)):
            raise SystemExit(f"case.evidence.{field} required")

    price = market.get("price") or {}
    purchase = number("market price", price.get("value"), 0)
    currency = price.get("currency")
    if not present(currency):
        raise SystemExit("market price currency missing")

    days = 365.0 * horizon / 12.0
    energy_kwh = power / 1000.0 * hours * days
    electricity = energy_kwh * rate
    tco = purchase + platform + electricity + risk - resale

    print(f"CASE: {case.get('case_id', a.case.stem)}")
    print(f"HARDWARE: {market.get('hardware_id')}")
    print(f"MARKET RECORD: {market_id}")
    print(f"PURCHASE: {purchase:.2f} {currency}")
    print(f"HORIZON: {horizon:g} months")
    print(f"ENERGY: {energy_kwh:.3f} kWh")
    print(f"ELECTRICITY: {electricity:.2f} {currency}")
    print(f"PLATFORM DELTA: {platform:.2f} {currency}")
    print(f"RISK RESERVE: {risk:.2f} {currency}")
    print(f"RESALE ESTIMATE: -{resale:.2f} {currency}")
    print(f"TCO: {tco:.2f} {currency}")
    print("EVIDENCE / ASSUMPTIONS")
    for field in required_evidence:
        print(f"- {field}: {evidence[field]}")
    print(f"- purchase_price: market observation {market_id}")
    print("TCO is scenario output, not a feasibility gate or purchase recommendation.")


if __name__ == "__main__":
    main()

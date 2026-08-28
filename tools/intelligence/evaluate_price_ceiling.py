#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
from datetime import date
from pathlib import Path

from market_evidence_gate import expected_grade, freshness, watchlist_gate


POLICY_CONTRACT = "explicit-market-price-ceiling-v1"


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    if not Path(path).is_file():
        return []
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_object(path, label, errors):
    try:
        obj = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(obj, dict):
        errors.append(f"{label}: expected one JSON object")
        return {}
    return obj


def finite_positive(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0
    )


def finite_nonnegative(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) >= 0
    )


def build_price_ceiling_result(
    catalog,
    policy_path,
    as_of,
    allow_synthetic=False,
):
    catalog = Path(catalog)
    policy_path = Path(policy_path)
    errors = []

    if not policy_path.is_file():
        errors.append(f"price ceiling policy is not a file: {policy_path}")
        policy = {}
    else:
        policy = load_object(policy_path, "price ceiling policy", errors)

    try:
        as_of_date = date.fromisoformat(str(as_of))
    except ValueError:
        errors.append(f"invalid as_of date: {as_of}")
        as_of_date = None

    record = None
    if policy:
        if policy.get("price_ceiling_policy_schema_version") != 1:
            errors.append("price_ceiling_policy_schema_version must be 1")
        if not isinstance(policy.get("policy_id"), str) or not policy.get("policy_id"):
            errors.append("policy_id must be non-empty")
        if not isinstance(policy.get("market_record_id"), str) or not policy.get("market_record_id"):
            errors.append("market_record_id must be non-empty")
        if not isinstance(policy.get("hardware_id"), str) or not policy.get("hardware_id"):
            errors.append("hardware_id must be non-empty")

        ceiling = policy.get("max_sticker")
        if not isinstance(ceiling, dict):
            errors.append("max_sticker must be an object")
            ceiling = {}
        if not isinstance(ceiling.get("currency"), str) or not ceiling.get("currency"):
            errors.append("max_sticker.currency must be non-empty")
        if not finite_positive(ceiling.get("value")):
            errors.append("max_sticker.value must be finite and > 0")
        if not finite_nonnegative(policy.get("watch_band_pct")):
            errors.append("watch_band_pct must be finite and >= 0")

        rows = [
            x for x in load_jsonl(catalog / "market.jsonl")
            if x.get("record_id") == policy.get("market_record_id")
        ]
        if len(rows) != 1:
            errors.append(
                f"expected exactly one market record {policy.get('market_record_id')!r}, found {len(rows)}"
            )
        else:
            record = rows[0]

    market_state = None
    if record is not None and as_of_date is not None:
        if record.get("hardware_id") != policy.get("hardware_id"):
            errors.append("market record hardware_id does not match policy hardware_id")

        synthetic = bool(record.get("synthetic", False))
        if synthetic and not allow_synthetic:
            errors.append("synthetic market record requires explicit --allow-synthetic")

        grade = str(record.get("market_evidence_grade") or "").upper()
        expected = expected_grade(record)
        if expected is None or grade != expected:
            errors.append(
                f"market evidence grade mismatch: actual={grade!r} expected={expected!r}"
            )

        fresh = freshness(record, as_of_date)
        gate = watchlist_gate(grade, fresh)
        if gate != "ELIGIBLE":
            errors.append(f"market evidence is not Experiment 38 eligible: {gate}")

        price = record.get("price") or {}
        currency = price.get("currency")
        value = price.get("value")
        if currency != (policy.get("max_sticker") or {}).get("currency"):
            errors.append(
                "market price currency does not match max_sticker currency; no FX conversion is inferred"
            )
        if not finite_positive(value):
            errors.append("market price value must be finite and > 0")

        market_state = {
            "record_id": record.get("record_id"),
            "hardware_id": record.get("hardware_id"),
            "price_state": record.get("price_state"),
            "currency": currency,
            "value": float(value) if finite_positive(value) else value,
            "market_evidence_grade": grade,
            "freshness": fresh,
            "synthetic": synthetic,
        }

    result = None
    if not errors and market_state is not None:
        ask = market_state["value"]
        ceiling = float(policy["max_sticker"]["value"])
        band = float(policy["watch_band_pct"])
        watch_limit = ceiling * (1.0 + band / 100.0)

        if ask <= ceiling:
            decision = "WITHIN-CEILING"
        elif ask <= watch_limit:
            decision = "WATCH-BAND"
        else:
            decision = "ABOVE-BAND"

        result = {
            "price_ceiling_result_schema_version": 1,
            "policy_contract": POLICY_CONTRACT,
            "policy_id": policy["policy_id"],
            "market_record_id": policy["market_record_id"],
            "hardware_id": policy["hardware_id"],
            "as_of": str(as_of),
            "synthetic_input": market_state["synthetic"],
            "market": market_state,
            "policy": {
                "max_sticker": {
                    "currency": policy["max_sticker"]["currency"],
                    "value": ceiling,
                },
                "watch_band_pct": band,
                "watch_limit": watch_limit,
            },
            "decision": decision,
            "evidence": {
                "policy_sha256": sha256_file(policy_path),
                "market_catalog_sha256": sha256_file(catalog / "market.jsonl"),
            },
            "scope": "EXPLICIT_PERSONAL_PRICE_POLICY_NO_FX_NO_AUTO_BUY",
        }

    return {"errors": errors, "result": result}


def main():
    p = argparse.ArgumentParser(
        description=(
            "Evaluate an explicit personal sticker-price ceiling against one current "
            "Experiment 38-eligible market observation."
        )
    )
    p.add_argument("catalog", type=Path)
    p.add_argument("--policy", type=Path, required=True)
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--allow-synthetic", action="store_true")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()

    built = build_price_ceiling_result(
        a.catalog,
        a.policy,
        a.as_of,
        allow_synthetic=a.allow_synthetic,
    )

    print("PRICE CEILING POLICY")
    print("ERRORS")
    for error in built["errors"]:
        print("- " + error)

    if built["errors"] or built["result"] is None:
        print("PRICE CEILING: BLOCKED")
        raise SystemExit(2)

    result = built["result"]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"market={result['market']['value']} {result['market']['currency']} | "
        f"ceiling={result['policy']['max_sticker']['value']} | "
        f"watch_limit={result['policy']['watch_limit']}"
    )
    print(f"synthetic_input={result['synthetic_input']}")
    print(f"PRICE CEILING: {result['decision']}")
    print(f"out={a.out}")
    print(
        "WITHIN-CEILING is not BUY. This result only applies the explicit personal "
        "price policy to the selected current market observation."
    )


if __name__ == "__main__":
    main()

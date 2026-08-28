#!/usr/bin/env python3
import argparse
from pathlib import Path

from evaluate_price_ceiling import build_price_ceiling_result, load_object


def verify_price_ceiling_result(
    result_path,
    catalog,
    policy_path,
    as_of,
    allow_synthetic=False,
):
    result_path = Path(result_path)
    errors = []
    supplied = {}
    if not result_path.is_file():
        errors.append(f"price ceiling result is not a file: {result_path}")
    else:
        supplied = load_object(result_path, "price ceiling result", errors)

    rebuilt = build_price_ceiling_result(
        catalog,
        policy_path,
        as_of,
        allow_synthetic=allow_synthetic,
    )
    errors.extend("source evidence: " + x for x in rebuilt["errors"])
    expected = rebuilt["result"]
    if expected is not None and supplied != expected:
        errors.append(
            "price ceiling result does not exactly match independently rebuilt "
            "market evidence + personal policy"
        )
    return {"errors": errors, "supplied": supplied, "expected": expected}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("catalog", type=Path)
    p.add_argument("--result", type=Path, required=True)
    p.add_argument("--policy", type=Path, required=True)
    p.add_argument("--as-of", required=True)
    p.add_argument("--allow-synthetic", action="store_true")
    a = p.parse_args()

    verified = verify_price_ceiling_result(
        a.result,
        a.catalog,
        a.policy,
        a.as_of,
        allow_synthetic=a.allow_synthetic,
    )
    print("PRICE CEILING VERIFICATION")
    print("ERRORS")
    for error in verified["errors"]:
        print("- " + error)
    if verified["errors"]:
        print("PRICE CEILING ARTIFACT: BLOCKED")
        raise SystemExit(2)
    print("PRICE CEILING ARTIFACT: PASS")
    print("The result is exactly reproducible from the selected market record and policy.")


if __name__ == "__main__":
    main()

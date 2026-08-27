#!/usr/bin/env python3

import argparse
import json


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def get(obj, *keys):
    value = obj

    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)

    return value


def ratio(a, b):
    if not isinstance(a, (int, float)):
        return None
    if not isinstance(b, (int, float)) or b == 0:
        return None
    return a / b


def fmt(value):
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline")
    parser.add_argument("speculative")
    args = parser.parse_args()

    base = load(args.baseline)
    spec = load(args.speculative)

    base_tps = get(base, "summary", "server_predicted_tps")
    spec_tps = get(spec, "summary", "server_predicted_tps")
    base_wall = get(base, "response", "wall_s")
    spec_wall = get(spec, "response", "wall_s")

    print(f"baseline: {args.baseline}")
    print(f"spec:     {args.speculative}")
    print()
    print(
        "server decode speedup: "
        f"{fmt(ratio(spec_tps, base_tps))}x"
    )
    print(
        "wall latency speedup: "
        f"{fmt(ratio(base_wall, spec_wall))}x"
    )
    print(
        "spec acceptance: "
        f"{fmt(get(spec, 'summary', 'acceptance_rate'))}"
    )
    print(
        "spec accepted/draft-round: "
        f"{fmt(get(spec, 'summary', 'accepted_tokens_per_draft_round'))}"
    )
    print(
        "baseline decode calls/output: "
        f"{fmt(get(base, 'summary', 'decode_calls_per_output_token'))}"
    )
    print(
        "spec decode calls/output: "
        f"{fmt(get(spec, 'summary', 'decode_calls_per_output_token'))}"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

FILES = (
    "hardware.jsonl",
    "models.jsonl",
    "runtimes.jsonl",
    "market.jsonl",
    "compatibility.jsonl",
    "benchmarks.jsonl",
)


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
    p.add_argument("--as-of", default=date.today().isoformat())
    p.add_argument("--within-days", type=int, default=30)
    p.add_argument("--include-synthetic", action="store_true")
    p.add_argument("--show-unscheduled", action="store_true")
    a = p.parse_args()

    if a.within_days < 0:
        raise SystemExit("--within-days must be >= 0")

    as_of = date.fromisoformat(a.as_of)
    scheduled = []
    unscheduled = []

    for name in FILES:
        for r in load(a.catalog / name):
            if r.get("synthetic", False) and not a.include_synthetic:
                continue

            rid = r.get("record_id", "<missing>")
            revalidate = r.get("revalidate_after")
            if not revalidate:
                unscheduled.append((name, r))
                continue

            d = date.fromisoformat(str(revalidate))
            delta = (d - as_of).days
            if delta < 0:
                state = "STALE"
            elif delta == 0:
                state = "DUE-TODAY"
            elif delta <= a.within_days:
                state = "DUE-SOON"
            else:
                state = "FRESH"

            scheduled.append({
                "state": state,
                "days": delta,
                "revalidate_after": d.isoformat(),
                "record_id": rid,
                "record_type": r.get("record_type"),
                "source_file": name,
                "observed_at": r.get("observed_at") or (r.get("source") or {}).get("observed_at"),
            })

    state_order = {"STALE": 0, "DUE-TODAY": 1, "DUE-SOON": 2, "FRESH": 3}
    scheduled.sort(
        key=lambda x: (
            state_order.get(x["state"], 9),
            x["revalidate_after"],
            x["record_id"],
        )
    )

    counts = {}
    for x in scheduled:
        counts[x["state"]] = counts.get(x["state"], 0) + 1

    print("INTELLIGENCE FRESHNESS")
    print(f"as_of={a.as_of}")
    print(f"within_days={a.within_days}")
    print(f"scheduled={len(scheduled)}")
    print(f"unscheduled={len(unscheduled)}")

    print("STATE COUNTS")
    for state in ("STALE", "DUE-TODAY", "DUE-SOON", "FRESH"):
        print(f"- {state}={counts.get(state, 0)}")

    print("REVALIDATION QUEUE")
    for x in scheduled:
        if x["state"] == "FRESH":
            continue
        print(
            f"- state={x['state']} | days={x['days']} | "
            f"revalidate_after={x['revalidate_after']} | "
            f"type={x['record_type']} | record={x['record_id']} | "
            f"observed={x['observed_at']} | file={x['source_file']}"
        )

    if a.show_unscheduled:
        print("UNSCHEDULED")
        for name, r in sorted(unscheduled, key=lambda p: str(p[1].get("record_id", ""))):
            print(
                f"- type={r.get('record_type')} | "
                f"record={r.get('record_id')} | file={name}"
            )

    if counts.get("STALE", 0):
        print("FRESHNESS: STALE-REVALIDATION-REQUIRED")
    elif counts.get("DUE-TODAY", 0) or counts.get("DUE-SOON", 0):
        print("FRESHNESS: REVALIDATION-QUEUE-PRESENT")
    else:
        print("FRESHNESS: CURRENT-WITHIN-WINDOW")

    print("Stale means revalidation is required; it does not automatically mean the old observation is false.")


if __name__ == "__main__":
    main()

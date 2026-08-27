#!/usr/bin/env python3
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

def parse_date(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None

def evidence_ok(market, condition):
    return market in {"M2","M3"} and condition in {"C3","C4"}

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: evaluate_watchlist.py watchlist.csv")

    rows = list(csv.DictReader(Path(sys.argv[1]).open(encoding="utf-8")))
    now = datetime.now(timezone.utc)

    for r in rows:
        try:
            ask = float(r["ask_cny"])
            ceiling = float(r["max_sticker_cny"])
            band = float(r.get("watch_band_pct") or 10)
        except Exception:
            print(r.get("candidate"), "INVALID NUMERIC DATA")
            continue

        if r["fit"] == "FAIL" or r["software"] == "FAIL" or r["performance"] == "FAIL":
            status = "SKIP"
        elif "UNKNOWN" in {r["fit"], r["software"], r["performance"]}:
            status = "NEEDS EVIDENCE"
        elif not evidence_ok(r["market_evidence"], r["condition_evidence"]):
            status = "NEEDS EVIDENCE"
        elif ask <= ceiling:
            status = "BUY-CANDIDATE"
        elif ask <= ceiling * (1 + band/100):
            status = "WATCH"
        else:
            status = "OVERPRICED"

        observed = parse_date(r["observed_at"])
        stale = "UNKNOWN"
        if observed is not None:
            if observed.tzinfo is None:
                observed = observed.replace(tzinfo=timezone.utc)
            age_days = (now - observed.astimezone(timezone.utc)).total_seconds()/86400
            stale = "YES" if age_days > 7 else "NO"

        print(
            f"{r['candidate']}: {status} | ask={ask:.0f} ceiling={ceiling:.0f} "
            f"| market={r['market_evidence']} condition={r['condition_evidence']} "
            f"| stale={stale}"
        )

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


def parse_datetime(s):
    try:
        value = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except Exception:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def evidence_ok(market, condition):
    return market in {"M2", "M3"} and condition in {"C3", "C4"}


def freshness_state(row, now):
    revalidate = str(row.get("revalidate_after") or "").strip()
    if revalidate:
        d = parse_datetime(revalidate)
        if d is None:
            return "INVALID"
        if d.date() < now.date():
            return "STALE"
        if d.date() == now.date():
            return "DUE-TODAY"
        return "CURRENT"

    observed = parse_datetime(row.get("observed_at"))
    if observed is None:
        return "UNKNOWN"

    age_days = (now - observed).total_seconds() / 86400
    return "STALE" if age_days > 7 else "CURRENT"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("watchlist", type=Path)
    p.add_argument("--as-of")
    a = p.parse_args()

    rows = list(csv.DictReader(a.watchlist.open(encoding="utf-8")))
    now = parse_datetime(a.as_of) if a.as_of else datetime.now(timezone.utc)
    if now is None:
        raise SystemExit("invalid --as-of")

    for r in rows:
        try:
            ask = float(r["ask_cny"])
            ceiling = float(r["max_sticker_cny"])
            band = float(r.get("watch_band_pct") or 10)
        except Exception:
            print(r.get("candidate"), "INVALID NUMERIC DATA")
            continue

        freshness = freshness_state(r, now)

        if r["fit"] == "FAIL" or r["software"] == "FAIL" or r["performance"] == "FAIL":
            status = "SKIP"
        elif "UNKNOWN" in {r["fit"], r["software"], r["performance"]}:
            status = "NEEDS EVIDENCE"
        elif freshness in {"STALE", "DUE-TODAY", "UNKNOWN", "INVALID"}:
            status = "NEEDS EVIDENCE"
        elif not evidence_ok(r["market_evidence"], r["condition_evidence"]):
            status = "NEEDS EVIDENCE"
        elif ask <= ceiling:
            status = "BUY-CANDIDATE"
        elif ask <= ceiling * (1 + band / 100):
            status = "WATCH"
        else:
            status = "OVERPRICED"

        stale = "YES" if freshness == "STALE" else ("UNKNOWN" if freshness in {"UNKNOWN", "INVALID"} else "NO")

        print(
            f"{r['candidate']}: {status} | ask={ask:.0f} ceiling={ceiling:.0f} "
            f"| market={r['market_evidence']} condition={r['condition_evidence']} "
            f"| freshness={freshness} stale={stale}"
        )


if __name__ == "__main__":
    main()

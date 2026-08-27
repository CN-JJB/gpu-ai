#!/usr/bin/env python3
import argparse,csv
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("scenarios",type=Path)
    a=p.parse_args()

    rows=list(csv.DictReader(a.scenarios.open(encoding="utf-8")))
    if not rows:
        raise SystemExit("empty scenarios")

    print("SYNTHETIC HOST-MEMORY RECLAIM MODEL")
    for r in rows:
        name=r["name"]
        ram=float(r["ram_gib"])
        anon=float(r["anonymous_gib"])
        cache=float(r["file_cache_gib"])
        other=float(r["kernel_other_gib"])
        frac=float(r["reclaimable_cache_fraction"])
        req=float(r["new_request_gib"])

        if min(ram,anon,cache,other,req)<0 or not 0<=frac<=1:
            raise SystemExit(f"invalid scenario: {name}")

        free=ram-anon-cache-other
        if free<0:
            raise SystemExit(f"overcommitted physical accounting: {name}")

        reclaim=cache*frac
        available_proxy=free+reclaim
        shortfall=max(req-available_proxy,0)

        if req<=free:
            cls="FITS_WITH_FREE"
        elif req<=available_proxy:
            cls="FITS_AFTER_SYNTHETIC_CACHE_RECLAIM"
        else:
            cls="PRESSURE_BEYOND_SYNTHETIC_RECLAIM"

        print(name)
        print(f"  free_GiB: {free:.3f}")
        print(f"  synthetic_reclaimable_cache_GiB: {reclaim:.3f}")
        print(f"  available_proxy_GiB: {available_proxy:.3f}")
        print(f"  request_GiB: {req:.3f}")
        print(f"  shortfall_GiB: {shortfall:.3f}")
        print(f"  classification: {cls}")
        print()

    print("WARNING: available_proxy is NOT Linux MemAvailable.")
    print("It is a teaching model for reclaim intuition only.")

if __name__=="__main__":
    main()

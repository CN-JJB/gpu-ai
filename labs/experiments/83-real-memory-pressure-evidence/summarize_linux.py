#!/usr/bin/env python3
import argparse,csv
from pathlib import Path

def f(row,key):
    v=row.get(key,"")
    return None if v=="" else float(v)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("timeline",type=Path)
    a=p.parse_args()

    rows=list(csv.DictReader(a.timeline.open(encoding="utf-8")))
    if len(rows)<2:
        raise SystemExit("need at least two samples")

    first,last=rows[0],rows[-1]
    total=f(last,"MemTotal_kB")
    avail0=f(first,"MemAvailable_kB")
    avail1=f(last,"MemAvailable_kB")
    free1=f(last,"MemFree_kB")
    cached1=f(last,"Cached_kB")

    def delta(key):
        a0=f(first,key);a1=f(last,key)
        return None if a0 is None or a1 is None else a1-a0

    print("LINUX MEMORY WINDOW SUMMARY")
    if total and avail1 is not None:
        print(f"last MemAvailable: {avail1/total*100:.3f}% of MemTotal")
    if total and free1 is not None:
        print(f"last MemFree: {free1/total*100:.3f}% of MemTotal")
    if total and cached1 is not None:
        print(f"last Cached: {cached1/total*100:.3f}% of MemTotal")

    for key in ["pswpin","pswpout","pgmajfault","pgfault","oom_kill"]:
        d=delta(key)
        print(f"delta {key}: {'UNKNOWN' if d is None else int(d)}")

    print()
    hints=[]
    if total and free1 is not None and avail1 is not None and cached1 is not None:
        if free1/total<0.05 and avail1/total>0.20 and cached1/total>0.20:
            hints.append(
                "LOW_FREE_BUT_AVAILABLE: low MemFree with healthy MemAvailable/high cache can be normal"
            )

    psout=delta("pswpout")
    maj=delta("pgmajfault")
    if total and avail0 is not None and avail1 is not None:
        drop=(avail0-avail1)/total
        if drop>0.10 and (psout or 0)>0 and (maj or 0)>0:
            hints.append(
                "HOST_PRESSURE_COMPATIBLE: MemAvailable fell while swap-out and major faults increased"
            )

    oom=delta("oom_kill")
    if oom is not None and oom>0:
        hints.append(
            "OOM_EVENT_OBSERVED: kernel vmstat oom_kill counter increased in the window"
        )

    if not hints:
        hints.append("NO_SIMPLE_PATTERN: inspect raw timeline/process/GPU/log evidence")

    for x in hints:
        print("- "+x)

    print()
    print("These are evidence-compatible hints, not universal root-cause proof.")

if __name__=="__main__":
    main()

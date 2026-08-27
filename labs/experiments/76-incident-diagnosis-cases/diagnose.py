#!/usr/bin/env python3
import argparse,csv,statistics
from pathlib import Path

def rows(path):
    out=[]
    for r in csv.DictReader(Path(path).open(encoding="utf-8")):
        out.append({k:float(v) for k,v in r.items()})
    if len(out)<2:
        raise SystemExit("need at least two samples")
    return out

def ratio(a,b):
    return float("inf") if a==0 and b>0 else (1.0 if a==0 else b/a)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("csv")
    a=p.parse_args()
    r=rows(a.csv)
    first,last=r[0],r[-1]

    ttft_r=ratio(first["ttft_p95_ms"],last["ttft_p95_ms"])
    itl_r=ratio(first["itl_p95_ms"],last["itl_p95_ms"])
    clock_r=ratio(first["sm_clock_mhz"],last["sm_clock_mhz"])
    deferred_delta=last["requests_deferred"]-first["requests_deferred"]
    temp_delta=last["temp_c"]-first["temp_c"]
    vram_range=max(x["vram_used_gib"] for x in r)-min(x["vram_used_gib"] for x in r)
    max_vram_frac=max(x["vram_used_gib"]/x["vram_total_gib"] for x in r)

    hypotheses=[]

    if deferred_delta>=3 and ttft_r>=2 and itl_r<1.25 and clock_r>0.9:
        hypotheses.append(
            "QUEUE_PRESSURE_COMPATIBLE: TTFT/deferred rose while ITL/clocks stayed relatively stable"
        )

    if temp_delta>=10 and clock_r<=0.8 and itl_r>=1.3:
        hypotheses.append(
            "THERMAL_CLOCK_HYPOTHESIS: temperature rose, clocks fell, and ITL worsened"
        )

    if max_vram_frac>=0.90 and vram_range<=0.25 and ttft_r<1.25 and itl_r<1.25:
        hypotheses.append(
            "HIGH_STABLE_VRAM: high VRAM alone is not leak evidence in this trace"
        )

    print("INCIDENT CASE SUMMARY")
    print(f"samples: {len(r)}")
    print(f"TTFT ratio last/first: {ttft_r:.3f}x")
    print(f"ITL ratio last/first: {itl_r:.3f}x")
    print(f"deferred delta: {deferred_delta:.3f}")
    print(f"clock ratio last/first: {clock_r:.3f}x")
    print(f"temperature delta: {temp_delta:.3f} C")
    print(f"VRAM range: {vram_range:.3f} GiB")
    print(f"max VRAM fraction: {max_vram_frac*100:.3f}%")
    print()
    if hypotheses:
        for h in hypotheses:
            print("- "+h)
    else:
        print("- NO_SIMPLE_PATTERN: collect more evidence")

    print()
    print("These are evidence-compatible hypotheses, not proven root causes.")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse,csv,statistics
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("trace",type=Path)
    a=p.parse_args()

    rows=[]
    for r in csv.DictReader(a.trace.open(encoding="utf-8")):
        rows.append({k:float(v) for k,v in r.items()})
    if len(rows)<4:
        raise SystemExit("need at least four samples")

    first,last=rows[0],rows[-1]
    tg_ratio=last["tg_tok_s"]/first["tg_tok_s"]
    clock_ratio=last["clock_mhz"]/first["clock_mhz"]
    temp_delta=last["temp_c"]-first["temp_c"]
    power_ratio=last["power_w"]/first["power_w"]

    q=max(1,len(rows)//4)
    first_window=statistics.mean(x["tg_tok_s"] for x in rows[:q])
    last_window=statistics.mean(x["tg_tok_s"] for x in rows[-q:])
    window_drift=last_window/first_window-1

    print("SUSTAINED PERFORMANCE TRACE")
    print(f"samples: {len(rows)}")
    print(f"temperature delta: {temp_delta:.3f} C")
    print(f"clock ratio last/first: {clock_ratio:.6f}x")
    print(f"TG ratio last/first: {tg_ratio:.6f}x")
    print(f"power ratio last/first: {power_ratio:.6f}x")
    print(f"first-window TG: {first_window:.6f}")
    print(f"last-window TG: {last_window:.6f}")
    print(f"window TG drift: {window_drift*100:.3f}%")
    print()

    hints=[]
    if temp_delta>=15 and clock_ratio<=0.85 and tg_ratio<=0.90:
        hints.append(
            "THERMAL_CLOCK_PERF_DRIFT_COMPATIBLE: strong temperature rise accompanies clock/performance decline"
        )
    if abs(window_drift)<=0.03 and clock_ratio>=0.97:
        hints.append(
            "SUSTAINED_STABLE: performance/clocks remain stable in this synthetic window"
        )
    if temp_delta<10 and clock_ratio<=0.90 and tg_ratio<=0.90:
        hints.append(
            "CLOCK_PERF_DRIFT_WITHOUT_LARGE_THERMAL_RISE: investigate power/other limiter evidence"
        )

    if not hints:
        hints.append("NO_SIMPLE_PATTERN: inspect complete timeline and vendor limiter evidence")

    for h in hints:
        print("- "+h)
    print()
    print("Pattern classification is not proof of the exact physical limiter.")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse,json,statistics
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    a=p.parse_args()

    m=json.loads(a.manifest.read_text(encoding="utf-8"))
    ts=[float(x) for x in m["samples_ts"]]
    ns=[int(x) for x in m["samples_ns"]]

    if len(ts)<4 or len(ts)!=len(ns):
        raise SystemExit("invalid sustained sample arrays")

    q=max(1,len(ts)//4)
    first=statistics.mean(ts[:q])
    last=statistics.mean(ts[-q:])
    drift=last/first-1

    cumulative=0.0
    print("SUSTAINED TG SUMMARY")
    print(f"samples: {len(ts)}")
    print(f"first-quartile mean TG: {first:.6f}")
    print(f"last-quartile mean TG: {last:.6f}")
    print(f"TG drift: {drift*100:.3f}%")
    print(f"min TG: {min(ts):.6f}")
    print(f"max TG: {max(ts):.6f}")
    print()
    print("APPROX SAMPLE TIMELINE")
    for i,(rate,dur_ns) in enumerate(zip(ts,ns)):
        dur=dur_ns/1e9
        start=cumulative
        cumulative += dur
        print(
            f"{i:02d}: approx {start:.3f}-{cumulative:.3f}s "
            f"TG={rate:.6f} tok/s"
        )
    print()
    print("Approx timeline assumes measured repetitions are contiguous;")
    print("correlate with raw telemetry and benchmark wall start/end.")

if __name__=="__main__":
    main()

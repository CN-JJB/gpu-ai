#!/usr/bin/env python3
import argparse,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("trace",type=Path)
    a=p.parse_args()
    data=json.loads(a.trace.read_text(encoding="utf-8"))

    print("LIFECYCLE TIMELINE")
    for r in data["runs"]:
        s=r["spawn_ms"]
        h=r["first_http_ms"]
        ready=r["ready_ms"]
        infer=r["first_inference_done_ms"]
        warm=r["warm_request_ms"]

        if not s <= h <= ready <= infer:
            raise SystemExit(f"invalid state ordering: {r['name']}")

        print(r["name"])
        print(f"  first HTTP: {h-s} ms after spawn")
        print(f"  readiness: {ready-s} ms after spawn")
        print(f"  first inference complete: {infer-s} ms after spawn")
        print(f"  post-ready first inference: {infer-ready} ms")
        print(f"  later warm request: {warm} ms")
        print()

    a0=data["runs"][0]
    a1=data["runs"][1]
    print("RESTART DELTA")
    print(f"  readiness delta: {(a1['ready_ms']-a1['spawn_ms'])-(a0['ready_ms']-a0['spawn_ms'])} ms")
    print("  lesson: first HTTP, ready, first inference, warm are separate states")

if __name__=="__main__":
    main()

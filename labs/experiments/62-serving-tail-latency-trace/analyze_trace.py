#!/usr/bin/env python3
import argparse
import csv
import math
import statistics
from pathlib import Path

def pct(values, p):
    if not values:
        return None
    vals = sorted(values)
    rank = max(1, math.ceil(p * len(vals)))
    return vals[rank - 1]

def fmt(v):
    return "n/a" if v is None else f"{v:.3f}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("trace", type=Path)
    p.add_argument("--ttft-slo-ms", type=float, default=500.0)
    p.add_argument("--itl-slo-ms", type=float, default=80.0)
    p.add_argument("--required-compliance", type=float, default=0.99)
    a = p.parse_args()

    rows = list(csv.DictReader(a.trace.open(encoding="utf-8")))
    if not rows:
        raise SystemExit("empty trace")

    ttft=[]
    queue=[]
    e2e=[]
    itl=[]
    outputs=[]

    for r in rows:
        arrival=float(r["arrival_ms"])
        service=float(r["service_start_ms"])
        first=float(r["first_token_ms"])
        done=float(r["complete_ms"])
        nout=int(r["output_tokens"])

        if not (arrival <= service <= first <= done):
            raise SystemExit(f"invalid timeline for {r['request_id']}")
        if nout < 1:
            raise SystemExit(f"output_tokens must be >=1: {r['request_id']}")

        q=service-arrival
        t=first-arrival
        e=done-arrival
        i=None if nout==1 else (done-first)/(nout-1)

        queue.append(q)
        ttft.append(t)
        e2e.append(e)
        outputs.append(nout)
        if i is not None:
            itl.append(i)

    start=min(float(r["arrival_ms"]) for r in rows)
    end=max(float(r["complete_ms"]) for r in rows)
    makespan_s=(end-start)/1000.0

    passes=0
    for r in rows:
        arrival=float(r["arrival_ms"])
        first=float(r["first_token_ms"])
        done=float(r["complete_ms"])
        nout=int(r["output_tokens"])
        t=first-arrival
        i=0.0 if nout==1 else (done-first)/(nout-1)
        if t <= a.ttft_slo_ms and i <= a.itl_slo_ms:
            passes += 1

    compliance=passes/len(rows)

    print("TRACE SUMMARY")
    print(f"requests: {len(rows)}")
    print("percentile estimator: nearest-rank ceil(p*N)")
    print()
    print("TTFT ms")
    print(f"  mean: {statistics.mean(ttft):.3f}")
    print(f"  p50:  {fmt(pct(ttft,0.50))}")
    print(f"  p95:  {fmt(pct(ttft,0.95))}")
    print(f"  p99:  {fmt(pct(ttft,0.99))}")
    print("queue ms")
    print(f"  mean: {statistics.mean(queue):.3f}")
    print(f"  p95:  {fmt(pct(queue,0.95))}")
    print("E2E ms")
    print(f"  mean: {statistics.mean(e2e):.3f}")
    print(f"  p95:  {fmt(pct(e2e,0.95))}")
    print("request mean-ITL ms")
    print(f"  mean: {statistics.mean(itl):.3f}")
    print(f"  p95:  {fmt(pct(itl,0.95))}")
    print()
    print(f"makespan: {makespan_s:.3f} s")
    print(f"request throughput: {len(rows)/makespan_s:.3f} req/s")
    print(f"output token throughput: {sum(outputs)/makespan_s:.3f} tok/s")
    print()
    print(
        f"SLO per request: TTFT <= {a.ttft_slo_ms:g} ms AND "
        f"mean-ITL <= {a.itl_slo_ms:g} ms"
    )
    print(f"compliance: {compliance*100:.3f}% ({passes}/{len(rows)})")
    print(f"required: {a.required_compliance*100:.3f}%")
    print("SLO: " + ("PASS" if compliance >= a.required_compliance else "FAIL"))

if __name__ == "__main__":
    main()

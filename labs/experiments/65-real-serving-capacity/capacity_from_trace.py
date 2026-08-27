#!/usr/bin/env python3
import argparse
import csv
import statistics
from pathlib import Path

def num(v):
    if v is None or str(v).strip()=="":
        return None
    return float(v)

def peak(intervals):
    events=[]
    for a,b in intervals:
        if b<=a:
            continue
        events.append((a,1))
        events.append((b,-1))
    events.sort(key=lambda x:(x[0],x[1]))
    cur=0
    best=0
    for _,d in events:
        cur += d
        best=max(best,cur)
    return best

def main():
    p=argparse.ArgumentParser()
    p.add_argument("requests_csv",type=Path)
    p.add_argument("--kv-gib-per-active",type=float)
    a=p.parse_args()

    rows=list(csv.DictReader(a.requests_csv.open(encoding="utf-8")))
    rows=[r for r in rows if r.get("status","ok")=="ok"]
    if not rows:
        raise SystemExit("no successful requests")

    system=[]
    e2e=[]
    active=[]
    queue=[]
    have_service=True

    for r in rows:
        start=num(r.get("client_send_ms"))
        done=num(r.get("complete_ms"))
        if start is None or done is None:
            raise SystemExit("client_send_ms/complete_ms required")
        if done<start:
            raise SystemExit(f"invalid interval: {r.get('request_id')}")
        system.append((start,done))
        e2e.append((done-start)/1000)

        ss=num(r.get("service_start_ms"))
        if ss is None:
            have_service=False
        else:
            if not start <= ss <= done:
                raise SystemExit(f"invalid service_start_ms: {r.get('request_id')}")
            active.append((ss,done))
            queue.append((start,ss))

    start=min(x[0] for x in system)
    end=max(x[1] for x in system)
    horizon_s=(end-start)/1000
    lam=len(rows)/horizon_s
    area_system=sum((b-a)/1000 for a,b in system)
    lsystem=area_system/horizon_s
    mean_w=statistics.mean(e2e)

    print("REAL TRACE CAPACITY SUMMARY")
    print(f"successful requests: {len(rows)}")
    print(f"horizon: {horizon_s:.6f} s")
    print(f"completed throughput lambda: {lam:.6f} req/s")
    print(f"mean client E2E W_system: {mean_w:.6f} s")
    print(f"lambda*W_system: {lam*mean_w:.6f}")
    print(f"trace-area L_system: {lsystem:.6f}")
    print(f"peak client in-system requests: {peak(system)}")

    if have_service:
        wactive=[(b-a)/1000 for a,b in active]
        wqueue=[(b-a)/1000 for a,b in queue]
        la=sum(wactive)/horizon_s
        lq=sum(wqueue)/horizon_s
        print()
        print(f"mean W_active: {statistics.mean(wactive):.6f} s")
        print(f"L_active: {la:.6f}")
        print(f"peak active: {peak(active)}")
        print(f"mean W_queue: {statistics.mean(wqueue):.6f} s")
        print(f"L_queue: {lq:.6f}")
        print(f"peak queue: {peak(queue)}")
        if a.kv_gib_per_active is not None:
            print(f"average active KV proxy: {la*a.kv_gib_per_active:.3f} GiB")
            print(f"peak active KV proxy: {peak(active)*a.kv_gib_per_active:.3f} GiB")
            print("WARNING: constant KV/sequence is only a planning proxy.")
    else:
        print()
        print("service_start_ms unavailable:")
        print("- L_system includes queue/network/service.")
        print("- cannot derive L_active or active KV from this trace.")
        if a.kv_gib_per_active is not None:
            print("- refusing active-KV estimate without service-start evidence.")

    print()
    print("WARNING: finite-batch identity does not prove a representative steady-state workload.")

if __name__=="__main__":
    main()

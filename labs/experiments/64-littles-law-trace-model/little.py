#!/usr/bin/env python3
import argparse
import csv
import statistics
from pathlib import Path

def peak(intervals):
    events=[]
    for start,end in intervals:
        if end <= start:
            continue
        events.append((start,1))
        events.append((end,-1))
    # half-open intervals [start,end): completion before arrival at same timestamp
    events.sort(key=lambda x:(x[0],x[1]))
    cur=0
    best=0
    for _,delta in events:
        cur += delta
        best=max(best,cur)
    return best

def main():
    p=argparse.ArgumentParser()
    p.add_argument("trace",type=Path)
    p.add_argument("--kv-gib-per-active",type=float,default=1.5)
    a=p.parse_args()

    rows=list(csv.DictReader(a.trace.open(encoding="utf-8")))
    if not rows:
        raise SystemExit("empty trace")

    sys_intervals=[]
    active_intervals=[]
    queue_intervals=[]
    wsys=[]
    wactive=[]
    wqueue=[]

    for r in rows:
        arrival=float(r["arrival_ms"])/1000
        service=float(r["service_start_ms"])/1000
        done=float(r["complete_ms"])/1000

        if not arrival <= service <= done:
            raise SystemExit(f"invalid timeline: {r['request_id']}")

        sys_intervals.append((arrival,done))
        active_intervals.append((service,done))
        queue_intervals.append((arrival,service))

        wsys.append(done-arrival)
        wactive.append(done-service)
        wqueue.append(service-arrival)

    start=min(x[0] for x in sys_intervals)
    end=max(x[1] for x in sys_intervals)
    horizon=end-start
    n=len(rows)
    lam=n/horizon

    mean_sys=statistics.mean(wsys)
    mean_active=statistics.mean(wactive)
    mean_queue=statistics.mean(wqueue)

    area_sys=sum(b-a for a,b in sys_intervals)
    area_active=sum(b-a for a,b in active_intervals)
    area_queue=sum(b-a for a,b in queue_intervals)

    lsys=area_sys/horizon
    lactive=area_active/horizon
    lqueue=area_queue/horizon

    print("LITTLE'S LAW TRACE")
    print(f"requests: {n}")
    print(f"horizon: {horizon:.3f} s")
    print(f"throughput lambda: {lam:.6f} req/s")
    print()
    print("SYSTEM")
    print(f"  mean W_system: {mean_sys:.6f} s")
    print(f"  lambda*W: {lam*mean_sys:.6f}")
    print(f"  trace-area L: {lsys:.6f}")
    print(f"  peak: {peak(sys_intervals)}")
    print("ACTIVE")
    print(f"  mean W_active: {mean_active:.6f} s")
    print(f"  lambda*W: {lam*mean_active:.6f}")
    print(f"  trace-area L: {lactive:.6f}")
    print(f"  peak: {peak(active_intervals)}")
    print("QUEUE")
    print(f"  mean W_queue: {mean_queue:.6f} s")
    print(f"  lambda*W: {lam*mean_queue:.6f}")
    print(f"  trace-area L: {lqueue:.6f}")
    print(f"  peak: {peak(queue_intervals)}")
    print()
    print(f"check L_system-(L_active+L_queue): {lsys-(lactive+lqueue):.12f}")
    print()
    print("CONSTANT-KV TEACHING PROXY")
    print(f"KV per active sequence: {a.kv_gib_per_active:.3f} GiB")
    print(f"average active KV proxy: {lactive*a.kv_gib_per_active:.3f} GiB")
    print(f"peak active KV proxy: {peak(active_intervals)*a.kv_gib_per_active:.3f} GiB")
    print("WARNING: real per-sequence KV is not constant.")

if __name__=="__main__":
    main()

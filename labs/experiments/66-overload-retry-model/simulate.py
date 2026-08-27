#!/usr/bin/env python3
import argparse
import heapq
import itertools
import math
import statistics

def percentile(values,p):
    if not values:
        return None
    vals=sorted(values)
    return vals[max(0,math.ceil(p*len(vals))-1)]

def simulate(queue_limit,retry_mode,max_retries,n,spacing,service_time):
    states={
        i:{
            "arrival":i*spacing,
            "accepted":False,
            "service_start":None,
            "complete":None,
            "attempts":0,
        }
        for i in range(n)
    }

    events=[]
    seq=itertools.count()

    def push(t,kind,rid,attempt):
        priority=0 if kind=="complete" else 1
        heapq.heappush(
            events,
            (t,priority,next(seq),kind,rid,attempt)
        )

    for rid in states:
        push(states[rid]["arrival"],"attempt",rid,0)

    active=None
    queue=[]
    rejects=0
    attempts=0
    max_queue=0

    def retry(t,rid,attempt):
        if attempt >= max_retries:
            return
        nxt=attempt+1
        if retry_mode=="immediate":
            delay=0.1
        elif retry_mode=="backoff":
            delay=0.5*(2**attempt)
        else:
            return
        push(t+delay,"attempt",rid,nxt)

    while events:
        t,_,__,kind,rid,attempt=heapq.heappop(events)
        st=states[rid]

        if kind=="complete":
            if active != rid:
                raise RuntimeError("active/completion mismatch")
            st["complete"]=t
            active=None

            if queue:
                nrid,nattempt=queue.pop(0)
                nst=states[nrid]
                active=nrid
                nst["service_start"]=t
                push(t+service_time,"complete",nrid,nattempt)
            continue

        if st["accepted"] or st["complete"] is not None:
            continue

        attempts += 1
        st["attempts"] += 1

        can_accept=(
            active is None
            or queue_limit is None
            or len(queue) < queue_limit
        )

        if can_accept:
            st["accepted"]=True
            if active is None:
                active=rid
                st["service_start"]=t
                push(t+service_time,"complete",rid,attempt)
            else:
                queue.append((rid,attempt))
                max_queue=max(max_queue,len(queue))
        else:
            rejects += 1
            retry(t,rid,attempt)

    completed=[
        st for st in states.values()
        if st["complete"] is not None
    ]
    waits=[
        st["service_start"]-st["arrival"]
        for st in completed
    ]

    return {
        "attempts":attempts,
        "reject_attempts":rejects,
        "completed":len(completed),
        "dropped":n-len(completed),
        "max_queue":max_queue,
        "mean_wait":statistics.mean(waits) if waits else None,
        "p95_wait":percentile(waits,0.95),
        "makespan":max(st["complete"] for st in completed) if completed else 0,
    }

def show(name,r):
    print(name)
    for k in [
        "attempts","reject_attempts","completed","dropped",
        "max_queue"
    ]:
        print(f"  {k}: {r[k]}")
    print(f"  mean_wait_s: {r['mean_wait']:.6f}")
    print(f"  p95_wait_s: {r['p95_wait']:.6f}")
    print(f"  makespan_s: {r['makespan']:.6f}")
    print(f"  attempt_amplification: {r['attempts']/10:.3f}x")
    print()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--requests",type=int,default=10)
    p.add_argument("--spacing",type=float,default=0.5)
    p.add_argument("--service-time",type=float,default=1.0)
    a=p.parse_args()

    if a.requests != 10:
        raise SystemExit(
            "default report formatting assumes --requests 10; "
            "edit the script for generalized amplification denominator"
        )

    scenarios=[
        (
            "unbounded",
            simulate(None,"none",0,a.requests,a.spacing,a.service_time)
        ),
        (
            "bounded-no-retry",
            simulate(2,"none",0,a.requests,a.spacing,a.service_time)
        ),
        (
            "bounded-immediate-retry",
            simulate(2,"immediate",3,a.requests,a.spacing,a.service_time)
        ),
        (
            "bounded-backoff",
            simulate(2,"backoff",3,a.requests,a.spacing,a.service_time)
        ),
    ]

    for name,r in scenarios:
        show(name,r)

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import heapq
import itertools
import math
import statistics
from collections import defaultdict

JOBS = [
    {"id":"A1","tenant":"A","tokens":100,"arrival":0.0},
    {"id":"A2","tenant":"A","tokens":100,"arrival":0.0},
    {"id":"B1","tenant":"B","tokens":10,"arrival":0.0},
    {"id":"B2","tenant":"B","tokens":10,"arrival":0.0},
    {"id":"B3","tenant":"B","tokens":10,"arrival":0.0},
    {"id":"B4","tenant":"B","tokens":10,"arrival":0.0},
]

def percentile(vals,p):
    vals=sorted(vals)
    return vals[max(0,math.ceil(p*len(vals))-1)]

def simulate(policy, slots=2, token_rate=10.0):
    pending=[dict(j) for j in JOBS]
    active=[]
    complete=[]
    counts=defaultdict(int)
    seq=itertools.count()
    t=0.0
    busy_slot_seconds=0.0

    def choose():
        if not pending:
            return None

        if policy=="fifo":
            return 0

        for i,j in enumerate(pending):
            if counts[j["tenant"]] < 1:
                return i

        if policy=="fair-borrow":
            return 0

        return None

    while pending or active:
        while len(active) < slots:
            idx=choose()
            if idx is None:
                break

            j=pending.pop(idx)
            j["start"]=t
            duration=j["tokens"]/token_rate
            j["done"]=t+duration
            busy_slot_seconds += duration
            counts[j["tenant"]] += 1
            heapq.heappush(active,(j["done"],next(seq),j))

        if not active:
            raise RuntimeError("scheduler deadlock")

        t=active[0][0]

        while active and abs(active[0][0]-t) < 1e-12:
            _,_,j=heapq.heappop(active)
            counts[j["tenant"]] -= 1
            complete.append(j)

    makespan=max(j["done"] for j in complete)
    util=busy_slot_seconds/(slots*makespan)

    per=defaultdict(list)
    for j in complete:
        per[j["tenant"]].append(j)

    out={}
    for tenant,items in per.items():
        waits=[j["start"]-j["arrival"] for j in items]
        out[tenant]={
            "requests":len(items),
            "tokens":sum(j["tokens"] for j in items),
            "mean_wait":statistics.mean(waits),
            "p95_wait":percentile(waits,0.95),
            "last_done":max(j["done"] for j in items),
        }

    return makespan,util,out,complete

def main():
    total_tokens=sum(j["tokens"] for j in JOBS)
    print("SYNTHETIC MULTI-TENANT SCHEDULER")
    print(f"requests={len(JOBS)} total_output_tokens={total_tokens}")
    print("A: 2 requests / 200 tokens")
    print("B: 4 requests / 40 tokens")
    print()

    for policy in ["fifo","strict-cap","fair-borrow"]:
        makespan,util,per,complete=simulate(policy)
        print(policy)
        print(f"  makespan: {makespan:.3f} s")
        print(f"  slot utilization: {util*100:.3f}%")
        for tenant in ["A","B"]:
            m=per[tenant]
            print(
                f"  tenant {tenant}: requests={m['requests']} "
                f"tokens={m['tokens']} "
                f"mean_wait={m['mean_wait']:.3f}s "
                f"p95_wait={m['p95_wait']:.3f}s "
                f"last_done={m['last_done']:.3f}s"
            )
        print("  starts:",", ".join(
            f"{j['id']}@{j['start']:.1f}"
            for j in sorted(complete,key=lambda x:(x["start"],x["id"]))
        ))
        print()

if __name__=="__main__":
    main()

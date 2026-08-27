#!/usr/bin/env python3
import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

def pct(vals,p):
    if not vals:
        return None
    vals=sorted(vals)
    return vals[max(0,math.ceil(p*len(vals))-1)]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("workload_jsonl",type=Path)
    p.add_argument("requests_csv",type=Path)
    a=p.parse_args()

    meta={}
    for line in a.workload_jsonl.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj=json.loads(line)
        rid=str(obj["id"])
        meta[rid]=obj

    rows=list(csv.DictReader(a.requests_csv.open(encoding="utf-8")))
    groups=defaultdict(list)

    for r in rows:
        rid=str(r["request_id"])
        if rid not in meta:
            raise SystemExit(f"request {rid} missing from workload metadata")
        tenant=str(meta[rid].get("tenant","UNSPECIFIED"))
        r["_meta"]=meta[rid]
        groups[tenant].append(r)

    print("PER-TENANT SERVING REPORT")
    print("| tenant | requests | success | prompt tokens* | requested output | observed output ids | TTFT p50 ms | TTFT p95 ms | E2E p95 ms |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    for tenant in sorted(groups):
        items=groups[tenant]
        success=[r for r in items if r.get("status","ok")=="ok"]
        ttft=[
            float(r["client_ttft_ms"])
            for r in success
            if r.get("client_ttft_ms","").strip()
        ]
        e2e=[
            float(r["client_e2e_ms"])
            for r in success
            if r.get("client_e2e_ms","").strip()
        ]
        prompt=sum(
            int(r["_meta"].get("prompt_tokens",0) or 0)
            for r in items
        )
        requested=sum(
            int(r["_meta"].get("n_predict",0) or 0)
            for r in items
        )
        observed=sum(
            int(float(r.get("token_ids_seen",0) or 0))
            for r in success
        )
        fmt=lambda x:"n/a" if x is None else f"{x:.3f}"
        print(
            f"| {tenant} | {len(items)} | {len(success)} | {prompt} | "
            f"{requested} | {observed} | {fmt(pct(ttft,.50))} | "
            f"{fmt(pct(ttft,.95))} | {fmt(pct(e2e,.95))} |"
        )

    print()
    print("* prompt_tokens comes from workload metadata and must be produced by the exact tokenizer.")
    print("observed output ids comes from client stream token arrays; inspect raw SSE for anomalies.")

if __name__=="__main__":
    main()

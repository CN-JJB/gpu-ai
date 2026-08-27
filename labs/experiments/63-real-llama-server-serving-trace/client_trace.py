#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def fetch_text(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"# fetch failed: {type(e).__name__}: {e}\n"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("workload",type=Path)
    p.add_argument("--server",default="http://127.0.0.1:8080")
    p.add_argument("--out-dir",type=Path,default=Path("evidence"))
    p.add_argument("--timeout",type=float,default=3600)
    a=p.parse_args()

    items=[
        json.loads(line)
        for line in a.workload.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not items:
        raise SystemExit("empty workload")

    a.out_dir.mkdir(parents=True,exist_ok=True)
    raw_dir=a.out_dir/"raw-sse"
    raw_dir.mkdir(exist_ok=True)

    metrics_url=a.server.rstrip("/")+"/metrics"
    (a.out_dir/"metrics-before.txt").write_text(
        fetch_text(metrics_url),encoding="utf-8"
    )

    t0=time.perf_counter()
    results=[]
    lock=threading.Lock()

    def worker(item):
        delay=float(item.get("delay_ms",0))/1000.0
        target=t0+delay
        now=time.perf_counter()
        if target>now:
            time.sleep(target-now)

        prompt_path=Path(item["prompt_file"])
        prompt_bytes=prompt_path.read_bytes()
        prompt=prompt_bytes.decode("utf-8")
        rid=str(item["id"])
        n_predict=int(item["n_predict"])

        body=json.dumps({
            "prompt":prompt,
            "n_predict":n_predict,
            "stream":True,
            "return_tokens":True,
            "timings_per_token":True
        }).encode("utf-8")

        req=urllib.request.Request(
            a.server.rstrip("/")+"/completion",
            data=body,
            headers={"Content-Type":"application/json"},
            method="POST",
        )

        sent=time.perf_counter()
        first_token_chunk=None
        done=None
        token_ids=0
        token_chunks=0
        token_chunk_times=[]
        raw=[]

        status="ok"
        error=""

        try:
            with urllib.request.urlopen(req,timeout=a.timeout) as resp:
                for raw_line in resp:
                    line=raw_line.decode("utf-8",errors="replace").rstrip("\r\n")
                    stamp=time.perf_counter()
                    raw.append(f"{(stamp-t0)*1000:.3f}\t{line}")
                    if not line.startswith("data: "):
                        continue
                    payload=line[6:]
                    if payload=="[DONE]":
                        continue
                    try:
                        obj=json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    toks=obj.get("tokens") or []
                    if toks:
                        token_ids += len(toks)
                        token_chunks += 1
                        token_chunk_times.append(stamp)
                        if first_token_chunk is None:
                            first_token_chunk=stamp
                    if obj.get("stop") is True:
                        done=stamp
                if done is None:
                    done=time.perf_counter()
        except Exception as e:
            status="error"
            error=f"{type(e).__name__}: {e}"
            done=time.perf_counter()

        gaps=[
            (b-c)*1000
            for c,b in zip(token_chunk_times,token_chunk_times[1:])
        ]

        rec={
            "request_id":rid,
            "scheduled_ms":delay*1000,
            "client_send_ms":(sent-t0)*1000,
            "first_token_chunk_ms":(
                "" if first_token_chunk is None
                else (first_token_chunk-t0)*1000
            ),
            "complete_ms":(done-t0)*1000,
            "client_ttft_ms":(
                "" if first_token_chunk is None
                else (first_token_chunk-sent)*1000
            ),
            "client_e2e_ms":(done-sent)*1000,
            "token_ids_seen":token_ids,
            "token_chunks":token_chunks,
            "mean_token_chunk_gap_ms":(
                "" if not gaps else sum(gaps)/len(gaps)
            ),
            "prompt_bytes":len(prompt_bytes),
            "prompt_sha256":sha256_bytes(prompt_bytes),
            "requested_n_predict":n_predict,
            "status":status,
            "error":error,
        }

        (raw_dir/f"{rid}.log").write_text(
            "\n".join(raw)+"\n",encoding="utf-8"
        )
        with lock:
            results.append(rec)

    threads=[threading.Thread(target=worker,args=(x,)) for x in items]
    for t in threads: t.start()
    for t in threads: t.join()

    (a.out_dir/"metrics-after.txt").write_text(
        fetch_text(metrics_url),encoding="utf-8"
    )

    results.sort(key=lambda r:r["scheduled_ms"])
    fields=list(results[0].keys())
    with (a.out_dir/"requests.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    identity={
        "workload_path":str(a.workload),
        "workload_sha256":sha256_bytes(a.workload.read_bytes()),
        "server":a.server,
        "request_count":len(items),
        "timing_boundary":"client perf_counter around HTTP/SSE",
        "chunk_gap_warning":"SSE token-bearing chunk gap is not guaranteed true token ITL",
    }
    (a.out_dir/"workload-manifest.json").write_text(
        json.dumps(identity,indent=2,sort_keys=True)+"\n",
        encoding="utf-8"
    )

    print(json.dumps(identity,indent=2,sort_keys=True))
    print(f"wrote {a.out_dir/'requests.csv'}")

if __name__=="__main__":
    main()

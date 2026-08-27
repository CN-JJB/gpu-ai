#!/usr/bin/env python3
import argparse,csv,json,os,shutil,subprocess,time
import urllib.error,urllib.parse,urllib.request
from pathlib import Path

ALLOWED_HOSTS={"127.0.0.1","localhost","::1"}

METRICS=[
    "llamacpp:prompt_tokens_seconds",
    "llamacpp:predicted_tokens_seconds",
    "llamacpp:requests_processing",
    "llamacpp:requests_deferred",
    "llamacpp:n_busy_slots_per_decode",
    "llamacpp:n_tokens_max",
]

def fetch_metrics(base):
    try:
        with urllib.request.urlopen(base.rstrip("/")+"/metrics",timeout=3) as r:
            return r.read().decode("utf-8",errors="replace"),r.status
    except urllib.error.HTTPError as e:
        return e.read().decode("utf-8",errors="replace"),e.code
    except Exception as e:
        return f"# fetch failed: {type(e).__name__}: {e}\n",None

def parse_metrics(text):
    out={}
    for line in text.splitlines():
        if not line or line.startswith("#") or "{" in line:
            continue
        parts=line.split()
        if len(parts)!=2:
            continue
        name,value=parts
        if name in METRICS:
            try: out[name]=float(value)
            except ValueError: pass
    return out

def run_raw(cmd,timeout=5):
    try:
        p=subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            text=True,
            check=False
        )
        return p.returncode,p.stdout
    except Exception as e:
        return -1,f"{type(e).__name__}: {e}\n"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base",default="http://127.0.0.1:8080")
    p.add_argument("--duration",type=float,default=30)
    p.add_argument("--interval",type=float,default=1.0)
    p.add_argument("--out-dir",type=Path,default=Path("incident-evidence"))
    a=p.parse_args()

    u=urllib.parse.urlparse(a.base)
    if u.hostname not in ALLOWED_HOSTS:
        raise SystemExit("collector is intentionally limited to localhost/loopback")
    if not 1 <= a.duration <= 300:
        raise SystemExit("duration must be 1..300 seconds")
    if a.interval < 0.5:
        raise SystemExit("interval must be >= 0.5 seconds")

    a.out_dir.mkdir(parents=True,exist_ok=True)
    metrics_dir=a.out_dir/"metrics-raw"
    vendor_dir=a.out_dir/"vendor-raw"
    metrics_dir.mkdir(exist_ok=True)
    vendor_dir.mkdir(exist_ok=True)

    vendor="none"
    if shutil.which("nvidia-smi"):
        vendor="nvidia"
    elif shutil.which("amd-smi"):
        vendor="amd-smi"
    elif shutil.which("rocm-smi"):
        vendor="rocm-smi"

    rows=[]
    start=time.monotonic()
    i=0
    while True:
        elapsed=time.monotonic()-start
        if elapsed > a.duration and i>0:
            break

        wall=time.strftime("%Y-%m-%dT%H:%M:%S%z")
        text,status=fetch_metrics(a.base)
        (metrics_dir/f"{i:04d}.txt").write_text(text,encoding="utf-8")
        parsed=parse_metrics(text)

        vendor_rc=None
        if vendor=="nvidia":
            cmd=[
                "nvidia-smi",
                "--query-gpu=timestamp,index,name,temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw,clocks.sm,clocks.mem",
                "--format=csv,noheader,nounits"
            ]
            vendor_rc,vout=run_raw(cmd)
            (vendor_dir/f"{i:04d}-nvidia.csv").write_text(vout,encoding="utf-8")
        elif vendor=="amd-smi":
            vendor_rc,vout=run_raw(["amd-smi","metric"])
            (vendor_dir/f"{i:04d}-amd-smi.txt").write_text(vout,encoding="utf-8")
        elif vendor=="rocm-smi":
            vendor_rc,vout=run_raw([
                "rocm-smi","--showtemp","--showuse","--showmemuse",
                "--showclocks","--showpower"
            ])
            (vendor_dir/f"{i:04d}-rocm-smi.txt").write_text(vout,encoding="utf-8")

        row={
            "sample":i,
            "wall_time":wall,
            "elapsed_s":elapsed,
            "metrics_http_status":status,
            "vendor_tool":vendor,
            "vendor_returncode":vendor_rc,
        }
        for name in METRICS:
            row[name]=parsed.get(name,"")
        try:
            loads=os.getloadavg()
            row["host_load1"]=loads[0]
        except (AttributeError,OSError):
            row["host_load1"]=""

        rows.append(row)
        i+=1

        sleep_until=start+i*a.interval
        delay=sleep_until-time.monotonic()
        if delay>0:
            time.sleep(delay)

    fields=list(rows[0].keys())
    with (a.out_dir/"timeline.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(rows)

    manifest={
        "schema_version":1,
        "base":a.base,
        "duration_s":a.duration,
        "interval_s":a.interval,
        "samples":len(rows),
        "vendor_tool":vendor,
        "network_scope":"loopback-only",
        "changes_made":[
            "none to clocks/power/driver/firewall",
            "collector only reads localhost metrics and installed telemetry CLI"
        ]
    }
    (a.out_dir/"collector-manifest.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

MEM_FIELDS=[
    "MemTotal","MemFree","MemAvailable","Buffers","Cached",
    "SReclaimable","Shmem","SwapTotal","SwapFree","SwapCached"
]
VM_FIELDS=[
    "pswpin","pswpout","pgmajfault","pgfault","oom_kill",
    "workingset_refault_file","workingset_refault_anon"
]
PROC_FIELDS=[
    "VmSize","VmRSS","RssAnon","RssFile","RssShmem","VmSwap"
]

def parse_kv_file(path,wanted):
    out={}
    try:
        lines=Path(path).read_text(encoding="utf-8",errors="replace").splitlines()
    except Exception:
        return out
    for line in lines:
        if ":" in line:
            key,val=line.split(":",1)
            if key not in wanted:
                continue
            parts=val.strip().split()
            try:
                n=float(parts[0])
            except Exception:
                continue
            unit=parts[1] if len(parts)>1 else ""
            out[key]=(n,unit)
        else:
            parts=line.split()
            if len(parts)==2 and parts[0] in wanted:
                try: out[parts[0]]=(float(parts[1]),"counter")
                except ValueError: pass
    return out

def kb_value(d,key):
    v=d.get(key)
    return "" if v is None else v[0]

def counter_value(d,key):
    v=d.get(key)
    return "" if v is None else v[0]

def run_raw(cmd,timeout=5):
    try:
        p=subprocess.run(
            cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
            text=True,timeout=timeout,check=False
        )
        return p.returncode,p.stdout
    except Exception as e:
        return -1,f"{type(e).__name__}: {e}\n"

def nvidia_snapshot():
    if not shutil.which("nvidia-smi"):
        return None
    cmd=[
        "nvidia-smi",
        "--query-gpu=index,name,memory.used,memory.total,utilization.gpu",
        "--format=csv,noheader,nounits"
    ]
    rc,out=run_raw(cmd)
    return {"returncode":rc,"output":out}

def linux_process(pid):
    if pid is None:
        return {},{}
    base=Path("/proc")/str(pid)
    status=parse_kv_file(base/"status",set(PROC_FIELDS))
    smaps={}
    p=base/"smaps_rollup"
    if p.is_file():
        smaps=parse_kv_file(p,{
            "Rss","Pss","Pss_Anon","Pss_File","Pss_Shmem",
            "Private_Clean","Private_Dirty","Swap"
        })
    return status,smaps

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pid",type=int)
    p.add_argument("--duration",type=float,default=30)
    p.add_argument("--interval",type=float,default=1.0)
    p.add_argument("--out-dir",type=Path,default=Path("memory-evidence"))
    a=p.parse_args()

    if not 1<=a.duration<=300:
        raise SystemExit("duration must be 1..300 seconds")
    if a.interval<0.5:
        raise SystemExit("interval must be >=0.5 seconds")
    if a.pid is not None and a.pid<=0:
        raise SystemExit("pid must be positive")

    system=platform.system()
    if system!="Linux":
        raise SystemExit(
            "collect_memory.py currently provides structured sampling on Linux; "
            "use the bundled platform notes/scripts for other OSes"
        )

    a.out_dir.mkdir(parents=True,exist_ok=True)
    raw=a.out_dir/"raw"
    raw.mkdir(exist_ok=True)

    rows=[]
    start=time.monotonic()
    i=0
    while True:
        elapsed=time.monotonic()-start
        if elapsed>a.duration and i>0:
            break

        mem=parse_kv_file("/proc/meminfo",set(MEM_FIELDS))
        vm=parse_kv_file("/proc/vmstat",set(VM_FIELDS))
        proc,smaps=linux_process(a.pid)

        gpu=nvidia_snapshot()
        if gpu is not None:
            (raw/f"{i:04d}-nvidia.csv").write_text(
                gpu["output"],encoding="utf-8"
            )

        snapshot={
            "meminfo":{k:mem[k] for k in mem},
            "vmstat":{k:vm[k] for k in vm},
            "process_status":{k:proc[k] for k in proc},
            "smaps_rollup":{k:smaps[k] for k in smaps},
            "nvidia":gpu
        }
        (raw/f"{i:04d}.json").write_text(
            json.dumps(snapshot,indent=2,sort_keys=True)+"\n",
            encoding="utf-8"
        )

        row={
            "sample":i,
            "wall_time":time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "elapsed_s":elapsed,
        }
        for k in MEM_FIELDS:
            row[k+"_kB"]=kb_value(mem,k)
        for k in VM_FIELDS:
            row[k]=counter_value(vm,k)
        for k in PROC_FIELDS:
            row["proc_"+k+"_kB"]=kb_value(proc,k)

        pss=smaps.get("Pss")
        row["proc_Pss_kB"]="" if pss is None else pss[0]

        rows.append(row)
        i+=1
        target=start+i*a.interval
        delay=target-time.monotonic()
        if delay>0:
            time.sleep(delay)

    fields=list(rows[0].keys())
    with (a.out_dir/"timeline.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader();w.writerows(rows)

    manifest={
        "schema_version":1,
        "platform":system,
        "pid":a.pid,
        "duration_s":a.duration,
        "interval_s":a.interval,
        "samples":len(rows),
        "stress_allocation_performed":False,
        "system_settings_changed":False,
        "notes":[
            "/proc/vmstat counters are cumulative; analyze deltas",
            "low MemFree alone is not a pressure diagnosis",
            "NVIDIA VRAM is a separate discrete-GPU memory domain"
        ]
    }
    (a.out_dir/"manifest.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse
import json
import os
import platform
import shutil
import stat
import subprocess
import time
from pathlib import Path

MIB=1024*1024

def run_capture(cmd,timeout=15):
    try:
        p=subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False
        )
        return {"command":cmd,"returncode":p.returncode,"output":p.stdout}
    except Exception as e:
        return {"command":cmd,"returncode":-1,"output":f"{type(e).__name__}: {e}\n"}

def fincore(path):
    if platform.system()!="Linux" or not shutil.which("fincore"):
        return {
            "available":False,
            "note":"fincore unavailable or non-Linux"
        }
    r=run_capture(["fincore","--json","--output-all",str(path)])
    return {
        "available":True,
        "returncode":r["returncode"],
        "output":r["output"]
    }

def meminfo():
    p=Path("/proc/meminfo")
    if platform.system()=="Linux" and p.is_file():
        wanted={"MemTotal","MemAvailable","Cached","Buffers","SwapCached"}
        out={}
        for line in p.read_text(encoding="utf-8",errors="replace").splitlines():
            key=line.split(":",1)[0]
            if key in wanted:
                out[key]=line.split(":",1)[1].strip()
        return out
    return {}

def read_pass(path,nbytes,block_bytes):
    done=0
    t0=time.perf_counter()
    with path.open("rb",buffering=0) as f:
        while done<nbytes:
            chunk=f.read(min(block_bytes,nbytes-done))
            if not chunk:
                break
            done += len(chunk)
    dt=time.perf_counter()-t0
    mib_s=(done/MIB)/dt if dt>0 else None
    return {
        "bytes_read":done,
        "duration_s":dt,
        "MiB_per_s":mib_s
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("model",type=Path)
    g=p.add_mutually_exclusive_group()
    g.add_argument("--bytes",type=int,default=512*MIB)
    g.add_argument("--full",action="store_true")
    p.add_argument("--passes",type=int,default=2)
    p.add_argument("--block-mib",type=int,default=8)
    p.add_argument("--out",type=Path,default=Path("file-read-probe.json"))
    a=p.parse_args()

    st=a.model.stat()
    if not stat.S_ISREG(st.st_mode):
        raise SystemExit("model must be a regular file")
    if not 1 <= a.passes <= 3:
        raise SystemExit("passes must be 1..3")
    if a.block_mib < 1 or a.block_mib > 64:
        raise SystemExit("block-mib must be 1..64")

    nbytes=st.st_size if a.full else min(a.bytes,st.st_size)
    if nbytes<=0:
        raise SystemExit("read size must be >0")

    result={
        "schema_version":1,
        "model_path":str(a.model.resolve()),
        "file_bytes":st.st_size,
        "bytes_per_pass":nbytes,
        "full_file":bool(a.full),
        "passes":a.passes,
        "block_bytes":a.block_mib*MIB,
        "platform":platform.platform(),
        "cache_drop_performed":False,
        "labels":[
            "pass1 initial cache state UNKNOWN unless independent residency evidence says otherwise",
            "later passes occur after same-file buffered read"
        ],
        "before":{
            "fincore":fincore(a.model),
            "meminfo":meminfo()
        },
        "read_results":[]
    }

    for i in range(a.passes):
        rec=read_pass(a.model,nbytes,a.block_mib*MIB)
        rec["pass"]=i+1
        rec["label"]="initial-state-unknown" if i==0 else "after-same-file-read"
        result["read_results"].append(rec)

    result["after"]={
        "fincore":fincore(a.model),
        "meminfo":meminfo()
    }

    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    print(f"wrote {a.out}")
    print("WARNING: the read probe itself changes page-cache state.")
    print("WARNING: MiB/s from later passes is not automatically storage bandwidth.")

if __name__=="__main__":
    main()

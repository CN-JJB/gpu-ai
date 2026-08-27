#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import subprocess
import time
from datetime import datetime,timezone
from pathlib import Path

FORBIDDEN={
    "-m","--model","-hf","-hfr","--hf-repo","-hff","--hf-file","-hft","--hf-token",
    "-p","--n-prompt","-n","--n-gen","-r","--repetitions",
    "-o","--output","-oe","--output-err"
}

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def validate_extra(args):
    for x in args:
        key=x.split("=",1)[0]
        if key in FORBIDDEN:
            raise SystemExit(f"forbidden controlled field in --extra-arg: {x}")

def clean_env():
    env=os.environ.copy()
    for k in list(env):
        if k.startswith("LLAMA_ARG_") or k=="HF_TOKEN":
            del env[k]
    return env

def parse_jsonl(text):
    rows=[]
    for line in text.splitlines():
        line=line.strip()
        if not line.startswith("{"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--bench-bin",type=Path,required=True)
    p.add_argument("--model",type=Path,required=True)
    p.add_argument("--n-gen",type=int,default=512)
    p.add_argument("--repetitions",type=int,default=20)
    p.add_argument("--no-warmup",action="store_true")
    p.add_argument("--extra-arg",action="append",default=[])
    p.add_argument("--out-dir",type=Path,default=Path("sustained-tg"))
    a=p.parse_args()

    if not a.bench_bin.is_file():
        raise SystemExit("llama-bench binary not found")
    if not a.model.is_file():
        raise SystemExit("model not found")
    if not 16<=a.n_gen<=8192:
        raise SystemExit("n-gen must be 16..8192")
    if not 4<=a.repetitions<=60:
        raise SystemExit("repetitions must be 4..60")
    validate_extra(a.extra_arg)

    a.out_dir.mkdir(parents=True,exist_ok=True)

    cmd=[
        str(a.bench_bin),
        "-m",str(a.model),
        "-p","0",
        "-n",str(a.n_gen),
        "-r",str(a.repetitions),
        "-o","jsonl",
    ]
    if a.no_warmup:
        cmd.append("--no-warmup")
    cmd.extend(a.extra_arg)

    start_epoch=time.time()
    start_iso=datetime.now(timezone.utc).isoformat()
    t0=time.perf_counter()
    proc=subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=clean_env(),
        check=False
    )
    elapsed=time.perf_counter()-t0
    end_epoch=time.time()
    end_iso=datetime.now(timezone.utc).isoformat()

    (a.out_dir/"llama-bench.jsonl").write_text(proc.stdout,encoding="utf-8")
    (a.out_dir/"llama-bench.stderr.txt").write_text(proc.stderr,encoding="utf-8")

    rows=parse_jsonl(proc.stdout)
    tg=[
        r for r in rows
        if int(r.get("n_prompt",-1))==0 and int(r.get("n_gen",0))==a.n_gen
    ]
    if proc.returncode!=0:
        raise SystemExit(f"llama-bench failed with code {proc.returncode}")
    if len(tg)!=1:
        raise SystemExit(f"expected exactly one TG JSON row, got {len(tg)}")

    row=tg[0]
    samples=row.get("samples_ts")
    samples_ns=row.get("samples_ns")
    if not isinstance(samples,list) or len(samples)!=a.repetitions:
        raise SystemExit("samples_ts missing or repetition count mismatch")
    if not isinstance(samples_ns,list) or len(samples_ns)!=a.repetitions:
        raise SystemExit("samples_ns missing or repetition count mismatch")

    manifest={
        "schema_version":1,
        "bench_bin":str(a.bench_bin.resolve()),
        "bench_sha256":sha256(a.bench_bin),
        "model":str(a.model.resolve()),
        "model_sha256":sha256(a.model),
        "n_gen":a.n_gen,
        "repetitions":a.repetitions,
        "warmup":"disabled" if a.no_warmup else "llama-bench default",
        "extra_args":a.extra_arg,
        "command":cmd,
        "start_epoch_s":start_epoch,
        "end_epoch_s":end_epoch,
        "start_utc":start_iso,
        "end_utc":end_iso,
        "wall_elapsed_s":elapsed,
        "avg_ts":row.get("avg_ts"),
        "samples_ts":samples,
        "samples_ns":samples_ns,
        "environment_policy":"LLAMA_ARG_* and HF_TOKEN removed"
    }
    (a.out_dir/"manifest.json").write_text(
        json.dumps(manifest,indent=2,sort_keys=True)+"\n",
        encoding="utf-8"
    )
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

FORBIDDEN_PREFIXES=(
    "-m","--model","--model-url","--hf-repo","--hf-file",
    "--host","--port","--api-key","--api-key-file",
    "--ssl-key-file","--ssl-cert-file",
    "--tools","--agent","-ag","--mcp-","--ui-mcp-proxy"
)

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def validate_extra(args):
    for x in args:
        blocked=False
        for p in FORBIDDEN_PREFIXES:
            if x==p or x.startswith(p+"="):
                blocked=True
            if p in ("--tools","--mcp-") and x.startswith(p):
                blocked=True
        if blocked:
            raise SystemExit(
                f"forbidden extra arg in loopback-only reliability lab: {x}"
            )

def sanitized_child_env():
    env=os.environ.copy()
    for key in list(env):
        if key.startswith("LLAMA_ARG_") or key=="LLAMA_API_KEY":
            del env[key]
    return env

def poll_health(proc,base,deadline,poll_s):
    t0=time.perf_counter()
    first_http=None
    transitions=[]
    while True:
        if proc.poll() is not None:
            raise RuntimeError(f"server exited before ready, code={proc.returncode}")

        now=time.perf_counter()
        if now-t0 > deadline:
            raise TimeoutError("readiness deadline exceeded")

        status=None
        try:
            with urllib.request.urlopen(base+"/health",timeout=2) as r:
                status=r.status
                r.read(1024)
        except urllib.error.HTTPError as e:
            status=e.code
        except Exception:
            status=None

        rel=(time.perf_counter()-t0)*1000
        if status is not None and first_http is None:
            first_http=rel
        if not transitions or transitions[-1]["status"]!=status:
            transitions.append({"ms":rel,"status":status})

        if status==200:
            return {
                "first_http_ms":first_http,
                "ready_ms":rel,
                "health_transitions":transitions
            }

        time.sleep(poll_s)

def smoke(base,prompt):
    body=json.dumps({
        "prompt":prompt,
        "n_predict":1,
        "temperature":0.0,
        "cache_prompt":False
    }).encode("utf-8")
    req=urllib.request.Request(
        base+"/completion",
        data=body,
        headers={"Content-Type":"application/json"},
        method="POST"
    )
    t0=time.perf_counter()
    with urllib.request.urlopen(req,timeout=120) as r:
        status=r.status
        data=r.read(1024*1024)
    return {
        "http_status":status,
        "duration_ms":(time.perf_counter()-t0)*1000,
        "response_bytes":len(data)
    }

def stop_child(proc,timeout_s=10):
    t0=time.perf_counter()
    proc.terminate()
    forced=False
    try:
        code=proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        forced=True
        proc.kill()
        code=proc.wait(timeout=5)
    return {
        "exit_code":code,
        "stop_ms":(time.perf_counter()-t0)*1000,
        "forced_kill":forced
    }

def one_run(name,cmd,base,log_path,deadline,poll_s,prompt):
    with log_path.open("wb") as log:
        spawn=time.perf_counter()
        proc=subprocess.Popen(
            cmd,
            stdout=log,
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            env=sanitized_child_env()
        )
        try:
            health=poll_health(proc,base,deadline,poll_s)
            smoke_result=smoke(base,prompt)
            usable_ms=(time.perf_counter()-spawn)*1000
            stop=stop_child(proc)
            return {
                "name":name,
                **health,
                "smoke":smoke_result,
                "first_inference_complete_ms":usable_ms,
                "stop":stop,
                "server_log":str(log_path)
            }
        except Exception:
            if proc.poll() is None:
                stop_child(proc)
            raise

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--server-bin",type=Path,required=True)
    p.add_argument("--model",type=Path,required=True)
    p.add_argument("--port",type=int,default=18080)
    p.add_argument("--deadline",type=float,default=180)
    p.add_argument("--poll",type=float,default=0.1)
    p.add_argument("--prompt",default="Reply with OK.")
    p.add_argument("--extra-arg",action="append",default=[])
    p.add_argument("--out-dir",type=Path,default=Path("restart-evidence"))
    a=p.parse_args()

    if not a.server_bin.is_file():
        raise SystemExit("server binary not found")
    if not a.model.is_file():
        raise SystemExit("model file not found")
    if not 1024 <= a.port <= 65535:
        raise SystemExit("port must be 1024..65535")

    validate_extra(a.extra_arg)
    a.out_dir.mkdir(parents=True,exist_ok=True)

    server_sha=sha256(a.server_bin)
    model_sha_before=sha256(a.model)

    cmd=[
        str(a.server_bin),
        "-m",str(a.model),
        "--host","127.0.0.1",
        "--port",str(a.port),
        *a.extra_arg
    ]
    base=f"http://127.0.0.1:{a.port}"

    runs=[]
    for idx,name in enumerate(["cold-start","restart"],start=1):
        runs.append(one_run(
            name,cmd,base,
            a.out_dir/f"server-{idx}.log",
            a.deadline,a.poll,a.prompt
        ))
        if name=="cold-start":
            time.sleep(0.5)

    model_sha_after=sha256(a.model)
    result={
        "schema_version":1,
        "network_scope":"forced-loopback-127.0.0.1",
        "server_binary":str(a.server_bin),
        "server_sha256":server_sha,
        "model":str(a.model),
        "model_sha256_before":model_sha_before,
        "model_sha256_after":model_sha_after,
        "model_identity_unchanged":model_sha_before==model_sha_after,
        "command_without_secrets":cmd,
        "child_env_policy":"all LLAMA_ARG_* and LLAMA_API_KEY removed",
        "runs":runs,
        "notes":[
            "health 200 is readiness, not proof of steady-state SLO",
            "child is terminated only after smoke request finishes",
            "this lab does not test application-level in-flight draining"
        ]
    }
    out=a.out_dir/"restart-result.json"
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True))
    print(f"wrote {out}")

if __name__=="__main__":
    main()

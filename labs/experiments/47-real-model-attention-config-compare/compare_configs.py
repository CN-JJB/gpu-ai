#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def gib(n):
    return n/(1024**3)

def inspect(path, context, kv_bits, sequences):
    raw=json.loads(Path(path).read_text(encoding="utf-8"))
    c=raw.get("text_config",raw)

    layers=c.get("num_hidden_layers")
    hidden=c.get("hidden_size")
    hq=c.get("num_attention_heads")
    hkv=c.get("num_key_value_heads",hq)
    dh=c.get("head_dim")

    derived=False
    if dh is None and hidden is not None and hq:
        if hidden % hq == 0:
            dh=hidden//hq
            derived=True

    group=None
    if hq and hkv and hq % hkv == 0:
        group=hq//hkv

    kv=None
    if None not in (layers,hkv,dh):
        kv=2*layers*hkv*dh*(kv_bits/8)*context*sequences

    flags=[]
    for k in [
        "sliding_window","layer_types","rope_scaling",
        "num_local_experts","num_experts_per_tok","n_routed_experts",
        "attention_chunk_size"
    ]:
        v=c.get(k)
        if v not in (None,False,0,[],{}):
            flags.append(k)

    return {
        "file":str(path),
        "model_type":c.get("model_type","?"),
        "layers":layers,
        "hq":hq,
        "hkv":hkv,
        "dh":dh,
        "derived":derived,
        "group":group,
        "kv":kv,
        "flags":flags,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("configs",nargs="+")
    p.add_argument("--context",type=int,default=32768)
    p.add_argument("--kv-bits",type=int,default=16)
    p.add_argument("--sequences",type=int,default=1)
    a=p.parse_args()

    print(f"context={a.context} KV={a.kv_bits}b sequences={a.sequences}")
    print("| config | model_type | L | Hq | Hkv | group | Dh | KV GiB | caveats |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---|")

    for path in a.configs:
        r=inspect(path,a.context,a.kv_bits,a.sequences)
        group="n/a" if r["group"] is None else r["group"]
        dh="?" if r["dh"] is None else str(r["dh"]) + ("*" if r["derived"] else "")
        kv="n/a" if r["kv"] is None else f"{gib(r['kv']):.3f}"
        flags=",".join(r["flags"]) if r["flags"] else "-"
        print(
            f"| {r['file']} | {r['model_type']} | {r['layers']} | {r['hq']} | "
            f"{r['hkv']} | {group} | {dh} | {kv} | {flags} |"
        )

    print()
    print("* head_dim derived as hidden_size // query_heads")

if __name__=="__main__":
    main()

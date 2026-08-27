#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def inspect(path,bits):
    raw=json.loads(Path(path).read_text(encoding="utf-8"))
    c=raw.get("text_config",raw)
    d=c.get("hidden_size")
    f=c.get("intermediate_size")
    hq=c.get("num_attention_heads")
    hkv=c.get("num_key_value_heads",hq)
    dh=c.get("head_dim")
    if dh is None and d is not None and hq and d % hq == 0:
        dh=d//hq

    attn=None
    ffn=None
    if None not in (d,hq,hkv,dh):
        qw=hq*dh
        kvw=hkv*dh
        attn=d*qw + 2*d*kvw + qw*d
    if None not in (d,f):
        ffn=3*d*f

    moe_keys=[
        "num_local_experts","num_experts_per_tok","n_routed_experts",
        "num_experts","moe_intermediate_size"
    ]
    moe=[k for k in moe_keys if c.get(k) not in (None,False,0,[],{})]

    return {
        "path":str(path),
        "type":c.get("model_type","?"),
        "d":d,"f":f,"hq":hq,"hkv":hkv,"dh":dh,
        "attn":attn,"ffn":ffn,
        "ratio":(ffn/attn if ffn is not None and attn else None),
        "ffn_mib":(ffn*bits/8/(1024**2) if ffn is not None else None),
        "moe":moe
    }

def fmt(v,pattern="{}"):
    return "n/a" if v is None else pattern.format(v)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("configs",nargs="+")
    p.add_argument("--weight-bits",type=float,default=4.5)
    a=p.parse_args()

    print(f"effective weight storage proxy={a.weight_bits:g} bits/weight")
    print("| config | type | d | d_ff | Hq | Hkv | Dh | attn weights/layer | dense gated FFN/layer | FFN/attn | FFN MiB/layer | caveat |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for pth in a.configs:
        r=inspect(pth,a.weight_bits)
        caveat="MOE-CAVEAT:"+",".join(r["moe"]) if r["moe"] else "-"
        print(
            f"| {r['path']} | {r['type']} | {fmt(r['d'])} | {fmt(r['f'])} | "
            f"{fmt(r['hq'])} | {fmt(r['hkv'])} | {fmt(r['dh'])} | "
            f"{fmt(r['attn'],'{:,}')} | {fmt(r['ffn'],'{:,}')} | "
            f"{fmt(r['ratio'],'{:.3f}')} | {fmt(r['ffn_mib'],'{:.3f}')} | {caveat} |"
        )

    print()
    print("Dense 3*d*d_ff is a teaching baseline. Inspect model code for exact architecture.")

if __name__=="__main__":
    main()

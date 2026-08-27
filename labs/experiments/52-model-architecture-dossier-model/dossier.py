#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

GIB=1024**3

def human(n):
    if n is None: return "n/a"
    return f"{n/GIB:.3f} GiB"

def first(c,names):
    for n in names:
        if c.get(n) is not None:
            return n,c[n]
    return None,None

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("config",type=Path)
    p.add_argument("--context",type=int,required=True)
    p.add_argument("--kv-bits",type=float,default=16)
    p.add_argument("--sequences",type=int,default=1)
    p.add_argument("--params-b",type=float)
    p.add_argument("--weight-bpw",type=float)
    p.add_argument("--artifact",type=Path)
    p.add_argument("--reserve-gib",type=float,default=1)
    p.add_argument("--memory-gib",type=float)
    a=p.parse_args()

    raw=json.loads(a.config.read_text(encoding="utf-8"))
    c=raw.get("text_config",raw)

    d=c.get("hidden_size")
    L=c.get("num_hidden_layers")
    hq=c.get("num_attention_heads")
    hkv=c.get("num_key_value_heads",hq)
    dh=c.get("head_dim")
    if dh is None and d and hq and d%hq==0:
        dh=d//hq
    ff=c.get("intermediate_size")

    print("=== MODEL ARCHITECTURE DOSSIER ===")
    print(f"config: {a.config}")
    print(f"model_type: {c.get('model_type','?')}")
    print(f"layers={L} hidden={d} Hq={hq} Hkv={hkv} Dh={dh} d_ff={ff}")

    relation="unknown"
    if hq and hkv:
        if hkv==hq: relation="MHA-like"
        elif hkv==1: relation="MQA-like"
        elif hq%hkv==0: relation=f"GQA-like ({hq//hkv} Q/KV)"
        else: relation="architecture-specific"
    print(f"attention relation: {relation}")

    attn=None
    if None not in (d,hq,hkv,dh):
        qw=hq*dh; kvw=hkv*dh
        attn=d*qw+2*d*kvw+qw*d
        print(f"attention projection baseline/layer: {attn:,}")

    ffn=None
    if None not in (d,ff):
        ffn=3*d*ff
        print(f"dense gated FFN baseline/layer: {ffn:,}")
        if attn:
            print(f"FFN/attention ratio: {ffn/attn:.3f}x")

    kv=None
    if None not in (L,hkv,dh):
        kv=2*L*hkv*dh*(a.kv_bits/8)*a.context*a.sequences
        print(f"KV baseline @ context={a.context}, sequences={a.sequences}, {a.kv_bits:g}b: {human(kv)}")

    rn,N=first(c,["num_local_experts","n_routed_experts","num_experts"])
    kn,k=first(c,["num_experts_per_tok","num_selected_experts"])
    sn,s=first(c,["n_shared_experts","num_shared_experts"])
    fn,eff=first(c,["moe_intermediate_size","intermediate_size"])
    if N is not None:
        print("=== MoE ===")
        print(f"routed experts={N} ({rn}), top-k={k} ({kn}), shared={s} ({sn})")
        if d is not None and eff is not None:
            pe=3*d*eff
            print(f"common expert baseline: {pe:,} weights")
            print(f"all routed experts/layer: {pe*N:,} weights")
            if k is not None: print(f"active routed expert baseline/token/layer: {pe*k:,} weights")
        for key in ["first_k_dense_replace","moe_layer_freq","layer_types","sliding_window"]:
            if c.get(key) not in (None,False,0,[],{}):
                print(f"CAVEAT {key}={c[key]!r}")

    weight_bytes=None
    source=None
    if a.artifact is not None:
        weight_bytes=a.artifact.stat().st_size
        source="actual artifact bytes"
        print(f"artifact: {a.artifact}")
        print(f"artifact SHA256: {sha256(a.artifact)}")
    elif a.params_b is not None and a.weight_bpw is not None:
        weight_bytes=a.params_b*1e9*a.weight_bpw/8
        source="parameter × effective-bpw proxy"

    if weight_bytes is not None:
        print(f"weight/artifact planning value: {human(weight_bytes)} ({source})")

    reserve=a.reserve_gib*GIB
    lower=None
    if weight_bytes is not None and kv is not None:
        lower=weight_bytes+kv+reserve
        print(f"capacity lower bound incl reserve: {human(lower)}")
        if a.memory_gib is not None:
            mem=a.memory_gib*GIB
            verdict="FAIL-WITHOUT-OFFLOAD" if lower>mem else "POSSIBLE-NOT-PROVEN"
            print(f"usable memory input: {a.memory_gib:.3f} GiB")
            print(f"capacity verdict: {verdict}")

    caveats=[]
    for key in ["sliding_window","layer_types","rope_scaling","attention_chunk_size"]:
        if c.get(key) not in (None,False,0,[],{}): caveats.append(key)
    if caveats:
        print("architecture caveats: "+", ".join(caveats))
        print("homogeneous KV/dense baseline may be incomplete")

    print("=== HYPOTHESES TO TEST ===")
    print("- PP: large-token matrix/attention kernel efficiency; benchmark required")
    print("- TG: if fully resident, weight bandwidth is a candidate bottleneck; benchmark required")
    if hkv and hq and hkv<hq:
        print("- GQA/MQA structure reduces homogeneous KV vs same-Hq MHA")
    if N is not None:
        print("- MoE: expert placement/routing/batching/offload may dominate; active params do not prove fit")

if __name__=="__main__":
    main()

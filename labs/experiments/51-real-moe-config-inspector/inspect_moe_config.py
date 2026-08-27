#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def first(c, names):
    for n in names:
        if c.get(n) is not None:
            return n,c.get(n)
    return None,None

def human(n):
    if n is None:
        return "n/a"
    if n >= 1024**3:
        return f"{n/1024**3:.4f} GiB"
    return f"{n/1024**2:.4f} MiB"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("config",type=Path)
    p.add_argument("--weight-bits",type=float,default=4.5)
    a=p.parse_args()

    raw=json.loads(a.config.read_text(encoding="utf-8"))
    c=raw.get("text_config",raw)

    routed_name,n=first(c,["num_local_experts","n_routed_experts","num_experts"])
    topk_name,k=first(c,["num_experts_per_tok","num_selected_experts"])
    shared_name,s=first(c,["n_shared_experts","num_shared_experts"])
    f_name,f=first(c,["moe_intermediate_size","intermediate_size"])
    d=c.get("hidden_size")
    layers=c.get("num_hidden_layers")

    print(f"config: {a.config}")
    print(f"model_type: {c.get('model_type','?')}")
    print(f"hidden_size: {d}")
    print(f"layers: {layers}")
    print(f"routed experts: {n!r} (field={routed_name})")
    print(f"top-k: {k!r} (field={topk_name})")
    print(f"shared experts: {s!r} (field={shared_name})")
    print(f"expert intermediate: {f!r} (field={f_name})")
    print(f"storage proxy: {a.weight_bits:g} bits/weight")

    if None not in (d,f):
        pexpert=3*d*f
        ebytes=pexpert*a.weight_bits/8
        print()
        print("=== common SwiGLU-like expert baseline ===")
        print(f"expert weights: {pexpert:,}")
        print(f"expert storage: {human(ebytes)}")
        if n is not None:
            print(f"all routed experts/layer: {human(ebytes*n)}")
        if k is not None:
            print(f"active routed experts/token/layer: {human(ebytes*k)}")
        if isinstance(s,(int,float)) and s:
            print(f"shared experts/layer baseline: {human(ebytes*s)}")
            if k is not None:
                print(f"routed+shared active baseline/token/layer: {human(ebytes*(k+s))}")

    print()
    print("=== architecture fields requiring inspection ===")
    keys=[
        "first_k_dense_replace","moe_layer_freq","router_aux_loss_coef",
        "router_jitter_noise","norm_topk_prob","scoring_func",
        "routed_scaling_factor","shared_expert_intermediate_size",
        "expert_intermediate_size","ep_size","topk_group","n_group"
    ]
    found=False
    for key in keys:
        if key in c and c.get(key) not in (None,False,0,[],{}):
            found=True
            print(f"{key}: {c[key]!r}")
    if not found:
        print("- no listed special fields found; model code may still contain architecture-specific behavior")

    print()
    print("WARNING: 3*d*d_ff is a common expert baseline, not proof of exact expert implementation.")
    print("Do not equate active routed expert storage with full model memory.")

if __name__=="__main__":
    main()

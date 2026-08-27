#!/usr/bin/env python3
import argparse

GIB=1024**3

def size_gib(n):
    return n/GIB

def calc(context,layers,full,window,hkv,dh,bits):
    local=layers-full
    elem=bits/8
    per_position_layer=2*hkv*dh*elem
    full_pos=layers*context
    local_pos=layers*min(context,window)
    hybrid_pos=full*context + local*min(context,window)
    return {
        "full_pos":full_pos,
        "local_pos":local_pos,
        "hybrid_pos":hybrid_pos,
        "full":full_pos*per_position_layer,
        "local":local_pos*per_position_layer,
        "hybrid":hybrid_pos*per_position_layer,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--layers",type=int,default=32)
    p.add_argument("--full-layers",type=int,default=8)
    p.add_argument("--window",type=int,default=4096)
    p.add_argument("--kv-heads",type=int,default=8)
    p.add_argument("--head-dim",type=int,default=128)
    p.add_argument("--kv-bits",type=float,default=16)
    p.add_argument("--contexts",default="32768,131072")
    a=p.parse_args()

    if not 0 <= a.full_layers <= a.layers:
        raise SystemExit("full-layers must be between 0 and layers")

    local=a.layers-a.full_layers
    print("SYNTHETIC HYBRID ATTENTION MODEL")
    print(
        f"L={a.layers} full={a.full_layers} local={local} W={a.window} "
        f"Hkv={a.kv_heads} Dh={a.head_dim} KV={a.kv_bits:g}b"
    )
    print()
    print("| context | all-full GiB | all-local GiB | hybrid GiB | hybrid/full |")
    print("|---:|---:|---:|---:|---:|")
    for s in [int(x) for x in a.contexts.split(",")]:
        r=calc(s,a.layers,a.full_layers,a.window,a.kv_heads,a.head_dim,a.kv_bits)
        print(
            f"| {s} | {size_gib(r['full']):.3f} | {size_gib(r['local']):.3f} | "
            f"{size_gib(r['hybrid']):.3f} | {r['hybrid']/r['full']:.4f} |"
        )
        print(
            f"  cached position-layer counts: full={r['full_pos']:,}, "
            f"local={r['local_pos']:,}, hybrid={r['hybrid_pos']:,}"
        )

if __name__=="__main__":
    main()

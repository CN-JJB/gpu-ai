#!/usr/bin/env python3
import argparse,json
from pathlib import Path

GIB=1024**3

def human(n):
    return f"{n/GIB:.3f} GiB"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("config",type=Path)
    p.add_argument("--context",type=int,required=True)
    p.add_argument("--kv-bits",type=float,default=16)
    p.add_argument("--sequences",type=int,default=1)
    p.add_argument("--assume-all-sliding",action="store_true")
    p.add_argument("--deepseek-mla-proxy",action="store_true")
    a=p.parse_args()

    raw=json.loads(a.config.read_text(encoding="utf-8"))
    c=raw.get("text_config",raw)

    L=c.get("num_hidden_layers")
    hq=c.get("num_attention_heads")
    hkv=c.get("num_key_value_heads",hq)
    d=c.get("hidden_size")
    dh=c.get("head_dim")
    if dh is None and d and hq and d%hq==0:
        dh=d//hq
    W=c.get("sliding_window")
    layer_types=c.get("layer_types")

    print(f"config: {a.config}")
    print(f"model_type: {c.get('model_type','?')}")
    print(f"L={L} Hq={hq} Hkv={hkv} Dh={dh} context={a.context} KV={a.kv_bits:g}b")
    print(f"sliding_window: {W!r}")
    print(f"layer_types: {layer_types!r}")

    elem=a.kv_bits/8
    if None not in (L,hkv,dh):
        full=2*L*hkv*dh*elem*a.context*a.sequences
        print(f"homogeneous full-attention baseline: {human(full)}")

    if a.assume_all_sliding:
        if None in (L,hkv,dh,W):
            print("all-sliding estimate: UNKNOWN (missing L/Hkv/Dh/W)")
        else:
            local=2*L*hkv*dh*elem*min(a.context,W)*a.sequences
            print(f"all-sliding estimate: {human(local)}")
            print("EVIDENCE REQUIREMENT: caller asserted all layers use this window.")

    if isinstance(layer_types,list) and None not in (hkv,dh,W):
        full_count=0
        local_count=0
        unknown=[]
        for i,t in enumerate(layer_types):
            s=str(t).lower()
            if "sliding" in s or "local" in s:
                local_count+=1
            elif "full" in s or "global" in s:
                full_count+=1
            else:
                unknown.append((i,t))
        if not unknown and full_count+local_count==len(layer_types):
            pos=full_count*a.context+local_count*min(a.context,W)
            hybrid=2*hkv*dh*elem*pos*a.sequences
            print(f"layer_types-derived hybrid: full={full_count} local={local_count} KV={human(hybrid)}")
        else:
            print(f"layer_types-derived hybrid: UNKNOWN; unclassified entries={unknown[:8]}")

    kv_rank=c.get("kv_lora_rank")
    rope_dim=c.get("qk_rope_head_dim")
    print(f"kv_lora_rank: {kv_rank!r}")
    print(f"qk_rope_head_dim: {rope_dim!r}")

    if a.deepseek_mla_proxy:
        if None in (L,kv_rank,rope_dim):
            print("DeepSeek-style MLA proxy: UNKNOWN (missing fields)")
        else:
            width=kv_rank+rope_dim
            cache=L*width*elem*a.context*a.sequences
            print(f"DeepSeek-style MLA cached-width proxy: {width} elements/token/layer")
            print(f"DeepSeek-style MLA cache proxy: {human(cache)}")
            print("EVIDENCE REQUIREMENT: exact DeepSeek-style cache formulation must be confirmed.")

    print()
    print("Do not interpret one sliding_window field as proof that every layer is local.")

if __name__=="__main__":
    main()

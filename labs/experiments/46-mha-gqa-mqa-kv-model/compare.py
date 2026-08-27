#!/usr/bin/env python3
import argparse

def human_bytes(n):
    if n >= 1024**3:
        return f"{n/(1024**3):.3f} GiB"
    if n >= 1024**2:
        return f"{n/(1024**2):.3f} MiB"
    if n >= 1024:
        return f"{n/1024:.3f} KiB"
    return f"{n:.0f} B"

def row(name,hkv,a):
    q_width = a.q_heads * a.head_dim
    kv_width = hkv * a.head_dim

    params = (
        a.hidden * q_width
        + a.hidden * kv_width
        + a.hidden * kv_width
        + q_width * a.hidden
    )

    kv_bytes_per_elem = a.kv_bits / 8
    kv_token = 2 * a.layers * hkv * a.head_dim * kv_bytes_per_elem
    kv_total = kv_token * a.context * a.sequences

    group = None
    if hkv and a.q_heads % hkv == 0:
        group = a.q_heads // hkv

    return {
        "name": name,
        "hkv": hkv,
        "group": group,
        "kv_token": kv_token,
        "kv_total": kv_total,
        "params": params,
        "kv_width": kv_width,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--layers",type=int,default=32)
    p.add_argument("--hidden",type=int,default=4096)
    p.add_argument("--q-heads",type=int,default=32)
    p.add_argument("--head-dim",type=int,default=128)
    p.add_argument("--kv-bits",type=int,default=16)
    p.add_argument("--context",type=int,default=32768)
    p.add_argument("--sequences",type=int,default=1)
    p.add_argument("--gqa-kv-heads",type=int,default=8)
    a=p.parse_args()

    rows=[
        row("MHA",a.q_heads,a),
        row(f"GQA-{a.gqa_kv_heads}",a.gqa_kv_heads,a),
        row("MQA",1,a),
    ]

    print("HOMOGENEOUS SYNTHETIC MODEL")
    print(
        f"L={a.layers} d={a.hidden} Hq={a.q_heads} Dh={a.head_dim} "
        f"KV={a.kv_bits}b context={a.context} sequences={a.sequences}"
    )
    print()
    print("| type | Hkv | Q/KV group | KV width | KV/token | KV total | attention proj params/layer |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        g = "n/a" if r["group"] is None else str(r["group"])
        print(
            f"| {r['name']} | {r['hkv']} | {g} | {r['kv_width']} | "
            f"{human_bytes(r['kv_token'])} | {human_bytes(r['kv_total'])} | "
            f"{r['params']:,} |"
        )

if __name__=="__main__":
    main()

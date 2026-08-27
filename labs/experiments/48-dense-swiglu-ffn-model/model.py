#!/usr/bin/env python3
import argparse

def mib(n):
    return n / (1024**2)

def shape(*dims):
    return "[" + ",".join(str(x) for x in dims) + "]"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--layers",type=int,default=32)
    p.add_argument("--hidden",type=int,default=4096)
    p.add_argument("--intermediate",type=int,default=11008)
    p.add_argument("--q-heads",type=int,default=32)
    p.add_argument("--kv-heads",type=int,default=32)
    p.add_argument("--head-dim",type=int,default=128)
    p.add_argument("--weight-bits",type=float,default=16.0)
    p.add_argument("--prefill-rows",type=int,default=512)
    p.add_argument("--decode-rows",type=int,default=1)
    a=p.parse_args()

    d=a.hidden
    f=a.intermediate
    qwidth=a.q_heads*a.head_dim
    kvwidth=a.kv_heads*a.head_dim

    ffn=3*d*f
    attn=d*qwidth + 2*d*kvwidth + qwidth*d
    ffn_bytes=ffn*a.weight_bits/8
    layer=ffn+attn

    print("DENSE FFN TEACHING MODEL")
    print(
        f"L={a.layers} d={d} d_ff={f} Hq={a.q_heads} "
        f"Hkv={a.kv_heads} Dh={a.head_dim} weight={a.weight_bits:g}b"
    )
    print()
    print("=== weights / layer ===")
    print(f"attention Q/K/V/O: {attn:,}")
    print(f"SwiGLU gate/up/down: {ffn:,}")
    print(f"FFN / attention ratio: {ffn/attn:.6f}")
    print(f"attention + FFN: {layer:,}")
    print(f"across {a.layers} layers: {layer*a.layers:,}")
    print()
    print("=== FFN storage ===")
    print(f"FFN weight bytes/layer: {ffn_bytes:,.0f}")
    print(f"FFN weight MiB/layer: {mib(ffn_bytes):.4f}")
    print()
    for label,m in [("prefill",a.prefill_rows),("decode",a.decode_rows)]:
        print(f"=== {label} shapes ===")
        print("X:   ",shape(m,d))
        print("gate:",shape(m,f))
        print("up:  ",shape(m,f))
        print("down:",shape(m,d))
        ai=16*m/a.weight_bits
        print(f"weight-only AI proxy: {ai:.4f} FLOP/weight-byte")
        print()
    print("Proxy ignores activation traffic, cache, dequant and kernel overhead.")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse

def shape(*x):
    return "[" + ",".join(str(v) for v in x) + "]"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--layers", type=int, default=2)
    p.add_argument("--hidden", type=int, default=16)
    p.add_argument("--q-heads", type=int, default=4)
    p.add_argument("--kv-heads", type=int, default=2)
    p.add_argument("--head-dim", type=int, default=4)
    p.add_argument("--ffn", type=int, default=32)
    p.add_argument("--kv-bytes", type=int, default=2)
    p.add_argument("--prompt", type=int, default=8)
    a = p.parse_args()

    b, t = a.batch, a.prompt
    hq, hkv, dh = a.q_heads, a.kv_heads, a.head_dim

    print("SYNTHETIC TOY MODEL")
    print()
    print("=== config ===")
    print(f"B={b} layers={a.layers} d={a.hidden} Hq={hq} Hkv={hkv} Dh={dh} d_ff={a.ffn}")
    if hq * dh != a.hidden:
        print("WARNING: Hq * Dh != hidden; allowed for shape study but verify real architecture.")
    print()

    print("=== prefill ===")
    print("X      ", shape(b, t, a.hidden))
    print("Q      ", shape(b, hq, t, dh))
    print("K      ", shape(b, hkv, t, dh))
    print("V      ", shape(b, hkv, t, dh))
    print("scores ", shape(b, hq, t, t), "(conceptual)")
    prefill_scores = b * hq * t * t
    print("score elements:", prefill_scores)

    kv_per_token = 2 * a.layers * hkv * dh * a.kv_bytes * b
    kv_prompt = kv_per_token * t

    print()
    print("=== KV ===")
    print(f"KV bytes/token across all layers: {kv_per_token}")
    print(f"KV bytes after prompt: {kv_prompt}")

    s = t + 1
    print()
    print("=== one-token decode ===")
    print("X_new   ", shape(b, 1, a.hidden))
    print("Q_new   ", shape(b, hq, 1, dh))
    print("K_new   ", shape(b, hkv, 1, dh))
    print("V_new   ", shape(b, hkv, 1, dh))
    print("K cache ", shape(b, hkv, s, dh), "per layer after append")
    print("V cache ", shape(b, hkv, s, dh), "per layer after append")
    print("scores  ", shape(b, hq, 1, s), "(conceptual)")
    decode_scores = b * hq * s
    print("score elements:", decode_scores)
    print(f"KV bytes after append: {kv_per_token * s}")

    attn_params = (
        a.hidden * (hq * dh)
        + a.hidden * (hkv * dh)
        + a.hidden * (hkv * dh)
        + (hq * dh) * a.hidden
    )
    gated_ffn_params = 3 * a.hidden * a.ffn

    print()
    print("=== rough dense projection parameters / layer ===")
    print(f"attention Q/K/V/O baseline: {attn_params}")
    print(f"gated MLP 3-matrix baseline: {gated_ffn_params}")
    print("These omit bias/norm and are not universal architecture counts.")

if __name__ == "__main__":
    main()

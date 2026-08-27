#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

def fmt_bytes(n):
    gib = n / (1024**3)
    mib = n / (1024**2)
    if gib >= 0.1:
        return f"{n:,} bytes ({gib:.3f} GiB)"
    return f"{n:,} bytes ({mib:.3f} MiB)"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("config", type=Path)
    p.add_argument("--context", type=int)
    p.add_argument("--kv-bits", type=int, default=16)
    p.add_argument("--sequences", type=int, default=1)
    a = p.parse_args()

    raw = json.loads(a.config.read_text(encoding="utf-8"))
    c = raw.get("text_config", raw)

    def get(k, default=None):
        return c.get(k, default)

    hidden = get("hidden_size")
    layers = get("num_hidden_layers")
    hq = get("num_attention_heads")
    hkv = get("num_key_value_heads", hq)
    dh = get("head_dim")

    derived_dh = False
    if dh is None and hidden is not None and hq:
        if hidden % hq == 0:
            dh = hidden // hq
            derived_dh = True

    print(f"config: {a.config}")
    for k in [
        "model_type", "architectures", "vocab_size", "hidden_size",
        "intermediate_size", "num_hidden_layers", "num_attention_heads",
        "num_key_value_heads", "head_dim", "hidden_act", "rms_norm_eps",
        "rope_theta", "rope_scaling", "max_position_embeddings",
        "sliding_window", "tie_word_embeddings"
    ]:
        if k in c:
            print(f"{k}: {c[k]!r}")

    print()
    print("=== derived attention anatomy ===")
    print(f"layers: {layers}")
    print(f"query heads: {hq}")
    print(f"KV heads: {hkv}")
    print(f"head_dim: {dh}" + (" (derived hidden_size // query_heads)" if derived_dh else ""))

    if None not in (hidden, hq, hkv, dh):
        q_width = hq * dh
        kv_width = hkv * dh
        print(f"Q projection output width: {q_width}")
        print(f"K/V projection output width: {kv_width}")

        if hkv == hq:
            attn = "MHA-like KV head count"
        elif hkv == 1:
            attn = "MQA-like KV head count"
        elif hq % hkv == 0:
            attn = f"GQA-like, {hq // hkv} query heads per KV head"
        else:
            attn = "non-standard/architecture-specific head ratio"
        print(f"head relation: {attn}")

    if None not in (layers, hkv, dh):
        kv_bytes_per_elem = a.kv_bits / 8
        kv_per_token = 2 * layers * hkv * dh * kv_bytes_per_elem * a.sequences
        print()
        print("=== homogeneous KV baseline ===")
        print(f"KV bits/element: {a.kv_bits}")
        print(f"active sequences: {a.sequences}")
        print(f"KV bytes/token across all layers: {fmt_bytes(int(kv_per_token))}")
        if a.context is not None:
            print(f"context: {a.context}")
            print(f"KV total baseline: {fmt_bytes(int(kv_per_token * a.context))}")
        else:
            print("context not provided; pass --context for total estimate")

    inter = get("intermediate_size")
    if None not in (hidden, inter):
        dense_gated = 3 * hidden * inter
        print()
        print("=== dense gated-MLP projection baseline ===")
        print(f"3 × hidden × intermediate = {dense_gated:,} weights/layer")
        print("This is a teaching baseline, not proof the architecture uses exactly 3 dense matrices.")

    flags = []
    for k in [
        "sliding_window", "rope_scaling", "layer_types",
        "num_local_experts", "num_experts_per_tok", "n_routed_experts",
        "num_experts", "moe_intermediate_size", "attention_chunk_size"
    ]:
        v = c.get(k)
        if v not in (None, False, 0, [], {}):
            flags.append((k, v))

    if flags:
        print()
        print("=== architecture features requiring model-specific interpretation ===")
        for k, v in flags:
            print(f"{k}: {v!r}")
        print("Do not blindly apply the homogeneous dense/full-attention baseline.")

if __name__ == "__main__":
    main()

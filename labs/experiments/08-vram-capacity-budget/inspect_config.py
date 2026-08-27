#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

from budget import calculate, print_budget


def parse_args():
    p = argparse.ArgumentParser(
        description="Inspect a Hugging Face-style config.json and estimate KV/VRAM baseline."
    )
    p.add_argument("config", type=Path)
    p.add_argument("--params-b", type=float, required=True)
    p.add_argument("--weight-bpw", type=float, required=True)
    p.add_argument("--kv-bits", type=int, default=16)
    p.add_argument("--context", type=int, required=True)
    p.add_argument("--concurrency", type=int, default=1)
    p.add_argument("--reserve-gib", type=float, default=1.0)
    p.add_argument("--vram-gib", type=float)
    return p.parse_args()


def main():
    args = parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    config = raw.get("text_config", raw)

    layers = config.get("num_hidden_layers")
    hidden_size = config.get("hidden_size")
    attention_heads = config.get("num_attention_heads")
    kv_heads = config.get("num_key_value_heads")

    if kv_heads is None:
        kv_heads = attention_heads

    head_dim = config.get("head_dim")
    used_head_dim_fallback = False

    if head_dim is None and hidden_size is not None and attention_heads:
        if hidden_size % attention_heads != 0:
            raise SystemExit(
                "head_dim missing and hidden_size is not divisible by num_attention_heads."
            )
        head_dim = hidden_size // attention_heads
        used_head_dim_fallback = True

    required = {
        "num_hidden_layers": layers,
        "num_attention_heads": attention_heads,
        "num_key_value_heads": kv_heads,
        "head_dim": head_dim,
    }

    missing = [name for name, value in required.items() if value is None]

    if missing:
        raise SystemExit(
            "Config does not expose enough fields for this baseline: "
            + ", ".join(missing)
        )

    print(f"config: {args.config}")
    print(f"layers: {layers}")
    print(f"hidden_size: {hidden_size}")
    print(f"attention heads: {attention_heads}")
    print(f"KV heads: {kv_heads}")
    print(
        f"head_dim: {head_dim}"
        + (" (derived as hidden_size // attention_heads)" if used_head_dim_fallback else "")
    )

    warnings = []

    for key in [
        "sliding_window",
        "layer_types",
        "per_layer_config",
        "attention_chunk_size",
    ]:
        if key in config and config.get(key) not in (None, [], {}, 0):
            warnings.append(key)

    if warnings:
        print()
        print(
            "WARNING: config contains architecture features this homogeneous "
            "full-attention baseline does not model: "
            + ", ".join(warnings)
        )

    print()
    budget = calculate(
        params_b=args.params_b,
        weight_bpw=args.weight_bpw,
        layers=int(layers),
        attention_heads=int(attention_heads),
        kv_heads=int(kv_heads),
        head_dim=int(head_dim),
        kv_bits=args.kv_bits,
        context=args.context,
        concurrency=args.concurrency,
        reserve_gib=args.reserve_gib,
        vram_gib=args.vram_gib,
    )

    print_budget(budget, args.context, args.concurrency)


if __name__ == "__main__":
    main()

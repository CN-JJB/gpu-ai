#!/usr/bin/env python3

import argparse

GIB = 1024 ** 3


def quant_region_bpw(qbits, group_size, scale_bits, zero_bits):
    if group_size <= 0:
        raise ValueError("group_size must be positive")
    return qbits + (scale_bits + zero_bits) / group_size


def whole_model_bpw(quant_bpw, quant_fraction, unquantized_bits):
    if not 0.0 <= quant_fraction <= 1.0:
        raise ValueError("quant_fraction must be in [0, 1]")
    return quant_fraction * quant_bpw + (1.0 - quant_fraction) * unquantized_bits


def payload_gib(params_b, bpw):
    return params_b * 1e9 * bpw / 8.0 / GIB


def run_demo():
    print("Concept model: code bits + per-group metadata; not a real format simulator.")
    print()
    print("A) 4-bit codes + one FP16 scale per group")
    print(f"{'group':>7} {'quant bpw':>12} {'7B payload GiB':>16}")
    print("-" * 39)
    for group in [32, 64, 128]:
        bpw = quant_region_bpw(4, group, 16, 0)
        print(f"{group:>7} {bpw:>12.3f} {payload_gib(7, bpw):>16.3f}")

    print()
    print("B) 4-bit codes + FP16 scale + FP16 zero per group")
    print(f"{'group':>7} {'quant bpw':>12} {'7B payload GiB':>16}")
    print("-" * 39)
    for group in [32, 64, 128]:
        bpw = quant_region_bpw(4, group, 16, 16)
        print(f"{group:>7} {bpw:>12.3f} {payload_gib(7, bpw):>16.3f}")

    print()
    print("C) 95% quantized at group64 scale-only; 5% remains FP16")
    q = quant_region_bpw(4, 64, 16, 0)
    overall = whole_model_bpw(q, 0.95, 16)
    print(f"quant region bpw: {q:.4f}")
    print(f"whole-model bpw: {overall:.4f}")
    print(f"7B payload: {payload_gib(7, overall):.3f} GiB")
    print(f"pure 4-bit baseline: {payload_gib(7, 4):.3f} GiB")


def main():
    p = argparse.ArgumentParser(description="Effective bits-per-weight concept calculator.")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--params-b", type=float)
    p.add_argument("--qbits", type=float)
    p.add_argument("--group-size", type=int)
    p.add_argument("--scale-bits", type=float, default=16)
    p.add_argument("--zero-bits", type=float, default=0)
    p.add_argument("--quant-fraction", type=float, default=1.0)
    p.add_argument("--unquantized-bits", type=float, default=16)
    a = p.parse_args()

    if a.demo:
        run_demo()
        return

    missing = [n for n, v in {
        "--params-b": a.params_b,
        "--qbits": a.qbits,
        "--group-size": a.group_size,
    }.items() if v is None]
    if missing:
        raise SystemExit("Missing required arguments: " + ", ".join(missing))

    q = quant_region_bpw(a.qbits, a.group_size, a.scale_bits, a.zero_bits)
    overall = whole_model_bpw(q, a.quant_fraction, a.unquantized_bits)
    print(f"quant-region bpw: {q:.4f}")
    print(f"whole-model effective bpw: {overall:.4f}")
    print(f"weight payload baseline: {payload_gib(a.params_b, overall):.3f} GiB")
    print("NOTE: excludes alignment, format headers, tensor-specific schemes, runtime repacking and non-weight VRAM.")


if __name__ == "__main__":
    main()

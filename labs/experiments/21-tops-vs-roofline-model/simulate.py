#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class Path:
    name: str
    peak_tops: float
    prefill_util: float
    decode_util: float
    overhead: float
    note: str

PATHS = [
    Path("fp32",          50, 0.85, 0.30, 0.00, "baseline vector/scalar-like peak"),
    Path("fp16_matrix",  200, 0.90, 0.12, 0.00, "matrix unit"),
    Path("int8_matrix",  400, 0.80, 0.08, 0.05, "native low precision + small overhead"),
    Path("int4_native",  800, 0.65, 0.05, 0.08, "native low-bit matrix path"),
    Path("q4_weight_only",200,0.85, 0.12, 0.10, "4-bit storage, FP16-like compute after dequant"),
]

PROFILES = {
    "prefill_like": {"ai": 200.0, "util_field": "prefill_util"},
    "decode_like":  {"ai":   4.0, "util_field": "decode_util"},
}

BANDWIDTH_TB_S = 1.0

def main():
    print("SYNTHETIC ONLY — no real GPU claim")
    print(f"memory bandwidth = {BANDWIDTH_TB_S:.1f} TB/s")
    print()

    for profile, cfg in PROFILES.items():
        print(f"=== {profile} ===")
        print(f"arithmetic intensity = {cfg['ai']:.1f} ops/byte")
        memory_roof_tops = BANDWIDTH_TB_S * cfg["ai"]
        print(f"memory roof = {memory_roof_tops:.1f} TOPS-equivalent")
        print(f"{'path':18} {'peak':>8} {'util':>8} {'compute':>10} {'effective':>11}")
        for p in PATHS:
            util = getattr(p, cfg["util_field"])
            compute_roof = p.peak_tops * util
            achieved = min(compute_roof, memory_roof_tops)
            effective = achieved / (1.0 + p.overhead)
            print(f"{p.name:18} {p.peak_tops:8.1f} {util:8.2f} {compute_roof:10.1f} {effective:11.1f}")
        print()

    print("Interpret q4_weight_only carefully:")
    print("- storage is low-bit")
    print("- compute peak is intentionally FP16-like")
    print("- speedup can come from lower bytes, not native INT4 arithmetic")

if __name__ == "__main__":
    main()

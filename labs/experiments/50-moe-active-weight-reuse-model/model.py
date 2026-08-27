#!/usr/bin/env python3
import argparse

def human(n):
    if n >= 1024**3:
        return f"{n/1024**3:.4f} GiB"
    return f"{n/1024**2:.4f} MiB"

def analyze(name, counts, expert_bytes, devices):
    tokens = sum(counts)
    # counts are expert assignments; caller passes actual token count separately.
    unique = sum(1 for x in counts if x > 0)
    total_assignments = sum(counts)
    avg = total_assignments / len(counts)
    max_load = max(counts)
    imbalance = max_load / avg if avg else 0

    per_device = [0] * devices
    experts_per_device = len(counts) // devices
    for e,c in enumerate(counts):
        dev = min(e // experts_per_device, devices-1)
        per_device[dev] += c
    davg = sum(per_device) / devices
    dimbalance = max(per_device) / davg if davg else 0

    return {
        "name":name,
        "unique":unique,
        "assignment_counts":counts,
        "expert_imbalance":imbalance,
        "device_assignments":per_device,
        "device_imbalance":dimbalance,
        "ideal_unique_bytes":unique*expert_bytes,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--hidden",type=int,default=4096)
    p.add_argument("--expert-ffn",type=int,default=14336)
    p.add_argument("--experts",type=int,default=8)
    p.add_argument("--top-k",type=int,default=2)
    p.add_argument("--layers",type=int,default=32)
    p.add_argument("--weight-bits",type=float,default=4.5)
    p.add_argument("--batch-tokens",type=int,default=16)
    p.add_argument("--devices",type=int,default=4)
    a=p.parse_args()

    if a.experts != 8 or a.top_k != 2 or a.batch_tokens != 16:
        raise SystemExit("default routing patterns currently require experts=8, top-k=2, batch-tokens=16")
    if a.experts % a.devices:
        raise SystemExit("experts must divide evenly across devices for this teaching placement")

    pexpert=3*a.hidden*a.expert_ffn
    expert_bytes=pexpert*a.weight_bits/8
    all_layer=expert_bytes*a.experts
    active_layer=expert_bytes*a.top_k

    print("SYNTHETIC MOE TEACHING MODEL")
    print(
        f"d={a.hidden} expert_ffn={a.expert_ffn} N={a.experts} k={a.top_k} "
        f"L_moe={a.layers} weight={a.weight_bits:g}b batch={a.batch_tokens}"
    )
    print()
    print("=== expert accounting ===")
    print(f"one expert weights: {pexpert:,}")
    print(f"one expert storage: {human(expert_bytes)}")
    print(f"all routed experts/layer: {human(all_layer)}")
    print(f"selected top-k storage/layer: {human(active_layer)}")
    print(f"all routed experts across layers: {human(all_layer*a.layers)}")
    print(f"top-k no-reuse proxy across layers/token: {human(active_layer*a.layers)}")

    patterns=[
        ("balanced",[4,4,4,4,4,4,4,4]),
        ("skewed",[16,16,0,0,0,0,0,0]),
    ]

    print()
    print("=== routing batch ===")
    for name,counts in patterns:
        r=analyze(name,counts,expert_bytes,a.devices)
        per_token=r["ideal_unique_bytes"]/a.batch_tokens
        print(f"{name}:")
        print(f"  expert assignments: {r['assignment_counts']}")
        print(f"  unique experts touched: {r['unique']}")
        print(f"  expert max/avg load: {r['expert_imbalance']:.3f}x")
        print(f"  per-device assignments: {r['device_assignments']}")
        print(f"  device max/avg load: {r['device_imbalance']:.3f}x")
        print(f"  ideal unique expert bytes/layer: {human(r['ideal_unique_bytes'])}")
        print(f"  ideal weight bytes/token/layer: {human(per_token)}")

    print()
    print("Ideal bytes ignore finite cache, dequant, activations, dispatch and kernel overhead.")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse

def yn(v):
    return "YES" if v else "NO"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--total-gib", type=float, default=32.0)
    p.add_argument("--system-reserve-gib", type=float, default=6.0)
    p.add_argument("--safety-gib", type=float, default=3.0)
    p.add_argument("--weights-gib", type=float, default=18.0)
    p.add_argument("--kv-gib", type=float, default=2.0)
    p.add_argument("--workspace-gib", type=float, default=1.0)
    p.add_argument("--bandwidth-gib-s", type=float, default=200.0)
    p.add_argument("--other-traffic-gib-s", type=float, default=40.0)
    p.add_argument("--discrete-vram-gib", type=float, default=16.0)
    a = p.parse_args()

    safe_budget = max(0.0, a.total_gib - a.system_reserve_gib - a.safety_gib)
    runtime = a.weights_gib + a.kv_gib + a.workspace_gib
    margin = safe_budget - runtime

    full_bw_roof = a.bandwidth_gib_s / a.weights_gib if a.weights_gib > 0 else float("inf")
    model_bw = max(0.0, a.bandwidth_gib_s - a.other_traffic_gib_s)
    contested_roof = model_bw / a.weights_gib if a.weights_gib > 0 else float("inf")

    print("SYNTHETIC ONLY — no real Apple SKU claim")
    print()
    print("=== capacity ===")
    print(f"installed unified memory : {a.total_gib:.2f} GiB")
    print(f"system/apps reserve      : {a.system_reserve_gib:.2f} GiB")
    print(f"safety headroom          : {a.safety_gib:.2f} GiB")
    print(f"safe workload budget     : {safe_budget:.2f} GiB")
    print(f"weights                  : {a.weights_gib:.2f} GiB")
    print(f"KV                       : {a.kv_gib:.2f} GiB")
    print(f"workspace/runtime        : {a.workspace_gib:.2f} GiB")
    print(f"runtime footprint        : {runtime:.2f} GiB")
    print(f"unified-memory fit       : {yn(runtime <= safe_budget)}")
    print(f"margin                   : {margin:.2f} GiB")
    print()
    print(f"comparison dGPU VRAM     : {a.discrete_vram_gib:.2f} GiB")
    print(f"full-GPU-resident fit    : {yn(runtime <= a.discrete_vram_gib)}")
    print()
    print("=== decode bandwidth roof ===")
    print(f"total bandwidth          : {a.bandwidth_gib_s:.2f} GiB/s")
    print(f"other traffic demand     : {a.other_traffic_gib_s:.2f} GiB/s")
    print(f"model bandwidth budget   : {model_bw:.2f} GiB/s")
    print(f"full-bandwidth TG roof   : {full_bw_roof:.3f} token/s")
    print(f"contended TG roof        : {contested_roof:.3f} token/s")
    print()
    print("Interpretation:")
    print("- capacity and bandwidth are separate roofs")
    print("- unified memory removes a discrete VRAM pool boundary")
    print("- it does not make the shared memory subsystem infinite")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse

def gib_per_s_to_mib_per_ms(v):
    return v * 1024 / 1000

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--single-ms", type=float, default=10.0)
    p.add_argument("--gpus", type=int, default=2)
    p.add_argument("--transfer-mib", type=float, default=64.0)
    p.add_argument("--sync-ms", type=float, default=0.2)
    p.add_argument("--imbalance-ms", type=float, default=0.0)
    p.add_argument("--bandwidth", type=float, nargs="+", default=[8,16,32,64,128])
    a = p.parse_args()

    print(f"single GPU baseline: {a.single_ms:.3f} ms/token")
    print(f"GPUs: {a.gpus}")
    print(f"critical transfer: {a.transfer_mib:.3f} MiB/token")
    print()
    print(f"{'GiB/s':>8} {'comm_ms':>10} {'total_ms':>10} {'speedup':>10} {'eff':>10}")
    for bw in a.bandwidth:
        comm_ms = a.transfer_mib / gib_per_s_to_mib_per_ms(bw)
        total = a.single_ms / a.gpus + comm_ms + a.sync_ms + a.imbalance_ms
        speedup = a.single_ms / total
        efficiency = speedup / a.gpus
        print(f"{bw:8.2f} {comm_ms:10.4f} {total:10.4f} {speedup:10.4f} {efficiency:10.4f}")

if __name__ == "__main__":
    main()

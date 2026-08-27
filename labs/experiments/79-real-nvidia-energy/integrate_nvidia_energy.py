#!/usr/bin/env python3
import argparse,csv
from pathlib import Path

def parse_power(path,selected):
    total=0.0
    found=0
    with path.open(encoding="utf-8",errors="replace") as f:
        for row in csv.reader(f):
            if len(row)<8:
                continue
            try:
                idx=int(row[1].strip())
                power=float(row[7].strip())
            except ValueError:
                continue
            if selected and idx not in selected:
                continue
            total += power
            found += 1
    if found==0:
        raise ValueError(f"no usable NVIDIA power rows in {path}")
    return total,found

def main():
    p=argparse.ArgumentParser()
    p.add_argument("timeline",type=Path)
    p.add_argument("vendor_dir",type=Path)
    p.add_argument("--output-tokens",type=int,required=True)
    p.add_argument("--gpu-index",type=int,action="append",default=[])
    p.add_argument("--idle-watts",type=float)
    p.add_argument("--price-per-kwh",type=float)
    a=p.parse_args()

    if a.output_tokens<=0:
        raise SystemExit("output-tokens must be >0")
    if a.idle_watts is not None and a.idle_watts<0:
        raise SystemExit("idle-watts must be >=0")
    selected=set(a.gpu_index)

    rows=list(csv.DictReader(a.timeline.open(encoding="utf-8")))
    samples=[]
    gpu_counts=set()

    for r in rows:
        i=int(r["sample"])
        t=float(r["elapsed_s"])
        path=a.vendor_dir/f"{i:04d}-nvidia.csv"
        if not path.is_file():
            raise SystemExit(f"missing vendor sample: {path}")
        try:
            power,count=parse_power(path,selected)
        except ValueError as e:
            raise SystemExit(str(e))
        samples.append((t,power))
        gpu_counts.add(count)

    if len(samples)<2:
        raise SystemExit("need at least two power samples")
    if len(gpu_counts)!=1:
        raise SystemExit("selected GPU count changed across samples")

    samples.sort()
    energy=0.0
    incremental=0.0
    for (t0,p0),(t1,p1) in zip(samples,samples[1:]):
        dt=t1-t0
        if dt<=0:
            raise SystemExit("timeline elapsed_s must be strictly increasing")
        energy += 0.5*(p0+p1)*dt
        if a.idle_watts is not None:
            q0=max(p0-a.idle_watts,0)
            q1=max(p1-a.idle_watts,0)
            incremental += 0.5*(q0+q1)*dt

    duration=samples[-1][0]-samples[0][0]
    avg_power=energy/duration
    jpt=energy/a.output_tokens
    tpj=a.output_tokens/energy

    print("NVIDIA BOARD-ENERGY INTEGRATION")
    print(f"selected_gpu_count: {next(iter(gpu_counts))}")
    print(f"duration_s: {duration:.6f}")
    print(f"energy_j: {energy:.6f}")
    print(f"average_board_power_w: {avg_power:.6f}")
    print(f"output_tokens: {a.output_tokens}")
    print(f"J/output-token: {jpt:.6f}")
    print(f"output-tokens/J: {tpj:.9f}")
    print(f"output-tok/s: {a.output_tokens/duration:.6f}")

    if a.idle_watts is not None:
        print(f"aggregate_idle_baseline_w: {a.idle_watts:.6f}")
        print(f"incremental_energy_j: {incremental:.6f}")
        print(f"incremental_J/output-token: {incremental/a.output_tokens:.6f}")

    kwh=energy/3_600_000
    print(f"board_energy_kWh: {kwh:.9f}")
    if a.price_per_kwh is not None:
        print(f"board_energy_cost: {kwh*a.price_per_kwh:.9f}")

    print()
    print("WARNING: NVIDIA board power is not whole-system wall power.")
    print("WARNING: sampled/integrated telemetry is an approximation.")

if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse,csv
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("scenarios",type=Path)
    p.add_argument("--price-per-kwh",type=float,default=0.20)
    a=p.parse_args()

    rows=list(csv.DictReader(a.scenarios.open(encoding="utf-8")))
    print("SYNTHETIC ENERGY MODEL")
    for r in rows:
        name=r["name"]
        power=float(r["power_w"])
        rate=float(r["tok_s"])
        tokens=float(r["output_tokens"])
        idle=float(r["idle_w"])

        duration=tokens/rate
        energy=power*duration
        jpt=energy/tokens
        tpj=tokens/energy
        incremental=max(power-idle,0)*duration
        inc_jpt=incremental/tokens
        kwh_per_million=jpt*1_000_000/3_600_000
        cost=kwh_per_million*a.price_per_kwh

        print(name)
        print(f"  duration_s: {duration:.6f}")
        print(f"  total_energy_j: {energy:.6f}")
        print(f"  J/output-token: {jpt:.6f}")
        print(f"  output-tokens/J: {tpj:.6f}")
        print(f"  incremental_J/token_above_idle: {inc_jpt:.6f}")
        print(f"  kWh_per_1M_output_tokens: {kwh_per_million:.6f}")
        print(f"  cost_per_1M_at_price: {cost:.6f}")
        print()

    print("All powers/rates are synthetic constants.")
    print("Cost is synthetic GPU-board-energy arithmetic, not whole-system TCO.")

if __name__=="__main__":
    main()

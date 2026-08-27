#!/usr/bin/env python3
import argparse,csv
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("scenarios",type=Path)
    a=p.parse_args()

    rows=list(csv.DictReader(a.scenarios.open(encoding="utf-8")))
    if not rows:
        raise SystemExit("empty scenarios")

    print("SYNTHETIC MODEL-LOAD STAGE MODEL")
    for r in rows:
        name=r["name"]
        model=float(r["model_gib"])
        source=float(r["source_bw_gib_s"])
        host=float(r["host_backend_s"])
        upload=float(r["upload_gib"])
        upload_bw=float(r["upload_bw_gib_s"])
        tg=float(r["steady_tg_tok_s"])

        if min(model,source,upload_bw)<=0 or upload<0 or host<0 or tg<=0:
            raise SystemExit(f"invalid scenario: {name}")

        read_s=model/source
        upload_s=upload/upload_bw
        ready_s=read_s+host+upload_s

        print(name)
        print(f"  source_read_s: {read_s:.6f}")
        print(f"  host_backend_s: {host:.6f}")
        print(f"  device_upload_s: {upload_s:.6f}")
        print(f"  simple_serial_ready_s: {ready_s:.6f}")
        print(f"  steady_TG_tok_s: {tg:.6f}")
        print()

    print("Synthetic serial stage model only.")
    print("Real mmap/page faults/uploads can overlap or be lazy.")

if __name__=="__main__":
    main()

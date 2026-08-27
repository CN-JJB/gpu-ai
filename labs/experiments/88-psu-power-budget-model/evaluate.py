#!/usr/bin/env python3
import argparse,json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument("case",type=Path)
    a=p.parse_args()
    c=json.loads(a.case.read_text(encoding="utf-8"))

    reject=[]
    review=[]
    info=[]

    cap=float(c["psu"]["rated_w"])
    load=float(c["system"]["estimated_continuous_w"])
    policy=float(c["policy"]["min_headroom_fraction"])

    if cap <= 0 or load < 0:
        raise SystemExit("invalid wattage values")
    if not 0 <= policy < 1:
        raise SystemExit("policy min_headroom_fraction must be in [0,1)")

    headroom=cap-load
    frac=headroom/cap
    info.append(f"capacity={cap:g}W estimated_load={load:g}W")
    info.append(f"arithmetic_headroom={headroom:g}W ({frac*100:.3f}%)")

    if load > cap:
        reject.append("estimated continuous load exceeds PSU rated capacity")
    elif frac < policy:
        review.append(
            f"arithmetic headroom {frac*100:.3f}% below case policy {policy*100:.3f}%"
        )

    measured=c["system"].get("measured_wall_peak_w")
    if measured is None:
        info.append("whole-system wall peak UNKNOWN")
    else:
        measured=float(measured)
        info.append(f"measured wall peak={measured:g}W (different AC boundary from PSU DC rating)")

    compat=c["cables"].get("modular_compatibility")
    if compat is False:
        reject.append("modular PSU cable compatibility is known false")
    elif compat is None:
        review.append("modular PSU cable compatibility not proven")

    required=int(c["cables"]["required_gpu_power_paths"])
    available=int(c["cables"]["confirmed_compatible_paths"])
    if required < 0 or available < 0:
        raise SystemExit("connector path counts must be >=0")
    if available < required:
        reject.append(
            f"insufficient confirmed compatible GPU power paths: {available}/{required}"
        )

    if c["visual"].get("connector_heat_damage"):
        reject.append("visible connector heat/arcing damage — stop use")

    if not c["psu"].get("exact_model_known",False):
        review.append("exact PSU model/revision unknown")

    if c["system"].get("transient_compatibility_confirmed") is False:
        reject.append("exact manufacturer/spec transient compatibility known false")
    elif c["system"].get("transient_compatibility_confirmed") is None:
        info.append("transient compatibility UNKNOWN — arithmetic is not proof")

    decision="REJECT" if reject else ("REVIEW" if review else "ACCEPT")

    print(f"CASE: {c['case_id']}")
    print("INFO")
    for x in info: print("- "+x)
    print("REVIEW")
    for x in review: print("- "+x)
    print("REJECT")
    for x in reject: print("- "+x)
    print(f"DECISION: {decision}")
    print("This model checks planning gates; it is not an electrical safety certification.")


if __name__=="__main__":
    main()

#!/usr/bin/env python3
import argparse,json
from pathlib import Path

PLACEHOLDERS={"REPLACE","TODO","TBD","UNKNOWN"}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("dossier",type=Path)
    a=p.parse_args()
    c=json.loads(a.dossier.read_text(encoding="utf-8"))

    blocked=[]
    reject=[]
    review=[]
    info=[]

    for path,value in [
        ("case_id",c.get("case_id")),
        ("psu.brand",c["psu"].get("brand")),
        ("psu.model",c["psu"].get("model")),
        ("cables.compatibility_source",c["cables"].get("compatibility_source")),
    ]:
        if not isinstance(value,str) or value.strip().upper() in PLACEHOLDERS or not value.strip():
            blocked.append(f"missing evidence: {path}")

    cap=float(c["psu"]["rated_w"])
    load=float(c["system"]["estimated_continuous_w"])
    policy=float(c["policy"]["min_headroom_fraction"])

    if cap<=0:
        blocked.append("psu.rated_w must be >0")
    if load<=0:
        blocked.append("system.estimated_continuous_w must be >0")
    if not 0<=policy<1:
        blocked.append("policy.min_headroom_fraction must be in [0,1)")

    if blocked:
        print("DOSSIER: BLOCKED_MISSING_EVIDENCE")
        for x in blocked: print("- "+x)
        raise SystemExit(3)

    headroom=cap-load
    frac=headroom/cap
    info.append(f"capacity={cap:g}W estimated={load:g}W headroom={headroom:g}W ({frac*100:.3f}%)")

    if load>cap:
        reject.append("estimated continuous load exceeds rated capacity")
    elif frac<policy:
        review.append(
            f"arithmetic headroom below declared policy: {frac*100:.3f}% < {policy*100:.3f}%"
        )

    compat=c["cables"].get("modular_compatibility")
    if compat is False:
        reject.append("modular cable compatibility is known false")
    elif compat is None:
        review.append("modular cable compatibility remains unconfirmed")

    required=int(c["cables"]["required_gpu_power_paths"])
    confirmed=int(c["cables"]["confirmed_compatible_paths"])
    if confirmed<required:
        reject.append(f"confirmed compatible GPU power paths {confirmed} < required {required}")

    if c["visual"].get("connector_heat_damage"):
        reject.append("visible connector heat/arcing damage — STOP USE")

    if not c["psu"].get("exact_model_known"):
        review.append("exact PSU model/revision not confirmed")

    trans=c["system"].get("transient_compatibility_confirmed")
    if trans is False:
        reject.append("documented transient/config compatibility is known false")
    elif trans is None:
        info.append("transient compatibility remains UNKNOWN; capacity arithmetic is not proof")

    measured=c["system"].get("measured_wall_peak_w")
    if measured is None:
        info.append("wall power measurement not supplied")
    else:
        info.append(f"observed wall peak={float(measured):g}W; AC wall boundary differs from PSU DC rating")

    decision="REJECT" if reject else ("REVIEW" if review else "ACCEPT")
    print("INFO")
    for x in info: print("- "+x)
    print("REVIEW")
    for x in review: print("- "+x)
    print("REJECT")
    for x in reject: print("- "+x)
    print(f"DOSSIER: {decision}")
    print("Not an electrical/transient safety certification.")


if __name__=="__main__":
    main()

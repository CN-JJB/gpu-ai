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

    claimed=float(c["claim"]["vram_gib"])
    observed=float(c["observed"]["vram_gib"])
    if claimed <= 0 or observed <= 0:
        raise SystemExit("VRAM values must be >0")

    frac=observed/claimed
    if frac < 0.90 or frac > 1.10:
        reject.append(
            f"purchase-critical VRAM mismatch: claimed={claimed:g} GiB observed={observed:g} GiB"
        )

    if not c["observed"]["driver_recognized"]:
        reject.append("vendor driver does not recognize target GPU")
    if not c["observed"]["target_runtime_recognized"]:
        reject.append("target compute/runtime does not recognize GPU")
    if not c["workload"]["sustained_completed"]:
        reject.append("ordinary sustained target workload did not complete")

    uncorr=c["errors"].get("uncorrectable")
    if uncorr is None:
        info.append("uncorrectable-error telemetry unsupported/unknown")
    elif float(uncorr)>0:
        reject.append(f"observed uncorrectable errors: {uncorr}")

    max_width=c["pcie"].get("max_width")
    current_width=c["pcie"].get("current_width")
    expected_width=c["pcie"].get("expected_platform_width")
    under_load=bool(c["pcie"].get("observed_under_load",False))

    if max_width and expected_width and max_width < expected_width:
        review.append(
            f"reported max card/link width {max_width} below expected platform width {expected_width}; inspect platform/card identity"
        )

    if current_width and expected_width and current_width < expected_width:
        if under_load:
            review.append(
                f"under-load current PCIe width x{current_width} below expected x{expected_width}; check slot/lanes/riser/card"
            )
        else:
            review.append(
                f"idle current PCIe width x{current_width} below expected x{expected_width}; do not reject without under-load/platform check"
            )

    tg_first=float(c["workload"]["tg_first"])
    tg_last=float(c["workload"]["tg_last"])
    if tg_first <= 0 or tg_last <= 0:
        reject.append("invalid/non-positive sustained TG measurement")
    else:
        drift=(tg_last/tg_first)-1
        info.append(f"sustained TG drift: {drift*100:.3f}%")
        if drift < -0.15:
            review.append(
                f"sustained TG fell {abs(drift)*100:.1f}% — investigate thermal/power/other limiter"
            )

    if c["physical"].get("display_required") and not c["physical"].get("display_outputs_tested"):
        review.append("display output required but not tested")

    if reject:
        decision="REJECT"
    elif review:
        decision="REVIEW"
    else:
        decision="ACCEPT"

    print(f"CASE: {c['case_id']}")
    print("INFO")
    for x in info: print("- "+x)
    print("REVIEW")
    for x in review: print("- "+x)
    print("REJECT")
    for x in reject: print("- "+x)
    print(f"DECISION: {decision}")
    print("This is a teaching decision model, not a hardware certificate.")


if __name__=="__main__":
    main()

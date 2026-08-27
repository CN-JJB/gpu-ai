#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED = [
    ("candidate.exact_model",),
    ("candidate.memory_gib_usable",),
    ("candidate.asking_price",),
    ("workload.model",),
    ("workload.quant",),
    ("workload.runtime_footprint_gib",),
    ("workload.runtime",),
    ("software.support_state",),
    ("software.backend",),
]

def get(d, path):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur

def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: evaluate_candidate.py candidate.json")
    d = json.loads(Path(sys.argv[1]).read_text())

    missing = []
    for item in REQUIRED:
        key = item[0]
        if get(d, key) is None:
            missing.append(key)

    print("=== candidate dossier ===")
    print("model:", get(d, "candidate.exact_model"))
    print("asking price:", get(d, "candidate.asking_price"))
    print("workload:", get(d, "workload.model"), get(d, "workload.quant"))
    print()

    if missing:
        print("decision_status: NEEDS EVIDENCE")
        print("missing critical fields:")
        for x in missing:
            print("-", x)
        return

    usable = float(get(d, "candidate.memory_gib_usable"))
    footprint = float(get(d, "workload.runtime_footprint_gib"))
    fit = usable >= footprint

    support = get(d, "software.support_state")
    software_ok = support in {"official-current", "official-pinned"}

    price = float(get(d, "candidate.asking_price"))
    tco = get(d, "tco") or {}
    total = (
        price
        + float(tco.get("platform_extra") or 0)
        + float(tco.get("psu_cooling_extra") or 0)
        + float(tco.get("energy_estimate") or 0)
        + float(tco.get("repair_reserve") or 0)
        - float(tco.get("expected_resale") or 0)
    )

    print(f"capacity_gate: {'PASS' if fit else 'FAIL'} "
          f"(usable={usable:.2f} GiB, workload={footprint:.2f} GiB)")
    print(f"software_gate: {'PASS' if software_ok else 'FAIL/REVIEW'} ({support})")
    print(f"simple_recorded_TCO: {total:.2f}")
    print()

    weak = []
    for k, v in (get(d, "evidence") or {}).items():
        if v in {"E0", "E1", None}:
            weak.append((k, v))

    if not fit:
        status = "SKIP / CHANGE WORKLOAD"
    elif not software_ok:
        status = "NEEDS SOFTWARE DECISION"
    elif weak:
        status = "NEEDS EVIDENCE"
    else:
        status = "READY FOR SCENARIO DECISION"

    print("decision_status:", status)
    if weak:
        print("weak evidence:")
        for k, v in weak:
            print(f"- {k}: {v}")

    print()
    print("This tool does not auto-BUY. Compare PP/TG/TCO/risk under your scenario.")

if __name__ == "__main__":
    main()

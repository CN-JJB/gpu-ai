#!/usr/bin/env python3
import argparse,json
from pathlib import Path

VALID={"PASS","FAIL","UNKNOWN"}
PLACEHOLDERS={"REPLACE","TODO","TBD",""}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("dossier",type=Path)
    a=p.parse_args()
    c=json.loads(a.dossier.read_text(encoding="utf-8"))

    blocked=[]
    failed=[]
    passed=[]

    for name,g in c["gates"].items():
        status=str(g.get("status","")).upper()
        required=bool(g.get("required",False))
        source=str(g.get("source","")).strip()

        if status not in VALID:
            raise SystemExit(f"invalid status for {name}: {status}")

        if not required:
            continue

        if source.upper() in PLACEHOLDERS:
            blocked.append(f"{name}: missing evidence source")
            continue

        if status=="UNKNOWN":
            blocked.append(f"{name}: UNKNOWN ({source})")
        elif status=="FAIL":
            failed.append(f"{name}: FAIL ({source})")
        else:
            passed.append(f"{name}: PASS ({source})")

    design_id=str(c.get("design_id","")).strip()
    target_sha=str(c.get("target_sha256","")).strip()
    if design_id.upper() in PLACEHOLDERS or target_sha.upper() in PLACEHOLDERS:
        blocked.append("design/target identity incomplete")

    if blocked:
        decision="BLOCKED"
    elif failed:
        decision="REVISE"
    else:
        decision="ACCEPT"

    print("PASS")
    for x in passed: print("- "+x)
    print("FAIL")
    for x in failed: print("- "+x)
    print("BLOCKED")
    for x in blocked: print("- "+x)
    print(f"DECISION: {decision}")
    print("Preferences are intentionally excluded from feasibility decision.")


if __name__=="__main__":
    main()

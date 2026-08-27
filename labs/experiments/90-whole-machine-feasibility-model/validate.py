#!/usr/bin/env python3
import argparse,json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument("case",type=Path)
    a=p.parse_args()
    c=json.loads(a.case.read_text(encoding="utf-8"))

    fail=[]
    blocked=[]
    info=[]

    def gate(name,value,reason):
        if value is False:
            fail.append(f"{name}: {reason}")
        elif value is None:
            blocked.append(f"{name}: UNKNOWN — {reason}")
        else:
            info.append(f"{name}: PASS")

    req=float(c["model"]["required_runtime_vram_gib"])
    avail=float(c["gpu"]["runtime_available_vram_gib"])
    if req<=0 or avail<=0:
        raise SystemExit("VRAM requirements/availability must be >0")
    gate("model_vram",avail>=req,f"required={req:g} GiB available={avail:g} GiB")

    gate("runtime_backend",c["software"].get("target_backend_supported"),"exact target runtime/backend support")

    if c["gpu"].get("multi_gpu"):
        gate("multi_gpu_topology",c["gpu"].get("topology_validated"),"split/topology/P2P/lane evidence")

    ram_req=float(c["host"]["required_ram_gib"])
    ram_avail=float(c["host"]["available_ram_gib"])
    gate("host_ram",ram_avail>=ram_req,f"required={ram_req:g} GiB available={ram_avail:g} GiB")

    storage_req=float(c["storage"]["required_free_gib"])
    storage_avail=float(c["storage"]["available_free_gib"])
    gate("storage",storage_avail>=storage_req,f"required={storage_req:g} GiB available={storage_avail:g} GiB")

    gate("psu_capacity",c["psu"].get("capacity_policy_pass"),"PSU continuous/headroom policy")
    gate("psu_cables",c["psu"].get("cable_compatibility_confirmed"),"exact modular/auxiliary cable compatibility")
    gate("sustained_thermal",c["thermal"].get("sustained_target_pass"),"sustained workload/thermal target")

    if c["serving"].get("required"):
        gate("serving_slo",c["serving"].get("slo_pass"),"declared TTFT/ITL/throughput SLO")

    if c["network"].get("wider_than_loopback"):
        gate("network_controls",c["network"].get("controls_pass"),"declared auth/TLS/exposure policy")

    budget=float(c["budget"]["max_total"])
    cost=float(c["budget"]["estimated_total"])
    if budget<=0 or cost<0:
        raise SystemExit("budget values invalid")
    gate("budget",cost<=budget,f"max={budget:g} estimated={cost:g}")

    # Unknown purchase/safety evidence blocks even when other known gates fail;
    # report precedence keeps uncertainty visible before redesign/purchase.
    if blocked:
        decision="BLOCKED"
    elif fail:
        decision="REVISE"
    else:
        decision="ACCEPT"

    print(f"CASE: {c['case_id']}")
    print("PASS/INFO")
    for x in info: print("- "+x)
    print("BLOCKERS")
    for x in blocked: print("- "+x)
    print("KNOWN FAILURES")
    for x in fail: print("- "+x)
    print(f"DECISION: {decision}")
    print("No weighted score is used.")


if __name__=="__main__":
    main()

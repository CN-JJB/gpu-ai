#!/usr/bin/env python3
import argparse
import ipaddress
import json
from pathlib import Path

def scope(host):
    if host in ("localhost",):
        return "loopback"
    try:
        ip=ipaddress.ip_address(host)
    except ValueError:
        return "hostname/unknown"
    if ip.is_loopback:
        return "loopback"
    if ip.is_unspecified:
        return "wildcard-all-interfaces"
    if ip.is_private:
        return "private-address"
    return "other-address"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("config",type=Path)
    a=p.parse_args()

    c=json.loads(a.config.read_text(encoding="utf-8"))
    host=c["listen_host"]
    sc=scope(host)
    findings=[]

    def add(level,msg):
        findings.append((level,msg))

    add("INFO",f"listen scope: {sc} ({host})")

    externally_reachable=sc!="loopback"

    if externally_reachable and c.get("authentication")=="none":
        add("HIGH","non-loopback listener without authentication")

    if externally_reachable and c.get("tls_termination")=="none":
        add("REVIEW","non-loopback traffic has no declared TLS termination")

    if externally_reachable and c.get("metrics_enabled"):
        add("REVIEW","metrics enabled on broader listener scope")

    if externally_reachable and c.get("slots_enabled"):
        add("REVIEW","slots endpoint enabled on broader listener scope")

    if externally_reachable and c.get("cors_origins")=="*":
        add("INFO","wildcard CORS is not an authentication boundary")

    if c.get("tools_or_agent_enabled"):
        add("HIGH","host-action tools/agent capability enabled; trust boundary is larger")

    if c.get("prompt_logging"):
        add("PRIVACY","prompt logging enabled; inspect retention/access")

    if sc=="loopback" and c.get("authentication")=="none":
        add("INFO","no auth relies on loopback/local-host trust assumption")

    print("SERVICE EXPOSURE CHECK")
    for level,msg in findings:
        print(f"[{level}] {msg}")

    print()
    print("This is a teaching checklist, not a security certification.")
    print("It does not inspect firewall/NAT/router state.")

if __name__=="__main__":
    main()

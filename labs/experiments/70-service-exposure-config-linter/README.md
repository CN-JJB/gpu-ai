# Experiment 70 — Service Exposure Configuration Linter

硬件等级：L0

## Goal

Compare two synthetic service configurations.

## Local-only

```bash
python3 audit_config.py local-only.json
```

Expected:
- loopback scope;
- no-auth relies on local-host trust assumption;
- no external-exposure HIGH finding.

## Broad listener

```bash
python3 audit_config.py lan-risk.json
```

Expected findings include:
- wildcard/all-interface listener;
- no authentication;
- no declared TLS termination;
- metrics/slots broader exposure;
- prompt logging privacy review.

## Important

The linter does **not** inspect:
- firewall;
- router/NAT;
- VPN;
- cloud security group.

It cannot certify Internet reachability or security.

It is a checklist teaching tool.

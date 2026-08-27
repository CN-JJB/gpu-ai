# Expected — Experiment 70

## local-only.json

Expected themes:

```
[INFO] listen scope: loopback
[INFO] no auth relies on loopback/local-host trust assumption
```

No claim that loopback makes the host universally secure.

## lan-risk.json

Expected themes:

```
[INFO] wildcard/all-interface scope
[HIGH] non-loopback listener without authentication
[REVIEW] no declared TLS termination
[REVIEW] metrics broader exposure
[REVIEW] slots broader exposure
[PRIVACY] prompt logging enabled
```

The tool is not a vulnerability scanner.

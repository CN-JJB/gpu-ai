# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–38 are implemented.
Experiments 01–71 exist.

## Slice 38 core

Current pinned llama-server defaults/evidence:

```
host 127.0.0.1
port 8080
api key none
metrics disabled
slots enabled
Web UI enabled
```

Trust-boundary model:

```
loopback
→ broader interface
→ authentication
→ TLS path
→ endpoint exposure
→ logs/privacy
→ host-action tools
```

Key distinctions:

```
auth != TLS != CORS != firewall
```

The real lab:
- inventories listener sockets read-only;
- probes only localhost/loopback;
- never modifies firewall/NAT/router;
- never prints an API key or endpoint body.

## Active next slice — Operational Reliability / Recovery

Build:

```
process start
→ port/listener
→ health
→ model loaded
→ ready
→ warm request
→ serving
```

Then failure/recovery:

```
intentional local stop
→ request failure/drain behavior
→ restart
→ readiness recovery time
→ first-request cold/warm latency
```

Teach:
- liveness != readiness;
- listening port != model ready;
- crash/restart can lose warm caches;
- configuration/model SHA must survive restart;
- graceful drain is different from abrupt kill.

Real lab must only manipulate the user's own local test process and must not install system services or alter boot configuration.

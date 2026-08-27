# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–39 are implemented.
Experiments 01–73 exist.

## Slice 39 core

Pinned `llama-server /health`:

```
503 = Loading model
200 = model loaded / ready
```

Operational states:

```
process alive
→ listener/HTTP
→ readiness
→ smoke inference
→ warm steady state
```

Synthetic verified:

```
cold:
HTTP 400 ms
ready 5000 ms
first inference 5800 ms
warm 150 ms

restart:
HTTP 450 ms
ready 5100 ms
first inference 6300 ms
warm 160 ms
```

Real Experiment 73 is hardened:
- forced 127.0.0.1;
- only own child process managed;
- LLAMA_ARG_* hidden overrides stripped;
- model/network/auth/tools overrides rejected;
- model/server SHA recorded.

## Active next slice — Safe Upgrade / Rollback

Build a release gate:

```
baseline release
→ candidate identity
→ readiness
→ smoke
→ PP/TG
→ quality
→ serving SLO
→ ACCEPT or ROLLBACK
```

Define rollback triggers before candidate run.

Teach:
- runtime upgrade != model upgrade != config change;
- a new release may be faster but fail quality/SLO;
- rollback means restoring exact previous artifact/config identity, not merely restarting;
- rollback readiness must itself be verified.

Real lab should remain local, use exact artifacts, and avoid system-service installation.

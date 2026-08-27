# Evidence — Experiment 39: Operational Reliability / Readiness / Restart Recovery

状态：stable lifecycle/recovery lesson complete; L0 lifecycle arithmetic verified; real loopback restart probe hardened.

## Claim

> Process liveness, listener availability, model readiness, first successful inference and warm steady state are different operational states.

## Current pinned llama.cpp evidence

Pinned:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current server docs define:

```
GET /health
GET /v1/health
```

During model load:

```
HTTP 503
Loading model
```

When successfully loaded:

```
HTTP 200
{"status":"ok"}
```

The endpoint is documented as public/no API-key check.

Therefore the course uses `/health=200` as a model-readiness signal, not as proof of warm steady-state performance.

## Experiment 72 verification

Synthetic cold start:

```
first HTTP = 400 ms
health-ready = 5000 ms
first inference complete = 5800 ms
post-ready first inference = 800 ms
later warm request = 150 ms
```

Synthetic restart:

```
first HTTP = 450 ms
health-ready = 5100 ms
first inference complete = 6300 ms
post-ready first inference = 1200 ms
later warm request = 160 ms
```

Verified readiness delta:

```
+100 ms
```

All values are synthetic.

Core result:

```
listener
!= readiness
!= first usable inference
!= warm steady state
```

## Experiment 73 safety/identity design

The real probe:
- launches its own `llama-server` child;
- forces `127.0.0.1`;
- terminates only that child;
- installs no system service;
- changes no boot configuration.

It records:
- server binary SHA256;
- model SHA256 before/after;
- first HTTP timestamp;
- health status transitions;
- readiness timestamp;
- first one-token smoke-inference completion;
- child exit code;
- whether forced kill was required;
- raw server logs.

## Hardened configuration identity

The child environment removes:

```
LLAMA_ARG_*
LLAMA_API_KEY
```

so hidden llama-server environment overrides cannot silently change the experiment.

Extra args reject model/network/security/tool overrides including:
- `-m / --model`;
- remote/HF model source options;
- `--host / --port`;
- API-key/TLS options;
- tools/MCP/agent options.

Performance/execution options such as:
- GPU layers;
- context;
- FlashAttention;

remain allowed and are visible in the recorded command.

## Stop boundary

The default real lab stops the child only after the smoke request finishes.

It does **not** claim:
- in-flight drain behavior;
- rolling replacement;
- graceful completion of active requests.

```
process terminate
!= proven application-level drain
```

## Restart/cache boundary

Process-local state such as:
- active KV;
- in-memory prefix cache;
- some runtime warm state;

should be treated as cold after restart unless exact persistence/restore is proven.

A health-200 server can therefore still have worse first-request latency than later warm requests.

## Learner should reject

- process alive means ready;
- port open means model loaded;
- health 200 guarantees target SLO;
- sleep N seconds is a readiness check;
- same port means same model/runtime;
- restart preserves process-local KV/prefix cache;
- SIGTERM automatically means all in-flight requests drained.

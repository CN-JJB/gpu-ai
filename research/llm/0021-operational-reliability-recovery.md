# Research Note 0021 — Operational Reliability / Readiness / Restart Recovery

日期：2026-08-27

## Research question

When is a local LLM service actually usable?

These states are different:

```
process exists
→ socket/listener reachable
→ health endpoint responds
→ model loaded / ready
→ first inference succeeds
→ warm steady state
```

A reliability design must distinguish them.

---

# Current pinned llama.cpp evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

Current `llama-server` documentation defines:

```
GET /health
```

and `/v1/health`.

During model loading:

```
HTTP 503
message: Loading model
```

After successful model load:

```
HTTP 200
{"status":"ok"}
```

The endpoint is documented as public/no API-key check.

This makes it useful as a readiness signal, but also means its network exposure should be considered separately from authenticated inference endpoints.

---

# Part I — Liveness vs readiness

## Liveness

Question:

> Is the process alive/running?

A process can be alive while:
- loading a model;
- allocating GPU buffers;
- compiling/loading kernels;
- recovering from startup.

## Readiness

Question:

> Should traffic be sent here now?

For the pinned server, `/health = 200` is a useful model-loaded readiness signal.

Therefore:

```
process alive
!= ready
```

---

# Part II — Listener != ready

A server may bind its socket before the model finishes loading.

Then:

```
TCP/HTTP reachable
```

but:

```
/health = 503 Loading model
```

So a port-open check is weaker than application readiness.

---

# Part III — Readiness != successful real workload

A 200 health response confirms the runtime's documented readiness condition.

It does not prove:
- your exact prompt/template works;
- enough KV remains for your target context;
- your sampler/grammar/tool path works;
- performance meets SLO.

A minimal post-readiness smoke inference is stronger deployment evidence.

---

# Part IV — Startup timeline

Useful timestamps:

```
t_spawn
t_first_http
t_health_200
t_first_inference_done
```

Derived:

```
listener/HTTP availability
= t_first_http - t_spawn

readiness recovery
= t_health_200 - t_spawn

usable smoke recovery
= t_first_inference_done - t_spawn
```

Do not call them all "startup time".

---

# Part V — Cold vs warm state

After startup, later requests may benefit from:
- OS file cache;
- runtime allocations already initialized;
- prompt/KV cache;
- kernel/runtime warmup;
- filesystem/model pages resident.

A restart can remove process-local state.

Therefore compare:

```
first request after restart
vs
steady warm request
```

with exact workload identity.

Do not assume every difference is GPU warmup; identify cache/runtime layers where possible.

---

# Part VI — Prompt/KV cache after restart

In-memory KV/prompt cache belongs to runtime state.

An ordinary process restart should be treated as a cold in-memory cache boundary unless the exact runtime explicitly saves/restores that state.

Current llama-server has separate slot-cache save/restore capabilities, but that is not the same as automatic persistence across every restart.

So:

```
restart
→ assume warm cache lost
until proven restored
```

is the safer operational model.

---

# Part VII — Configuration identity after restart

A restart can accidentally change:
- binary/build;
- model path;
- model artifact;
- backend;
- GPU selection;
- context;
- KV type;
- FlashAttention;
- parallel slots.

A recovered server is not the same experiment merely because it answers on the same port.

Record:
- runtime binary SHA/version;
- model SHA;
- launch args/config;
- device identity.

Reuse Slice 33 manifest discipline.

---

# Part VIII — Graceful drain vs abrupt stop

## Drain

Conceptually:
1. stop admitting new work;
2. allow selected in-flight work to finish;
3. stop the process.

Goal:
- fewer interrupted requests;
- cleaner client semantics.

## Abrupt stop

Process disappears while work is in flight.

Possible results:
- connection reset;
- partial output;
- retry;
- duplicated work if caller retries elsewhere.

The exact behavior depends on runtime and gateway.

This course does not prescribe an undocumented llama-server drain endpoint.

---

# Part IX — SIGTERM/process terminate is not automatically a full drain

A process termination signal may allow cleanup, but that does not prove:
- new requests were blocked first;
- all active generations completed;
- clients received graceful completion.

Treat:

```
process terminate
```

and:

```
application-level drain
```

as different concepts.

The real lab only terminates a child process it started, while idle.

---

# Part X — Restart objective

A basic local recovery objective can define:

```
RTO-like target:
ready again within X seconds
```

and separately:

```
first smoke inference within Y seconds
```

This course uses "recovery target" rather than claiming formal disaster-recovery RTO/SLA semantics.

---

# Part XI — Failure visibility

Useful evidence after a failed start:
- process exit code;
- server stderr/stdout log;
- health transition history;
- device/runtime errors;
- model SHA/config.

Common failure classes include:
- invalid model path;
- insufficient VRAM/RAM;
- unsupported backend;
- port already in use;
- bad config.

Do not convert every startup failure into "GPU broken".

---

# Part XII — Readiness polling

A robust poller should distinguish:
- connection refused/no HTTP yet;
- HTTP 503 loading;
- HTTP 200 ready;
- process exited unexpectedly;
- overall timeout.

This produces much better diagnosis than:
```
sleep 10
then hope
```

---

# Part XIII — Health endpoint security

Pinned `/health` is public.

That can be useful for local supervisors/load balancers.

But if the service is exposed more broadly, public health response is still part of the observable surface.

Slice 38 exposure rules still apply.

---

# Part XIV — Restart and prefix cache

Slice 09 taught cross-request prefix reuse.

Operational consequence:

```
restart
→ in-memory prefix reuse may disappear
→ TTFT can regress temporarily
```

A service can be "healthy" yet temporarily colder/slower than steady state.

Therefore recovery benchmarking may need both:
- readiness;
- warmup to target performance.

---

# Part XV — Model load vs first inference

Even after the model is loaded, first inference can trigger additional one-time costs.

Do not assume:

```
health 200
=
steady-state TTFT
```

Measure both.

---

# Part XVI — Rolling replacement intuition

For more than one replica, a safe replacement pattern is conceptually:

```
start new
→ wait ready
→ smoke test
→ route traffic
→ drain old
→ stop old
```

For one local replica, there is an unavoidable service gap unless another capacity path exists.

The course does not require orchestration software.

---

# Part XVII — Real lab safety

Experiment 73:
- binds only to 127.0.0.1;
- launches its own child process;
- rejects host/port/auth/tools/agent overrides;
- terminates only that child PID;
- installs no service;
- changes no boot/startup setting.

It measures:
- listener/HTTP availability;
- health readiness;
- first smoke inference;
- graceful idle child termination;
- restart readiness;
- binary/model SHA identity.

---

# Claims to avoid

- "process alive means model ready";
- "port open means inference works";
- "health 200 guarantees target SLO";
- "SIGTERM is automatically a full request drain";
- "restart preserves prompt/KV cache";
- "same port means same model/runtime";
- "sleep N seconds is a readiness check";
- "first post-restart request represents steady-state performance".

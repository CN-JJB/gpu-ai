# Research Note 0018 — Overload, Admission Control, Retry Amplification and Backpressure

日期：2026-08-27

## Research question

When offered load exceeds sustainable service capacity, what should a local LLM service do?

Bad mental model:

```
never reject
=
best service
```

A system can avoid immediate errors by accepting every request into an ever-growing queue, while producing:
- extreme TTFT;
- timeout cascades;
- retry storms;
- high memory/queue overhead;
- poor SLO compliance.

This slice compares:
- unbounded queueing;
- bounded queue + rejection;
- immediate retry;
- exponential backoff.

---

# Part I — Offered load vs service capacity

Let:

```
λ_offer
=
incoming request rate
```

and:

```
μ
=
sustainable completion/service rate
```

If for a sustained interval:

```
λ_offer > μ
```

then backlog grows unless the system:
- sheds/rejects;
- slows arrivals;
- increases service capacity;
- reduces work per request.

Queueing cannot create compute capacity.

---

# Part II — Unbounded queue

An unbounded queue accepts all arrivals.

Advantages:
- no admission rejection;
- every request may eventually run if load later falls.

Disadvantages under sustained overload:
- queue wait grows;
- TTFT tail grows;
- client deadlines expire;
- queued work can become stale;
- memory/control-plane overhead grows.

Operationally:

```
no HTTP errors
```

can coexist with:

```
terrible user experience
```

---

# Part III — Bounded queue

A bounded queue admits only a limited number of waiting requests.

If full:

```
reject early
```

This trades:
- higher immediate reject rate

for:
- bounded queue memory;
- bounded waiting depth;
- lower admitted-request latency tail;
- faster overload signal to callers.

A rejected request is not "free", but it avoids consuming more queued waiting time.

---

# Part IV — Admission control

Admission control asks:

> Should this request enter the expensive model-serving path now?

Possible inputs:
- active slots;
- queued requests;
- current KV headroom;
- request prompt/output budget;
- tenant/user quota;
- latency SLO;
- model availability.

Simple count-only admission is useful but incomplete.

A long 64k-context request and a short 128-token request are not identical resource demands.

---

# Part V — Load shedding

Load shedding intentionally rejects/deprioritizes some work to protect:
- admitted-request latency;
- high-priority traffic;
- system stability.

Common result semantics can include:
- HTTP 429 Too Many Requests;
- HTTP 503 Service Unavailable;

depending on the service design.

The course does not prescribe one status code universally.

---

# Part VI — Immediate retries can amplify load

Suppose a request is rejected because the server is overloaded.

If client does:

```
retry after 100 ms
retry after 100 ms
retry after 100 ms
```

the retry arrives while overload still exists.

Now:

```
original offered load
+
retry attempts
```

can exceed the original traffic substantially.

This is retry amplification.

---

# Part VII — Backoff

A common client strategy:

```
delay
→ retry
→ longer delay
→ retry
```

For example:

```
0.5 s
1 s
2 s
4 s
...
```

This gives the server more time to recover.

Random jitter is often added in real distributed systems so many clients do not retry on the exact same synchronized schedule.

This L0 experiment uses deterministic backoff for reproducibility.

---

# Part VIII — Backoff is not a latency guarantee

Backoff can:
- reduce repeated failed attempts;
- improve eventual success during temporary overload.

But it can also increase:

```
time from original user request
to final completion
```

Therefore evaluate:
- attempt amplification;
- eventual success;
- user E2E;
- SLO.

Do not celebrate "all eventually completed" if users waited far beyond the service objective.

---

# Part IX — Timeout boundary

A client timeout means:

```
client stops waiting
```

It does **not automatically prove**:

```
server stopped model work
```

unless cancellation is propagated through:
- HTTP/server layer;
- scheduler;
- model execution.

If abandoned work keeps running, timeout can waste capacity and worsen overload.

Verify cancellation behavior in the exact runtime.

---

# Part X — Synthetic workload

Ten original requests:

```
arrival every 0.5 s
```

Single synthetic server:

```
service time = 1.0 s/request
capacity ≈ 1 req/s
```

Offered rate during the burst:

```
≈ 2 req/s
```

so arrival pressure exceeds service capacity.

---

# Part XI — Unbounded synthetic result

All ten enter.

Verified:

```
HTTP/attempts = 10
completed = 10
rejected attempts = 0
max queue = 5
mean wait = 2.25 s
p95 wait = 4.5 s
completion makespan = 10 s
```

No rejection, but terrible queue tail.

---

# Part XII — Bounded queue, no retry

Waiting queue limit:

```
2
```

Verified:

```
attempts = 10
completed = 7
rejected attempts = 3
dropped originals = 3
max queue = 2
mean wait among completed ≈ 1.286 s
p95 wait = 2.0 s
makespan = 7 s
```

This sacrifices availability to bound admitted-request wait.

---

# Part XIII — Immediate retry

Same queue limit:

```
2
```

Rejected clients retry:
- every 0.1 s;
- up to 3 retries.

Verified:

```
original requests = 10
HTTP attempts = 19
rejected attempts = 12
completed originals = 7
dropped originals = 3
```

Attempt amplification:

```
19 / 10
=
1.9×
```

Yet completion count did not improve over no-retry.

This is the key retry-storm teaching result.

---

# Part XIV — Exponential backoff synthetic result

Same queue limit.

Retry delays:

```
0.5 s
1.0 s
2.0 s
```

Verified:

```
attempts = 18
rejected attempts = 8
completed = 10
dropped = 0
max queue = 2
mean wait from original arrival = 2.25 s
p95 wait = 5.5 s
makespan = 10 s
```

All requests eventually complete, but tail wait remains high.

So:

```
eventual success
!=
interactive SLO success
```

---

# Part XV — Retry budget

Clients should have a finite retry budget.

Without it, a permanently unavailable service can produce unbounded retries.

A retry policy should consider:
- retryable status/error;
- attempt count;
- total deadline;
- backoff;
- jitter;
- idempotency.

For generation requests, retrying can also duplicate expensive work if the first attempt was actually running but the client lost the response.

---

# Part XVI — SLO-aware admission

An interactive service may prefer:

```
reject some requests early
```

rather than:

```
accept all
then let p95 TTFT grow without bound
```

The correct policy depends on:
- user expectations;
- request priority;
- workload burstiness;
- retry behavior;
- model capacity.

There is no universal queue length.

---

# Part XVII — KV-aware admission

A server with enough slots can still run out of KV capacity.

Admission can consider estimated:

```
current active KV
+
new request worst/expected KV
+
reserve
```

This matters with:
- long contexts;
- many concurrent sequences;
- heterogeneous request lengths.

Count-based:

```
active requests < N
```

is weaker than resource-aware admission.

---

# Part XVIII — Prompt/output budgets

A request can impose upper bounds:

```
max prompt tokens
max output tokens
max context
```

These are not only abuse controls.

They are capacity controls:
- bound per-request prefill;
- bound slot occupation duration;
- bound KV growth.

---

# Part XIX — Queue discipline

FIFO is easy to understand but not always ideal.

Alternative policies can consider:
- priority;
- age;
- estimated size;
- tenant fairness.

However shortest-job-first-like scheduling requires work-size estimates and can starve long jobs if not designed carefully.

This course does not prescribe an advanced scheduler here.

The key skill is to state the policy and measure its consequences.

---

# Part XX — Real llama-server observation

Current pinned llama-server exposes:
- `requests_processing`;
- `requests_deferred`.

These are useful overload signals.

Experiment 63 can observe client:
- TTFT;
- E2E;
- errors;

while saving server metrics before/after.

A controlled burst can therefore show whether:
- requests are deferred;
- TTFT grows;
- errors occur.

Do not run course load tests against systems you do not own/control.

---

# Part XXI — Reverse proxy / application layer

Admission can live:
- inside the inference server;
- in an application gateway;
- in a reverse proxy;
- in a client-side queue.

Each placement sees different information.

A generic reverse proxy may know:
- request count;
- connection count;

but not:
- prompt token count;
- future KV cost.

Resource-aware admission may require application/model knowledge.

---

# Part XXII — Decision table

## Interactive low-latency

Prefer:
- bounded backlog;
- explicit rejection;
- controlled retry/backoff;
- strict prompt/output budgets;
- SLO monitoring.

## Offline batch

Can tolerate:
- longer queue;
- lower urgency;
- throughput-oriented batching.

One queue policy should not be assumed optimal for both.

---

# Claims to avoid

- "never reject = reliable";
- "queueing creates capacity";
- "client timeout means server work stopped";
- "retry immediately until success";
- "backoff guarantees low latency";
- "all eventual successes means good interactive service";
- "one queue limit is correct for every workload";
- "request count alone captures KV/resource demand";
- "HTTP 429 is always the only correct overload response".

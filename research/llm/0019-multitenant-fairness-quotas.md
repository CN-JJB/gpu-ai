# Research Note 0019 — Multi-Tenant Fairness, Quotas and Resource Accounting

日期：2026-08-27

## Research question

If several people share one local LLM server, what does "fair" mean?

A request-count-only rule can be misleading.

Example:

Tenant A:
```
2 requests × 1000 output tokens
```

Tenant B:
```
2 requests × 50 output tokens
```

Both submitted two HTTP requests.

They did not ask for equal:
- slot time;
- decode work;
- KV;
- context capacity.

This slice introduces fairness as explicit resource policy.

---

# Part I — Request fairness vs resource fairness

Equal request count:

```
A: 2 requests
B: 2 requests
```

does not imply equal:
- prompt tokens;
- output tokens;
- GPU time;
- active sequence duration;
- KV allocation.

For LLM serving, request count is a weak cost proxy.

---

# Part II — Long requests occupy scarce slots

A request can remain active while generating hundreds or thousands of tokens.

If:

```
output tokens ↑
```

then roughly:

```
active duration ↑
```

for the same decode cadence.

With finite slots, long requests can keep short requests waiting.

This is not malicious behavior; it is ordinary shared-resource contention.

---

# Part III — Context length is another cost axis

Long context can increase:
- prefill work;
- KV state;
- attention-side read work;
- TTFT.

So fairness policy can consider both:

```
prompt/context budget
```

and:

```
output/generation budget
```

rather than only request count.

---

# Part IV — Per-tenant concurrency limit

A simple policy:

```
tenant active requests <= C_tenant
```

Example:

```
2 total slots
tenant A max active = 1
tenant B max active = 1
```

This prevents one tenant from occupying both slots while another is waiting.

But strict caps can leave hardware idle when only one tenant has work.

---

# Part V — Work-conserving fairness

A work-conserving policy tries to preserve fairness **when tenants compete**, but allows spare capacity to be borrowed when it would otherwise sit idle.

Conceptually:

```
if A and B both waiting:
  enforce fair share

if only A waiting:
  let A borrow unused capacity
```

This improves utilization without abandoning fairness under contention.

---

# Part VI — Synthetic two-tenant model

Two slots.

Each active slot processes:

```
10 output tokens/s
```

All requests arrive at time zero.

Tenant A:

```
A1 = 100 tokens
A2 = 100 tokens
```

Tenant B:

```
B1..B4 = 10 tokens each
```

Total work:

```
A = 200 tokens
B = 40 tokens
```

Request share:

```
A = 2/6 = 33.3%
B = 4/6 = 66.7%
```

Output-work share:

```
A = 200/240 = 83.3%
B = 40/240 = 16.7%
```

So request count and resource demand point in opposite directions.

---

# Part VII — Global FIFO result

Request order:

```
A1, A2, B1, B2, B3, B4
```

Two slots immediately start:

```
A1 + A2
```

Both run for 10 seconds.

B waits.

Verified synthetic:

```
Tenant A mean wait = 0 s
Tenant A last completion = 10 s

Tenant B mean wait = 10.5 s
Tenant B p95 wait = 11 s
Tenant B last completion = 12 s

makespan = 12 s
slot utilization = 100%
```

Maximum utilization does not imply fair latency.

---

# Part VIII — Strict per-tenant cap

Policy:

```
max 1 active request / tenant
```

Starts:

```
A1 + B1
```

B short requests run one after another.

Verified:

Tenant B:

```
mean wait = 1.5 s
p95 wait = 3 s
last completion = 4 s
```

Tenant A:

```
A2 waits for A1
mean wait = 5 s
p95 wait = 10 s
last completion = 20 s
```

Overall:

```
makespan = 20 s
slot utilization = 60%
```

Fairer short-tenant latency, poor work conservation.

---

# Part IX — Work-conserving borrow

Same fair cap while both tenants have queued work.

After B finishes all queued requests at 4 seconds:

```
no competing B work remains
```

so A2 may borrow the otherwise idle slot.

Verified:

Tenant B remains:

```
mean wait = 1.5 s
p95 wait = 3 s
last completion = 4 s
```

Tenant A improves:

```
mean wait = 2 s
p95 wait = 4 s
last completion = 14 s
```

Overall:

```
makespan = 14 s
slot utilization ≈ 85.7%
```

This demonstrates:

```
fairness
+
work conservation
```

can be better than a rigid quota.

---

# Part X — Token quotas

A policy can limit:

```
prompt tokens / time window
output tokens / time window
```

or simply:

```
max output tokens / request
```

Token accounting is more resource-aware than request count, but still imperfect.

One 1000-token prompt and one 1000-token output do not necessarily cost the same GPU time.

---

# Part XI — Compute/resource cost is multidimensional

A better cost vector may include:

```
prompt tokens
output tokens
context length
KV bytes
active duration
model selected
LoRA/adapters
tool/multimodal work
```

Do not collapse all cost into one "request unit" unless the workload is homogeneous.

---

# Part XII — KV fairness

A tenant with:
- several long contexts;
- large generation budgets;

can hold substantial KV.

Per-tenant policy can include:

```
max concurrent active sequences
max context
max aggregate estimated KV
```

This protects other tenants from capacity starvation.

---

# Part XIII — Weighted fairness

Not all tenants need equal share.

Example policy:

```
interactive user weight = 2
background batch weight = 1
```

A weighted scheduler can intentionally give interactive work more opportunities.

This is policy, not a universal truth.

Weights should be explicit and auditable.

---

# Part XIV — Priority and starvation

Strict priority:

```
always serve high priority first
```

can starve low-priority work if high-priority arrivals never stop.

Likewise, shortest-job-first-like policies can improve mean latency but starve large jobs.

Fair systems may need:
- aging;
- minimum guaranteed share;
- max starvation time.

This slice teaches the tradeoff, not one universal scheduler.

---

# Part XV — Per-tenant SLO

Overall p95 can hide one tenant suffering badly.

Record per tenant:
- request count;
- prompt/output tokens;
- TTFT;
- E2E;
- error/reject rate;
- active-slot time proxy.

Example:

```
global p95 = acceptable
Tenant B p95 = terrible
```

Global aggregate alone is insufficient.

---

# Part XVI — Fairness vs throughput

A fairness policy can reduce peak hardware utilization if implemented rigidly.

Therefore evaluate:

```
per-tenant latency
+
aggregate throughput
+
slot utilization
+
resource share
```

The goal is not "fairness at any cost".

It is an explicit tradeoff.

---

# Part XVII — Application/gateway vs inference runtime

Per-user identity/quota often lives above the raw inference runtime.

The application layer may know:
- authenticated user;
- plan/tier;
- tenant;
- daily token budget.

The model server may know:
- slot state;
- KV state;
- model scheduler.

A complete system can combine both.

Do not assume llama-server itself implements every multi-tenant quota policy described here.

---

# Part XVIII — Security/privacy boundary

Tenant identifiers in Evidence should not require publishing real personal identities.

Use:
- pseudonymous tenant IDs;
- aggregate counts;
- redacted prompts.

Fairness analysis usually needs resource/latency metadata, not private content.

---

# Part XIX — Real workload report

For every tenant record:

```
requests
successful requests
prompt tokens
requested output budget
observed output tokens
TTFT p50/p95
E2E p50/p95
errors/rejects
```

Then compare:
- request share;
- token/work share;
- latency share.

This turns "Tenant B feels slow" into evidence.

---

# Part XX — Buyer/system consequence

A slower cheap GPU increases service time.

Under shared load:
- long requests occupy slots longer;
- fairness pressure rises;
- more queue/admission complexity is needed.

A faster or higher-memory card can improve not only one-user speed but multi-user isolation.

Hardware choice and scheduling policy interact.

---

# Claims to avoid

- "equal request count means fair resource use";
- "per-tenant concurrency cap always improves utilization";
- "strict quotas are always better than borrowing";
- "token count perfectly predicts GPU cost";
- "shortest job first is universally fair";
- "global p95 proves every tenant has good latency";
- "priority has no starvation risk";
- "the inference runtime alone must implement all tenant policy".

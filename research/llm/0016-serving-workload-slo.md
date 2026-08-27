# Research Note 0016 — Serving Workload / SLO: TTFT, ITL, Tail Latency and Throughput

日期：2026-08-27

## Research question

A local LLM server is not defined by one:

```
tokens/s
```

number.

A serving workload is a distribution over:
- request arrival time;
- prompt length;
- requested/generated output length;
- concurrency;
- cache state;
- sampling/tool behavior.

The user experience then depends on several distinct metrics:

```
queue wait
→ TTFT
→ ITL / generation cadence
→ E2E latency
→ request throughput
→ token throughput
→ tail percentiles
```

This slice connects the earlier continuous-batching lesson to a reproducible serving workload.

---

# Current pinned llama.cpp source evidence

Pinned upstream:

```
ggml-org/llama.cpp
d7a2074112d27649303fa107eb8c94db1ee435f3
```

## llama-server

Current server options include:
- `--parallel`: number of server slots;
- continuous batching enabled by default;
- `--metrics`: Prometheus-compatible metrics endpoint;
- prompt caching controls.

Current `/metrics` documentation exposes counters/gauges including:
- prompt tokens/time/throughput;
- predicted tokens/time/throughput;
- requests processing;
- requests deferred;
- context high watermark;
- busy slots per decode;
- speculative-decoding counters.

Pinned tests additionally verify:
- `llamacpp:prompt_tokens_cached_total`;
- cached prompt tokens are counted separately from processed prompt tokens.

## Current server benchmark

Pinned `tools/server/bench/README.md` uses k6 and can benchmark:
- many requests;
- multiple concurrent virtual users;
- prompt/output length filters.

It explicitly notes that its simple local dataset prefilter tokenizer is only a space split, so real model token counts can differ.

This reinforces the course rule:

```
workload identity should record actual model token counts
```

when exact token distribution matters.

---

# Part I — Request timeline

For one request:

```
client sends request
t_arrival
    ↓
queue / deferred
    ↓
prompt processing
    ↓
first generated token becomes visible
t_first
    ↓
subsequent generated tokens
    ↓
request complete
t_done
```

Client-observed:

```
TTFT
=
t_first - t_arrival
```

and:

```
E2E
=
t_done - t_arrival
```

If server-side service start is known:

```
queue_wait
=
t_service_start - t_arrival
```

Then TTFT can be conceptually decomposed:

```
TTFT
≈
queue wait
+
prompt/prefill work
+
first-token delivery overhead
```

The exact boundary depends on runtime instrumentation.

---

# Part II — ITL

Inter-token latency:

```
ITL_i
=
t_token_i - t_token_(i-1)
```

for generated tokens after the first.

A request-level average:

```
mean ITL
≈
(t_done - t_first) / (N_output - 1)
```

only when:
- first/last token timing is correctly measured;
- generated-token count is known;
- completion overhead is negligible or separately handled.

For a real streaming API, SSE chunks can:
- contain multiple tokens;
- be buffered;
- include non-token events.

Therefore:

```
SSE chunk gap
!= guaranteed true token ITL
```

Call it:
```
client-visible chunk-gap proxy
```
unless token-level timing evidence proves otherwise.

---

# Part III — TTFT vs ITL answer different UX questions

## TTFT

How long does the user stare at a blank response?

Sensitive to:
- queueing;
- prompt length;
- prefix cache hit;
- prefill throughput;
- batch scheduling.

## ITL

Once output starts, how quickly does text continue?

Sensitive to:
- decode throughput;
- active batch size;
- memory bandwidth;
- speculative decoding;
- synchronization;
- serving contention.

A system can have:

```
bad TTFT
+
good ITL
```

when requests queue but active generation remains fast.

It can also have:

```
good TTFT
+
bad ITL
```

when many requests are admitted quickly but active decode cadence becomes slow.

---

# Part IV — Request throughput vs token throughput

Request throughput:

```
completed requests / second
```

Output-token throughput:

```
generated output tokens / second
```

Prompt-token throughput:

```
processed prompt tokens / second
```

These are not interchangeable.

Example:

Workload A:
- many 8-token replies.

Workload B:
- many 512-token replies.

They can have:
- similar request throughput;
- very different token throughput;

or vice versa.

Therefore every throughput number needs request-shape context.

---

# Part V — Aggregate throughput vs per-user cadence

Continuous batching can improve GPU utilization by combining active sequences.

As concurrency rises:

```
aggregate tokens/s
can rise
```

while:

```
per-request ITL
can worsen
```

because each request shares decode work/capacity with more active sequences.

This is why:

> highest total throughput

is not automatically:

> best interactive server.

---

# Part VI — Queueing

If all slots/sequence capacity are busy, new requests wait.

Current pinned server exposes:

```
llamacpp:requests_processing
llamacpp:requests_deferred
```

as aggregate gauges.

A client trace can observe the consequence as rising TTFT.

Queueing matters because:

```
arrival rate
>
sustainable service rate
```

for long enough causes backlog growth.

You do not need advanced queueing theory to recognize this operational rule.

---

# Part VII — Length distributions matter

A benchmark that uses only:

```
prompt = 512
output = 128
```

is useful but describes only that fixed point.

Real workloads may contain:

```
short prompt + short reply
short prompt + long reply
long prompt + short reply
long prompt + long reply
```

Prompt length affects:
- prefill;
- KV;
- TTFT.

Output length affects:
- how long a slot remains active;
- total decode work;
- concurrency overlap.

Long requests can therefore influence short requests sharing the same server.

---

# Part VIII — Head-of-line / mixed-workload intuition

Imagine two requests arriving close together:

A:
```
prompt 64
output 32
```

B:
```
prompt 16000
output 512
```

Depending on scheduler/batching:
- B can occupy substantial prompt/decode work;
- A can see higher TTFT or ITL;
- aggregate throughput may still look healthy.

The user cares about A's latency, not just server-average tokens/s.

---

# Part IX — Percentiles

For request latencies:

```
[...]
```

p50:
- median-ish central request.

p95:
- threshold below which roughly 95% of observations fall under the chosen estimator.

p99:
- tail threshold near the slowest 1%.

Important:

```
percentile estimator matters
```

especially for small sample sizes.

This course's L0 analyzer uses the simple **nearest-rank** estimator:

```
rank = ceil(p × N)
```

after sorting.

Real monitoring tools can use different histogram/interpolation algorithms.

Record the method.

---

# Part X — Mean can hide a terrible tail

Synthetic TTFT:

```
100,105,110,115,120,125,
130,135,140,145,150,1200 ms
```

Mean:

```
≈ 214.6 ms
```

This sounds comfortably below a hypothetical:

```
TTFT target = 500 ms
```

But nearest-rank p95:

```
1200 ms
```

because one request is severely queued.

If the SLO requires 99% of requests <=500 ms, this workload fails.

Average alone hides that.

---

# Part XI — SLI, SLO and SLA

Useful operational distinction:

## SLI
Measured indicator.

Example:
```
client TTFT
```

## SLO
Internal target.

Example:
```
99% of requests TTFT <= 500 ms
```

## SLA
External contractual commitment, possibly with consequences.

This course focuses on SLI/SLO engineering.

Do not casually call every target an SLA.

---

# Part XII — Example SLO dimensions

Interactive chat might care about:

```
TTFT p95 <= target
ITL p95 <= target
error rate <= target
```

Batch generation might care more about:

```
aggregate output tok/s
job completion time
```

Different workload goals imply different optimal concurrency.

---

# Part XIII — SLO compliance

Given per-request requirement:

```
TTFT <= 500 ms
AND
mean ITL <= 80 ms
```

request compliance:

```
pass if both are true
```

Then:

```
SLO compliance
=
passing requests / total requests
```

If target:

```
99%
```

and measured:

```
91.7%
```

the SLO fails even if average TTFT is excellent.

---

# Part XIV — Throughput-optimal concurrency

Suppose:
- 1 slot underutilizes GPU;
- 4 active sequences improve batching;
- 16 active sequences improve aggregate tokens/s only slightly but double ITL.

For an interactive SLO:

```
concurrency=16
```

may be the wrong configuration even if it wins a throughput chart.

Choose:

```
highest throughput
subject to latency/quality constraints
```

not raw maximum throughput.

---

# Part XV — Cache state is workload identity

Prefix cache can strongly change TTFT.

A benchmark must say whether requests are:
- cold;
- warm repeated prefix;
- mixed;
- cache disabled;
- cache eviction pressure.

Pinned server metrics can distinguish processed prompt tokens and cached prompt tokens.

Therefore:

```
same prompt distribution
+
different cache state
```

is not the same serving workload.

---

# Part XVI — Real client trace vs server metrics

Client trace tells you:
- arrival;
- first visible output;
- completion;
- HTTP error;
- client chunk cadence.

Server metrics tell you:
- processed/cached prompt totals;
- predicted token totals;
- processing/deferred requests;
- slot occupancy proxy;
- aggregate prompt/decode rates.

Use both.

Neither alone tells the whole story.

---

# Part XVII — Network boundary

Client-observed TTFT includes:
- client/server network;
- HTTP handling;
- queue;
- model work;
- streaming delivery.

On localhost, network is small but not literally zero.

For remote serving, network variability can dominate tails.

Therefore label:

```
client-observed TTFT
```

rather than pretending it is pure GPU prefill time.

---

# Part XVIII — Workload Manifest extension

A serving workload should freeze:

```
request trace SHA
arrival schedule/distribution
prompt token counts
requested output lengths
cache policy/state
parallel slots
continuous batching
context
sampler
client location/path
```

Also record percentile estimator.

This extends Slice 33.

---

# Part XIX — Benchmark trace vs production trace

Synthetic traces are good for controlled questions.

Production-derived traces are good for realism.

If using production logs:
- remove/redact sensitive content;
- preserve length/arrival distributions if that is the experiment need;
- do not publish private prompts.

A distribution-only workload can often be reproduced without keeping user text.

---

# Part XX — Optimization decision

For serving, an optimization result should look like:

```
throughput +12%
TTFT p95 +3%
ITL p95 +4%
quality unchanged
→ likely acceptable
```

or:

```
throughput +18%
TTFT p95 +180%
SLO compliance 99.2% → 83%
→ reject for interactive workload
```

There is no universal answer without the workload goal.

---

# Claims to avoid

- "tokens/s is enough to describe a server";
- "TTFT is just prompt-eval time";
- "SSE chunk gap is always ITL";
- "request throughput and token throughput are interchangeable";
- "mean latency describes tail latency";
- "p95 is defined identically by every tool";
- "maximum aggregate throughput is always the best concurrency";
- "same requests with cold/warm prefix cache are the same workload";
- "server metrics alone provide client-observed latency".

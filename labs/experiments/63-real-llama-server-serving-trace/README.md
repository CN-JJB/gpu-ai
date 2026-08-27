# Experiment 63 — Real llama-server Serving Workload Trace

硬件等级：L1/L2/L3，取决于 server/model。

## Goal

Capture client-observed serving latency together with pinned/current server metrics.

Evidence:

```
workload identity
→ client request trace
→ /metrics before/after
→ analyzer
→ SLO report
```

No real performance data ships with the course.

## 1. Start server

Example only:

```bash
llama-server \
  -m MODEL.gguf \
  --metrics \
  --parallel 4
```

Confirm current:
```bash
llama-server --help
```

before running.

Continuous batching is enabled by default in the pinned snapshot, but record the actual setting.

## 2. Build exact prompts

Prefer Experiment 57.

For this lab, each JSONL workload item points at an exact already-rendered prompt file.

Example:
```json
{"id":"r0","delay_ms":0,"prompt_file":"prompts/p0.txt","n_predict":64}
```

Using exact rendered files avoids silently changing chat-template serialization inside the load generator.

## 3. Run collector

```bash
python3 client_trace.py \
  workload.jsonl \
  --server http://127.0.0.1:8080 \
  --out-dir evidence
```

The collector:
- schedules requests by `delay_ms`;
- sends streaming `/completion` requests;
- requests returned token IDs;
- records first token-bearing SSE chunk;
- records completion;
- records prompt SHA256;
- saves raw SSE per request;
- snapshots `/metrics` before/after when available.

## 4. Important ITL caveat

The client can timestamp SSE chunks.

But:

```
SSE chunk gap
!= guaranteed true token ITL
```

A chunk can contain:
- multiple token IDs;
- buffering effects;
- non-token events.

Therefore the collector reports:
```
client chunk-gap proxy
```

not "true ITL".

If a runtime exposes validated per-token timings, record them separately.

## 5. Analyze

Convert/inspect:
`requests.csv`

The real collector does not know exact server service-start time, so it cannot isolate queue wait from client timing.

Use:
- client TTFT;
- E2E;
- chunk-gap proxy;
- server `requests_deferred`/processing evidence;
- prompt/predicted counters.

Do not fabricate a queue_ms column.

## 6. Workload identity

Record:
- workload.jsonl SHA;
- every prompt SHA/token count;
- model/runtime manifest;
- slots;
- continuous batching;
- cache state;
- context;
- request arrival schedule;
- requested output lengths;
- client/server location;
- percentile method.

Pair with Experiment 61.

## 7. Current pinned /metrics

The pinned server exposes aggregate:
- prompt tokens/time/rate;
- predicted tokens/time/rate;
- processing/deferred requests;
- context high watermark;
- busy slots per decode;
- speculative metrics.

Pinned tests also verify:
`prompt_tokens_cached_total`.

Save raw metrics text rather than copying one dashboard screenshot.

## 8. Finish

Use:
`RESULT-TEMPLATE.md`.

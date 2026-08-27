# Experiment 67 — Controlled Local Overload Observation

硬件等级：L1/L2/L3。

## Safety / scope

Run only against:
- your own local server;
- a private test server you are authorized to load-test.

The workload generator hard-caps this course lab at 64 requests.

This is not a public-service load-testing recipe.

## Goal

Observe what your actual serving stack does when a short finite burst exceeds immediate slot capacity.

Measure:
- client TTFT/E2E;
- HTTP errors;
- server `requests_deferred`;
- processing requests;
- prompt/predicted token deltas.

## 1. Start with a healthy low-load baseline

Use Experiment 63.

Record:
- server slots;
- continuous batching;
- model;
- context;
- cache state.

## 2. Build a bounded burst

Reuse an exact prompt artifact.

Example:

```bash
python3 make_burst.py \
  --prompt-file ../63-real-llama-server-serving-trace/prompts/p0.txt \
  --requests 8 \
  --spacing-ms 50 \
  --n-predict 64
```

## 3. Capture

Reuse Experiment 63 collector:

```bash
python3 ../63-real-llama-server-serving-trace/client_trace.py \
  workload-burst.jsonl \
  --server http://127.0.0.1:8080 \
  --out-dir evidence-burst
```

## 4. Observe default behavior

Do not assume the server rejects.

The pinned llama-server exposes:
- processing requests;
- deferred requests.

Your exact runtime may queue/defer requests rather than return overload status.

Record what actually happens.

## 5. Admission layer experiment

If your application/reverse proxy supports a bounded queue or concurrency limit, compare:

```
default queueing
vs
bounded admission
```

as a **system comparison** unless only one semantic layer/config is changed and the manifest validator can prove it.

Do not prescribe one proxy product.

## 6. Retry experiment

Do not enable uncontrolled infinite retries.

If testing client retry:
- finite attempt count;
- finite total deadline;
- record every attempt;
- use backoff;
- preferably jitter in a real multi-client system.

## 7. Cancellation

If client deadlines/timeouts are used, verify whether abandoned generation actually stops on the server.

Do not infer cancellation merely because the client disconnected.

## 8. Result

Fill:
`RESULT-TEMPLATE.md`.

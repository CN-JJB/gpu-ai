# Experiment 65 — Real Serving Capacity from Request Trace

硬件等级：L1/L2/L3，复用 Experiment 63。

## Goal

Turn a real request trace into:
- completed throughput λ;
- average client time in system W;
- average client in-flight count L;
- peak client in-flight count.

If server-side/service-start timestamps are available, additionally derive:
- queue occupancy;
- active occupancy;
- active-KV planning proxy.

## Run on Experiment 63 output

```bash
python3 capacity_from_trace.py \
  ../63-real-llama-server-serving-trace/evidence/requests.csv
```

Experiment 63 currently records client send/completion but not exact server service-start.

Therefore the expected real output is:

```
L_system available
L_active UNKNOWN
queue UNKNOWN
```

Do not infer service start from first token time.

## If you enrich the CSV

If trusted instrumentation adds:

```
service_start_ms
```

the script will derive active/queue occupancy.

Optional:

```bash
--kv-gib-per-active 1.5
```

is only accepted meaningfully when active intervals exist.

This remains a constant-KV planning proxy.

## Interpretation

### L_system

Includes everything between:
- client send;
- completion.

It may contain:
- network;
- HTTP;
- deferred queue;
- active model service.

### L_active

Requires a trustworthy service-start boundary.

This is closer to slot/active-sequence occupancy.

### Peak

Always report alongside mean.

## Stability warning

A finite completed batch gives an exact area identity.

That does not prove the captured request pattern is representative or sustainable.

Compare multiple workload windows and check whether deferred/backlog state grows.

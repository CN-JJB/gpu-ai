# Overload / Admission Control Card

## Capacity condition

Sustained:

```
offered load > service capacity
```

means backlog grows unless load is:
- rejected;
- delayed upstream;
- reduced;
- or capacity increases.

## Queue choices

### Unbounded
- fewer immediate rejects
- potentially unbounded TTFT tail

### Bounded
- explicit rejection
- bounded queue depth
- protects admitted latency

## Retry

Immediate retry:

```
rejection
→ retry quickly
→ more offered attempts
→ overload amplification
```

Use finite:
- retry budget;
- total deadline;
- backoff;
- jitter when appropriate.

## Timeout

```
client timeout
!= guaranteed server cancellation
```

Verify exact runtime.

## Admission inputs

- active slots
- queue depth
- KV headroom
- prompt tokens
- output budget
- priority/quota
- SLO state

## Serving signals

- client TTFT/E2E/error rate
- server processing requests
- server deferred requests
- active KV/headroom

## Decision goal

```
protect SLO
+
avoid retry amplification
+
preserve useful throughput
```

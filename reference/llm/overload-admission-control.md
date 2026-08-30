# Overload / Admission Control Card

<figure>
  <img src="../../assets/diagrams/overload-retry.svg" alt="Overload / Admission Control Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Overload / Admission Control Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


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

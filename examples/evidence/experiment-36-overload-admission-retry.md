# Evidence — Experiment 36: Overload / Admission Control / Retry

状态：stable overload lesson complete; L0 queue/retry model verified; bounded real observation lab ready.

## Claim

> Under sustained offered load above service capacity, accepting everything into an unbounded queue can destroy tail latency. Immediate client retries can amplify load without improving successful original requests.

## Stable model

```
offered load > sustainable service capacity
```

implies backlog growth unless load is:
- shed/rejected;
- reduced;
- delayed upstream;
- or capacity increases.

Queueing does not create compute capacity.

## Experiment 66 verification

Synthetic:
```
10 original requests
arrival every 0.5 s
single service path
1.0 s service/request
```

### Unbounded

Verified:

```
attempts = 10
rejected attempts = 0
completed = 10
dropped = 0
max queue = 5
mean wait = 2.25 s
p95 wait = 4.5 s
makespan = 10 s
```

No immediate error, but a large wait tail.

### Bounded queue / no retry

Queue limit:

```
2 waiting
```

Verified:

```
attempts = 10
reject attempts = 3
completed = 7
dropped = 3
max queue = 2
mean wait ≈ 1.285714 s
p95 wait = 2.0 s
makespan = 7 s
```

### Immediate retry

Rejected requests retry every:

```
0.1 s
```

up to three retries.

Verified:

```
10 originals
19 attempts
12 rejected attempts
7 completed
3 dropped
```

Attempt amplification:

```
1.9×
```

Completion count is unchanged from bounded/no-retry.

### Exponential backoff

Deterministic delays:

```
0.5 s
1.0 s
2.0 s
```

Verified:

```
18 attempts
8 rejected attempts
10 completed
0 dropped
p95 wait = 5.5 s
makespan = 10 s
```

So eventual success improves, while interactive tail wait remains poor.

## Important boundaries

```
eventual success
!=
interactive SLO success
```

and:

```
client timeout
!=
proof server generation was cancelled
```

unless cancellation propagation is verified in the exact system.

## KV/resource-aware admission

Request count is not enough.

A stronger admission decision may consider:
- active slots;
- queued requests;
- KV headroom;
- prompt tokens;
- output budget;
- request priority;
- SLO.

## Experiment 67

The real lab:
- is explicitly restricted to systems the learner owns/controls;
- hard-caps the course workload generator at 64 requests;
- reuses Experiment 63 client/server metrics;
- records actual deferred/error behavior instead of assuming rejection semantics.

## Learner should reject

- never reject means reliable;
- queueing creates service capacity;
- immediate retry always improves reliability;
- backoff guarantees low latency;
- all eventual successes mean good interactive service;
- client timeout proves GPU work stopped;
- request count alone captures serving resource demand.

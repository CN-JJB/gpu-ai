# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–37 are implemented.
Experiments 01–69 exist.

## Slice 37 core

Synthetic shared server:

```
2 slots
A: 2 × 100-token jobs
B: 4 × 10-token jobs
```

Request share:
```
A 33%
B 67%
```

Output-work share:
```
A 83%
B 17%
```

Results:

```
FIFO:
B mean wait 10.5 s
util 100%

strict one-active/tenant:
B mean wait 1.5 s
util 60%

work-conserving borrowing:
B mean wait 1.5 s
util 85.714%
```

Lesson:
```
fair under contention
+
borrow idle capacity
```

can preserve fairness without rigidly wasting GPU.

## Active next slice — Service Exposure / Privacy / Auth

Teach safe deployment boundaries:

```
localhost
vs
LAN bind
vs
public exposure
```

Inventory:
- listen address/port;
- authentication;
- TLS termination;
- reverse-proxy/app gateway;
- server metrics endpoint;
- slots/cache endpoints;
- prompt/request logs;
- model files/licenses.

Real lab must be read-only:
- inspect listening sockets/process args/config;
- do not modify firewall/router/NAT;
- do not expose a service publicly as part of the course.

Focus on least exposure and evidence.

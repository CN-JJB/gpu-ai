# Handoff — GPU × Local LLM Course

## Repository

- Repo: CN-JJB/gpu-ai
- Branch: main

## Completed frontier

Slices 01–35 are implemented.
Experiments 01–65 exist.

## Slice 35

Serving capacity relation:

```
L = λW
```

but boundaries matter:

```
L_system = queued + active
L_active = active service
L_queue = deferred/waiting
```

Verified synthetic:

```
λ = 1.2 req/s

L_system 3.0, peak 5
L_active 2.7, peak 4
L_queue  0.3, peak 1
```

Constant active-KV teaching proxy:
```
1.5 GiB/sequence
average 4.05 GiB
peak 6.0 GiB
```

Do not size slots from ceil(L_system).
Do not derive active KV from client E2E trace without service-start evidence.

## Active next slice — Overload / Admission Control

Build a synthetic queue experiment with service capacity below offered load.

Compare:

```
unbounded queue
vs
bounded queue + reject
vs
bounded queue + immediate retries
vs
backoff
```

Teach:
- backlog can trade reject rate for disastrous TTFT;
- immediate retries can amplify offered load;
- rejecting early can preserve latency for admitted requests;
- client timeout does not automatically cancel server work unless the system propagates cancellation;
- admission must consider slots/KV/SLO, not only HTTP request count.

Then add a real llama-server/reverse-proxy observation packet without prescribing one proxy product.

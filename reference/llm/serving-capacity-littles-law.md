# Serving Capacity / Little's Law Card

## Core relation

```
L = λ W
```

Define the boundary.

## End-to-end system

```
W_system = completion - arrival
L_system = average queued + active
```

## Queue

```
W_queue = service_start - arrival
L_queue = λ W_queue
```

## Active service

```
W_active = completion - service_start
L_active = λ W_active
```

Then:

```
W_system = W_queue + W_active
L_system = L_queue + L_active
```

## Do not confuse

```
average L
!= peak concurrency
!= required slot count
```

## KV

A rough constant-state teaching proxy:

```
average active KV
≈
L_active × KV_per_active_sequence
```

But real per-request KV depends on current sequence length and cache architecture.

## Overload warning

Representative stable window:

```
arrivals ≈ completions
```

Persistent:

```
arrivals > completions
```

means backlog grows.

Do not use a stale W to "solve" an overloaded system.

## Little's Law cannot give

- p95/p99;
- burst peak;
- optimal slots;
- SLO miss probability.

Use trace/SLO evidence.

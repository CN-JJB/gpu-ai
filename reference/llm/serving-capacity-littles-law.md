# Serving Capacity / Little's Law Card

<figure>
  <img src="../../assets/diagrams/serving-capacity-littles-law.svg" alt="Serving Capacity / Little's Law Card 的教学视觉索引：先建立关键结构、流程与约束关系，再使用本页表格、公式和 checklist。">
  <figcaption>视觉索引：先用图建立 Serving Capacity / Little's Law Card 的核心关系，再把下面的表格、公式与检查项作为快速查阅层。</figcaption>
</figure>


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

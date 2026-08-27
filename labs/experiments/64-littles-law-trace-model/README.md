# Experiment 64 — Little's Law Trace Identity

硬件等级：L0

## Goal

Verify three consistent boundaries:

```
L_system = λ W_system
L_active = λ W_active
L_queue  = λ W_queue
```

and:

```
L_system
=
L_active + L_queue
```

## Run

```bash
python3 little.py trace-synthetic.csv
```

## Expected teaching result

```
lambda = 1.2 req/s

L_system = 3.0
L_active = 2.7
L_queue  = 0.3
```

But peaks:

```
system peak = 5
active peak = 4
queue peak  = 1
```

So average occupancy is not peak capacity.

## KV proxy

Default:

```
1.5 GiB / active sequence
```

gives:

```
average active KV proxy = 4.05 GiB
peak active KV proxy = 6.0 GiB
```

Synthetic only.

Real KV depends on current sequence/cache state.

# Expected — Experiment 50

Default expert accounting:

```
one expert weights:
176,160,768

one expert storage:
94.5000 MiB

all routed experts/layer:
756.0000 MiB

selected top-k storage/layer:
189.0000 MiB

all routed experts across 32 layers:
23.6250 GiB

top-k no-reuse proxy across 32 layers/token:
5.9062 GiB
```

Balanced routing:

```
[4,4,4,4,4,4,4,4]
unique experts = 8
expert max/avg = 1.0x
per-device assignments = [8,8,8,8]
device max/avg = 1.0x
ideal expert weight bytes/token/layer
= 47.25 MiB
```

Skewed:

```
[16,16,0,0,0,0,0,0]
unique experts = 2
expert max/avg = 4.0x
per-device assignments = [32,0,0,0]
device max/avg = 4.0x
ideal expert weight bytes/token/layer
= 11.8125 MiB
```

The skewed pattern has a lower idealized weight-byte proxy but much worse expert-parallel utilization.

That tradeoff is the lesson.

# Expected — Experiment 66

## Unbounded

```
attempts = 10
reject attempts = 0
completed = 10
dropped = 0
max queue = 5
mean wait = 2.25 s
p95 wait = 4.5 s
makespan = 10 s
attempt amplification = 1.0x
```

## Bounded, no retry

```
attempts = 10
reject attempts = 3
completed = 7
dropped = 3
max queue = 2
mean wait ≈ 1.285714 s
p95 wait = 2.0 s
makespan = 7 s
attempt amplification = 1.0x
```

## Bounded, immediate retry

```
attempts = 19
reject attempts = 12
completed = 7
dropped = 3
max queue = 2
mean wait ≈ 1.285714 s
p95 wait = 2.0 s
makespan = 7 s
attempt amplification = 1.9x
```

No additional original request completes.

## Bounded, exponential backoff

```
attempts = 18
reject attempts = 8
completed = 10
dropped = 0
max queue = 2
mean wait = 2.25 s
p95 wait = 5.5 s
makespan = 10 s
attempt amplification = 1.8x
```

All complete eventually, but interactive tail wait is poor.

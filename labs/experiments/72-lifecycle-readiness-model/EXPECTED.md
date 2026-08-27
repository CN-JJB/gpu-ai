# Expected — Experiment 72

```
cold-start
first HTTP = 400 ms after spawn
readiness = 5000 ms
first inference complete = 5800 ms
post-ready first inference = 800 ms
warm request = 150 ms

restart
first HTTP = 450 ms
readiness = 5100 ms
first inference complete = 6300 ms
post-ready first inference = 1200 ms
warm request = 160 ms

readiness delta = +100 ms
```

Synthetic only.

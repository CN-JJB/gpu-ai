# Expected — Experiment 36

There is no universal PASS result.

A correct packet contains:
- before-payment seller evidence;
- serial/identity;
- baseline log;
- a memory-integrity result;
- workload-relevant PP/TG evidence;
- thermals/error review;
- final decision.

## Important non-results

These are insufficient alone:

```
"GPU-Z opened"
"FurMark passed"
"3DMark score normal"
"seller has many reviews"
"验货宝 passed"
```

Any can be useful evidence, but none covers the entire acceptance model.

## Safe default

`collect-baseline.sh` is read-only/best-effort.

It does not:
- overclock;
- change power limits;
- flash BIOS;
- change firmware;
- run an automatic maximum-power stress test.

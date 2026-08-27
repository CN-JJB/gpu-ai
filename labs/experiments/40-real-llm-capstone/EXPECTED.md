# Expected — Experiment 40

There are no universal benchmark numbers.

A valid completed capstone has:

```
profile.txt
baseline-manifest.json
baseline.json
candidate-manifest.json
candidate.json
validator output
comparison output
CAPSTONE-CARD
```

## Validator

For a clean A/B:

```
IDENTITY CHECK: PASS
ONE-VARIABLE CHECK: PASS
PLACEHOLDER CHECK: PASS
```

If model SHA, runtime, device, PP/TG or repeats differ, identity check must fail.

If two config fields differ, one-variable check must fail.

## Benchmark result

Both are valid:

```
candidate faster
```

or:

```
candidate slower / same
```

provided:
- workload identity is controlled;
- raw data exists;
- conclusion matches the evidence.

## No fabricated examples

This experiment intentionally ships without PP/TG result files.

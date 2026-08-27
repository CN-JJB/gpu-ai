# Spec 0005 — Comparable Benchmark View

Status: implemented foundation  
Date: 2026-08-27

## Problem

A benchmark catalog makes it easy to make a bad leaderboard:

~~~text
GPU A = 100 tok/s
GPU B = 70 tok/s
→ A is faster
~~~

if the two rows used different:
- model artifacts;
- quant;
- context;
- PP/TG protocol;
- prompt identity;
- sequence count;
- execution settings.

I04 adds a descriptive comparable-workload view.

## Comparison key

v1 comparison groups require the same:

~~~text
model_id
+ artifact SHA
+ quant
+ workload object
~~~

The workload object includes the recorded benchmark protocol and execution identity.

Hardware/runtime are intentionally not part of the group key because the purpose is to observe system differences under the same model/workload.

## Interpretation

Rows in one group are:

~~~text
OBSERVATIONAL SYSTEM COMPARISON
~~~

not automatically a causal A/B.

For causal claims use the Experiment 60/61 semantic A/B discipline.

## Output

For every group:
- comparison fingerprint;
- model/artifact identity;
- workload identity;
- observation count;
- hardware;
- runtime/backend/build;
- PP/TG;
- evidence packet reference.

Optional sorting by PP or TG is descriptive performance ordering only.

It is not a recommendation ranking.

## No cross-group ranking

The tool must never sort observations from different comparison fingerprints into one performance table.

If groups differ, they remain separate.

## Synthetic fixture

The fixture includes two synthetic GPUs running the same synthetic artifact/workload.

Their fake TG values exist only to prove grouping behavior.

## Production behavior

The production benchmark catalog is initially empty.

Therefore the production comparable view should report no benchmark observations until real Evidence is ingested.

## Future price/performance

A later price/performance view may combine:
- one comparable benchmark group;
- explicitly selected market observations with matching cohort/geography/state.

It must not silently use the latest random asking price.

## Non-goals

This view does not:
- declare universal fastest GPU;
- compare unlike model artifacts;
- infer quality equivalence;
- infer purchase value;
- turn observational system comparisons into causal claims.
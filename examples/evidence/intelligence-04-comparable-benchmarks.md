# Evidence — Intelligence I04: Comparable Benchmark View

Status: same-artifact/workload descriptive grouping implemented.

## Claim

Benchmark observations should not enter one leaderboard unless their model artifact and workload identity are comparable.

## Comparison fingerprint

The view groups by:

~~~text
model_id
+ artifact SHA
+ quant
+ workload object
~~~

Hardware/runtime remain visible as compared system dimensions.

## Output semantics

Rows within one fingerprint are labeled:

~~~text
OBSERVATIONAL_SYSTEM_COMPARISON
~~~

They are not automatically causal A/B results.

For causal claims, use Experiment 60/61 semantic A/B rules.

## Synthetic proof

Two synthetic hardware fixtures use the same:
- model;
- artifact;
- quant;
- workload;
- runtime entity.

Synthetic TG:

~~~text
50 tok/s
40 tok/s
~~~

The tool places them in one group with:

~~~text
observations=2
comparison_status=DESCRIPTIVE_ONLY
~~~

These values prove grouping behavior only.

## Guardrail

The tool prints:

~~~text
No cross-group ranking is performed.
~~~

A sorted metric inside one group is not a purchase recommendation.
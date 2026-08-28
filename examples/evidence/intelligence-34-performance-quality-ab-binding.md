# Intelligence I34 — performance × quality A/B binding

Date: 2026-08-28

## Added

~~~text
tools/intelligence/experiment61_ab_contract.py
tools/intelligence/bind_performance_quality_ab.py
tools/intelligence/joint_tradeoff_selftest.py
docs/specs/0035-intelligence-performance-quality-ab-binding.md
~~~

## Positive contract

A model-artifact Experiment 61 A/B may emit descriptive PP/TG/PPL deltas only when:
- the one-variable manifest contract passes;
- both benchmark records exactly bind to their manifests;
- I33 fixed quality identity binds to both manifests;
- I33 baseline/candidate model SHA + bytes bind to the same manifest pair.

## Negative cases

The dedicated self-test blocks:
- mismatched quality candidate model SHA;
- benchmark workload drift;
- undeclared manifest differences;
- execution-variable quality attribution under the current I33 exact-evaluation contract.

## Synthetic-only boundary

All self-test PP/TG/PPL values are arithmetic fixtures only.

They are not real GPU performance, model quality, or recommendation evidence.

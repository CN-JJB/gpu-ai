# Intelligence I46 — explicit performance target policy

Date: 2026-08-28

## Added

~~~text
tools/intelligence/evaluate_performance_target.py
tools/intelligence/verify_performance_target.py
tools/intelligence/performance_target_selftest.py
labs/experiments/38-real-candidate-watchlist/performance-target-policy.template.json
docs/specs/0047-intelligence-performance-target-policy.md
~~~

## Behavior

The policy uses hard thresholds only:
- minimum candidate PP;
- minimum candidate TG;
- optional maximum candidate PPL;
- optional maximum PPL percent change.

I42 is rerun before evaluation.

## Negative cases

The self-test blocks:
- edited FAIL → PASS artifacts;
- comparison_id mismatch.

Synthetic fixtures remain explicitly labeled.

# Intelligence I48 — explicit price-ceiling policy

Date: 2026-08-28

## Added

~~~text
tools/intelligence/evaluate_price_ceiling.py
tools/intelligence/verify_price_ceiling.py
tools/intelligence/price_ceiling_selftest.py
labs/experiments/38-real-candidate-watchlist/price-ceiling-policy.template.json
docs/specs/0049-intelligence-price-ceiling-policy.md
~~~

## Neutral outputs

~~~text
WITHIN-CEILING
WATCH-BAND
ABOVE-BAND
~~~

No output is named BUY.

## Fail-closed behavior

The selected market observation must be current, grade-consistent and Experiment 38 eligible.

Currency must match exactly; no FX is invented.

Tampered result artifacts are blocked by independent reconstruction.

# Spec 0050 — Intelligence price-ceiling readiness bridge

Status: implemented in I49.

## Problem

I48 creates a reproducible neutral price-band result.

I43 must bind it to the same market observation already used by the market-evidence component.

Otherwise a caller could use one record for market-grade eligibility and a different cheaper record for the ceiling check.

## Bridge inputs

I43 adds:

~~~text
--price-ceiling-result
--price-ceiling-policy
~~~

Both are required together.

## Independent verification

I43 rebuilds the I48 artifact from:
- the current market catalog;
- explicit personal price policy;
- the same as-of date.

Synthetic evidence may be reconstructed for testing but remains production BLOCKED.

## Same-record invariant

The I48 result must satisfy:

~~~text
price_result.market_record_id
==
I43 --market-record-id
~~~

No split-record market/price admission is allowed.

## Readiness rule

The `price_ceiling` component passes only when:
- the I48 artifact independently reproduces;
- `synthetic_input=false`;
- the market record is exactly the I43 selected record;
- `decision=WITHIN-CEILING`.

`WATCH-BAND` and `ABOVE-BAND` remain blockers.

Even `WITHIN-CEILING` is not BUY.

## Trust boundary

I49 proves only that the selected current market observation is inside the learner's explicit sticker-price ceiling.

It cannot override missing condition, performance, compatibility, feasibility or other decision evidence.

# Spec 0048 — Intelligence performance-target readiness bridge

Status: implemented in I47.

## Problem

I46 makes an explicit no-weight performance/PPL threshold policy reproducible.

I43 should use that evidence rather than keeping the performance target permanently hardcoded as missing.

## Bridge inputs

I43 adds:

~~~text
--performance-target-result
--performance-target-policy
~~~

Both are required together.

## Independent verification

I43 calls the I46 verifier, which rebuilds the result from:
- the explicit policy;
- I42 verified tradeoff route;
- manifests;
- benchmark records;
- quality comparison and sealed quality evidence.

The supplied result is never trusted directly.

## Production rules

The `performance_target` component passes only when:
- the I46 artifact independently reproduces;
- `decision=PASS`;
- `synthetic_input=false`.

A synthetic PASS remains BLOCKED as production decision evidence.

A real FAIL remains BLOCKED.

## No policy invention

I47 does not choose thresholds.

It only consumes the learner's explicit I46 policy.

## Trust boundary

A passing component means the real verified candidate metrics meet the declared hard thresholds.

It still does not mean BUY and does not override market, condition, feasibility or price-policy blockers.

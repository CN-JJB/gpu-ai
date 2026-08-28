# Spec 0018 — Freshness-Aware Watchlist Market Gate

Status: implemented  
Date: 2026-08-28

## Problem

Before I17, two separate mechanisms existed:

```text
I10 freshness report
Experiment 38 watchlist evaluator
```

but freshness was not a hard purchase-decision gate.

Experiment 38 could print:

```text
BUY-CANDIDATE
stale=YES
```

because status was calculated before staleness.

That violates the stable course rule:

```text
refresh stale price evidence before paying
```

## I17 rule

A market observation must pass both:

```text
evidence-grade gate
+
freshness gate
```

before it can satisfy Experiment 38's market-evidence component.

## Evidence-grade gate

Unchanged from I16:

```text
M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
M2/M3 → grade-eligible
```

## Freshness states

```text
CURRENT
DUE-TODAY
STALE
UNSCHEDULED
INVALID
```

Watchlist mapping:

```text
CURRENT + M2/M3
→ ELIGIBLE

CURRENT + M0/M1
→ NEEDS-STRONGER-MARKET-EVIDENCE

DUE-TODAY
→ REVALIDATE-NOW

STALE
→ STALE-REVALIDATE

UNSCHEDULED / INVALID
→ REVALIDATION-SCHEDULE-REQUIRED
```

Freshness takes precedence over market grade for purchase use.

## Production catalog contract

Every non-synthetic market observation now requires:

```text
revalidate_after
```

The validator rejects a real market row without it.

Current OfferUp SOLD-marked rows receive:

```text
revalidate_after = 2026-09-04
```

which is a 7-day horizon from the 2026-08-28 capture.

## Experiment 38 correction

The real watchlist evaluator now evaluates freshness before BUY-CANDIDATE.

Decision precedence:

```text
hard FAIL
→ SKIP

hard UNKNOWN
→ NEEDS EVIDENCE

DUE-TODAY / STALE / UNKNOWN / INVALID freshness
→ NEEDS EVIDENCE

market/condition evidence insufficient
→ NEEDS EVIDENCE

then
→ BUY-CANDIDATE / WATCH / OVERPRICED
```

## Deterministic evaluation

Experiment 38 now accepts:

```bash
--as-of ISO-DATETIME
```

for reproducible tests and evidence review.

## revalidate_after fallback

If a watchlist CSV supplies `revalidate_after`, it is authoritative.

For older CSVs without it, the evaluator retains the previous fallback:

```text
observed_at age > 7 days
→ STALE
```

This keeps backward compatibility while moving new workflows to explicit expiration.

## Self-test cases

Synthetic watchlist rows verify:

```text
CURRENT + M2 + C3 + all hard PASS + under ceiling
→ BUY-CANDIDATE

DUE-TODAY with otherwise identical evidence
→ NEEDS EVIDENCE

STALE with otherwise identical evidence
→ NEEDS EVIDENCE

invalid revalidate_after
→ NEEDS EVIDENCE
```

A catalog row with missing `revalidate_after` must also fail validation.

## Non-goals

Freshness does not prove:
- the refreshed price will move;
- an old observation became false;
- a current observation is representative;
- a current M3 observation is a confirmed sale;
- a current candidate should be purchased.

It only prevents expired evidence from silently remaining purchase-eligible.

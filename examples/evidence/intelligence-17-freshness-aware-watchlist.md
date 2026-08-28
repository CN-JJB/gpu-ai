# Evidence — Intelligence I17: Freshness-Aware Watchlist Gate

Date: 2026-08-28  
Status: CI verified

## Defect

Before I17, Experiment 38 calculated BUY-CANDIDATE before evaluating price freshness.

Therefore a row could display:

~~~text
BUY-CANDIDATE
stale=YES
~~~

That contradicted the stable rule to refresh stale market evidence before paying.

## Fix

I17 adds two independent gates:

~~~text
market evidence grade
+
freshness
~~~

Current mapping:

~~~text
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
~~~

## Production contract

Every non-synthetic market observation now requires:

~~~text
revalidate_after
~~~

Nine OfferUp SOLD-marked rows were assigned:

~~~text
2026-09-04
~~~

as their current 7-day revalidation boundary.

## Experiment 38

The evaluator now blocks:

~~~text
DUE-TODAY
STALE
UNKNOWN
INVALID
~~~

from BUY-CANDIDATE.

It also supports:

~~~bash
--as-of ISO-DATETIME
~~~

for deterministic review.

## Regression cases

The self-test constructs four otherwise purchase-eligible rows:

~~~text
CURRENT → BUY-CANDIDATE
DUE-TODAY → NEEDS EVIDENCE
STALE → NEEDS EVIDENCE
INVALID → NEEDS EVIDENCE
~~~

A production market row with missing revalidate_after is also rejected.

## CI verification

GitHub Actions:

~~~text
workflow: Intelligence Self-Test
run number: 54
run id: 33137613634
head sha: bbf624e44579cbc765974bf8b5070330002f294e
job id: 98741045301
conclusion: success
~~~

Job steps:
- Checkout → success
- Set up Python → success
- Compile intelligence tools → success
- Run intelligence self-test → success

Log:

~~~text
SELFTEST: PASS
- market evidence eligibility is freshness-aware and all real market rows require revalidation dates
- Experiment 38 blocks due-today, stale and invalid market evidence from BUY-CANDIDATE
~~~

## Stable rule

~~~text
strong but expired evidence
!=
purchase-eligible evidence
~~~

Freshness does not say the old observation is false.

It says it must be refreshed before purchase use.

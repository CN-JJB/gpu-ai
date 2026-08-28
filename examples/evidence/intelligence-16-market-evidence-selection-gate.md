# Evidence — Intelligence I16: Market Evidence Selection Gate

Date: 2026-08-28  
Status: implemented; exact-main contract verified

## Claim

The dynamic Intelligence market catalog now reuses the stable Slice 19 / Experiment 38 M0–M3 grading system instead of inventing a second confidence vocabulary.

## Current production grades

```text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
```

Production count:

```text
M0 = 0
M1 = 2
M2 = 3
M3 = 9
total = 14
```

## Experiment 38 bridge

Current Experiment 38 accepts:

```text
market evidence M2/M3
```

as one prerequisite for BUY-CANDIDATE.

I16 therefore returns:

```text
M0/M1 → NEEDS-STRONGER-MARKET-EVIDENCE
M2/M3 → ELIGIBLE
```

Current production:

```text
eligible market observations = 12
needs stronger evidence = 2
```

ELIGIBLE only satisfies the market-evidence component.

## Claim-scoped M3

All nine current M3 observations are direct OfferUp pages marked SOLD with displayed listing prices.

Every one still has:

```text
transaction_amount_proven=NO
confirmed_transaction_price=false
```

Therefore:

```text
M3
!=
confirmed transaction amount
```

## Validator

Production market rows now require:
- valid M0/M1/M2/M3 grade;
- non-empty market_evidence_scope;
- current state/grade consistency.

Invalid examples rejected:

```text
MEDIAN_ASK + M3
SECONDARY_REPORTED + M2/M3
SOLD_MARKED_LISTING_PRICE + M1/M2
missing claim scope
```

## Exact-main verification

```text
market.jsonl
2686636ff2bcd18b278bd06bc36974ef882922b6

market_evidence_gate.py
88078e8bcab6a31c26a4c8a7a426713a2350eecb

validate_catalog.py
0e3d2b7913636bce0c2075120a26e778f476bf78

selftest.py
3f0dae9c5a183cf9110e9f099bc69e19a9e02518
```

Verified:
- production observations = 14;
- M1=2 / M2=3 / M3=9;
- every grade matches its current evidence state;
- every claim scope is present;
- 12 market-evidence eligible / 2 need stronger evidence;
- zero confirmed transaction amounts;
- validator guardrails present;
- self-test assertions present.

## Full Python boundary

I01–I10 retain the recorded full Python SELFTEST PASS.

I11–I16 are exact-main contract verified; a fresh complete Python rerun remains pending because the available local execution path cannot currently reconstruct the GitHub repository over the blocked network path.

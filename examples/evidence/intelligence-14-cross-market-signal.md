# Evidence — Intelligence I14: Cross-Market Signal Comparison

Date: 2026-08-28  
Status: implemented; exact-blob contract verified

## Claim

Two different market evidence states can be compared descriptively without being collapsed into one fair-value number.

## Left contract

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

## Right contract

```text
US
offerup-sold-marked-listing
used-consumer
used
SOLD_MARKED_LISTING_PRICE
USD
```

## Current signal

```text
RTX 3090
left  = 1499
right = 950
right vs left = -36.6%

RX 7900 XTX
left  = 1020
right = 700
right vs left = -31.4%

Arc A770 16GB
left  = 330
right = 200
right vs left = -39.4%
```

## Exact-blob verification

```text
market.jsonl
77715e5d3d78a7a756df671c081f3bc5eb8147bd

compare_market_contracts.py
a593b838446667de9537548660cb720805156c60

selftest.py
1e55c9505ac1fdb65b1b96b801dc32d64c2d058f
```

Contract verification confirmed:
- left rows = 3;
- right rows = 9;
- common hardware = 3;
- medians and percentages above;
- same-currency guardrail exists;
- CROSS-CONTRACT-DESCRIPTIVE label exists;
- self-test assertions exist.

## Interpretation boundary

```text
cross-contract signal gap
!=
confirmed transaction discount
!=
fair-value discount
```

Possible causes include:
- geography;
- channel;
- negotiation;
- condition/variant mix;
- timing;
- sample selection;
- user population.

## Why this matters

A price/performance tool that silently uses an active ask may produce a very different answer from one using a sold-marked listing signal.

Therefore the exact market observation must be part of the decision Evidence.
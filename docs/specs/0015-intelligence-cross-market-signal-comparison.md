# Spec 0015 — Cross-Market Signal Comparison

Status: implemented  
Date: 2026-08-28

## Problem

The repository now has two real market evidence states:

```text
active filtered eBay median asks
```

and:

```text
OfferUp listing pages marked SOLD
with displayed listing prices
```

It is useful to see how far apart those signals are, but dangerous to call the difference a transaction discount.

## Explicit contracts

Left example:

```text
GLOBAL-EBAY
secondary-aggregated-ebay-active
used-consumer
used
MEDIAN_ASK
USD
```

Right example:

```text
US
offerup-sold-marked-listing
used-consumer
used
SOLD_MARKED_LISTING_PRICE
USD
```

The tool requires both contracts explicitly.

It never auto-selects "latest market price."

## Comparison

For each hardware ID present in both contracts:

```text
median(left prices)
median(right displayed prices)
gap
right_vs_left_pct
```

The output labels itself:

```text
CROSS-CONTRACT-DESCRIPTIVE
```

## Current signal

Current data gives:

```text
RTX 3090
eBay active median ask = 1499
OfferUp sold-marked displayed median = 950
right vs left ≈ -36.6%

RX 7900 XTX
1020 vs 700
≈ -31.4%

Arc A770 16GB
330 vs 200
≈ -39.4%
```

## Interpretation boundary

These gaps may reflect:
- different channels;
- different geographies;
- negotiation behavior;
- listing selection;
- sample size;
- timing;
- card variants/condition;
- platform-specific user mix.

Therefore:

```text
cross-contract gap
!=
confirmed sale discount
!=
fair-value discount
```

## Currency gate

The tool refuses to compare contracts with different currencies.

It performs no FX conversion.

## Non-goals

This view is not:
- a fair-value model;
- a purchase recommendation;
- a seller-quality score;
- a confirmed transaction database;
- a substitute for local-market sampling.

Its purpose is to make market-state mismatch visible before price/performance or TCO analysis.

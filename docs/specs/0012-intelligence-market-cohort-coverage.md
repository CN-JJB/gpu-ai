# Spec 0012 — Explicit Market Cohort Coverage

Status: implemented  
Date: 2026-08-28

## Goal

Add stronger market-data coverage without confusing:
- asking price;
- sold price;
- geography;
- channel;
- condition;
- evidence class.

## Same-cohort production seed

I11 adds three current secondary observations from one methodology:

```text
geography   = GLOBAL-EBAY
channel     = secondary-aggregated-ebay-active
cohort      = used-consumer
condition   = used
price_state = MEDIAN_ASK
currency    = USD
```

Hardware:
- NVIDIA GeForce RTX 3090 24GB;
- AMD Radeon RX 7900 XTX 24GB;
- Intel Arc A770 16GB.

## Source semantics

The source tracks filtered active eBay listings and explicitly states that its going rates are asking prices, not sale prices.

Therefore the catalog uses:

```text
evidence_class = SECONDARY
price_state    = MEDIAN_ASK
```

It does not create SOLD-CONFIRMED records.

## Seed values

Dated source snapshots:

```text
RTX 3090      1499 USD  observed 2026-08-26
RX 7900 XTX   1020 USD  observed 2026-08-27
Arc A770 16G   330 USD  observed 2026-08-25
```

These are dynamic asking-price observations, not timeless fair values.

## Revalidation

A 7-day revalidation horizon is used for this volatile market seed:
- A770 → 2026-09-01;
- RTX 3090 → 2026-09-02;
- RX 7900 XTX → 2026-09-03.

I10 will surface them when due or stale.

## Query

```bash
python3 tools/intelligence/market_matrix.py intelligence/catalog \
  --geography GLOBAL-EBAY \
  --channel secondary-aggregated-ebay-active \
  --cohort used-consumer \
  --condition used \
  --price-state MEDIAN_ASK \
  --currency USD \
  --as-of 2026-08-28
```

## Guardrail

The market matrix groups by the full market contract.

It does not:
- sort by a universal value score;
- call asks confirmed sales;
- mix China secondary signals with global eBay asks;
- combine dealer quotes with peer-to-peer data;
- make a purchase recommendation.

## Next

Price/performance may use these rows only when real comparable benchmark Evidence exists for the same hardware and the caller explicitly selects the records.

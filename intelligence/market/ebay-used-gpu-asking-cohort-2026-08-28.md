# eBay Used-GPU Asking Cohort Snapshot — 2026-08-28

Purpose: preserve the dated source evidence behind I11/I12 market observations.

## Contract

All three rows use the same market contract:

```text
geography   = GLOBAL-EBAY
channel     = secondary-aggregated-ebay-active
cohort      = used-consumer
condition   = used
price_state = MEDIAN_ASK
currency    = USD
evidence    = SECONDARY
```

These are filtered live **asking prices**, not confirmed sales.

## NVIDIA GeForce RTX 3090 24GB

Source:
- https://rigprice.com/gpu/rtx-3090/

Snapshot:
- observed: 2026-08-26;
- median ask: 1499 USD;
- active used listings: 47;
- middle-half asking range: 1400–1520 USD;
- source export time: 2026-08-26 07:28:52 UTC.

The source explicitly says asking prices are not sale prices.

## AMD Radeon RX 7900 XTX 24GB

Source:
- https://rigprice.com/gpu/rx-7900-xtx/

Snapshot:
- observed: 2026-08-27;
- median ask: 1020 USD;
- active used listings: 23;
- middle-half asking range: 997–1080 USD;
- source export time: 2026-08-27 07:27:44 UTC.

## Intel Arc A770 16GB

Source:
- https://rigprice.com/gpu/arc-a770-16gb/

Snapshot:
- observed: 2026-08-25;
- median ask: 330 USD;
- active used listings: 8;
- middle-half asking range: 325–347 USD;
- source export time: 2026-08-25 19:29:43 UTC.

The small active sample is intentionally visible in the machine-readable observation.

## Source methodology boundary

The source describes its going rate as a median of filtered live eBay asking prices.

It excludes auctions, degraded cards and outliers according to its methodology.

It also reports delisted listings that it assumes sold, but eBay does not expose confirmed sale prices through this source.

Therefore this repository does **not** convert delisted assumptions into confirmed-sale observations.

## Catalog mapping

Production records:

```text
market:ebay-global:rtx3090:median-ask:2026-08-26
market:ebay-global:rx7900xtx:median-ask:2026-08-27
market:ebay-global:arc-a770-16g:median-ask:2026-08-25
```

Each record preserves:
- active_listings;
- range_low/range_high;
- range_kind;
- methodology;
- confirmed_sale=false;
- source export timestamp;
- revalidation date.

## Non-claims

This snapshot does not prove:
- fair purchase value;
- confirmed transaction prices;
- China-market equivalence;
- future price;
- hardware condition;
- performance;
- price/performance;
- TCO.

Use I10 to revalidate after the dated freshness boundary.
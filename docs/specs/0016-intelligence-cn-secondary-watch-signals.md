# Spec 0016 — China Secondary Watch Signals

Status: implemented  
Date: 2026-08-28

## Goal

Preserve current China used-GPU market reports without pretending that a secondary article is:
- a direct Xianyu listing sample;
- a confirmed sale;
- a normalized sold-price median.

## Contract

~~~text
geography   = CN
channel     = secondary-summary
cohort      = used-consumer
condition   = working-unverified
price_state = SECONDARY_REPORTED
currency    = CNY
~~~

## Current rows

~~~text
RTX 3090 24GB
7400 CNY
observed 2026-08-22

Arc A770 16GB
1450 CNY
observed 2026-08-21
~~~

## Required report semantics

SECONDARY_REPORTED must preserve:

~~~json
{
  "report": {
    "reported_market": "...",
    "direct_listing_capture": false,
    "confirmed_sale": false
  }
}
~~~

If a record claims direct listing capture or confirmed sale under this state, catalog validation must fail.

## A770 source context

A recent Chinese article reports that A770 16GB used prices on Xianyu were around 1150 CNY and then broadly rose to about 1450 CNY.

The catalog stores only the current reported 1450 CNY signal.

It does not infer:
- a transaction median;
- exact sample size;
- card condition distribution;
- seller quality;
- a buy target.

## Freshness

The A770 report is assigned:

~~~text
revalidate_after = 2026-08-28
~~~

so I10 marks it due on the current checkpoint date.

## Query

~~~bash
python3 tools/intelligence/market_matrix.py intelligence/catalog \
  --geography CN \
  --channel secondary-summary \
  --cohort used-consumer \
  --condition working-unverified \
  --price-state SECONDARY_REPORTED \
  --currency CNY \
  --as-of 2026-08-28
~~~

## Non-goals

This is a watch signal, not:
- direct marketplace scraping;
- confirmed-sale data;
- a cross-GPU value ranking;
- a purchase recommendation.

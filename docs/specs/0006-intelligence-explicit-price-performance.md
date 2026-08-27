# Spec 0006 — Explicit Price / Performance View

Status: implemented foundation  
Date: 2026-08-27

## Problem

Once benchmark and market observations exist, it is tempting to compute:

~~~text
tok/s / price
~~~

by joining:
- an arbitrary benchmark;
- the latest visible price.

That can silently mix:
- different workloads;
- asking vs sold prices;
- merchant vs peer-to-peer channels;
- working vs broken cards;
- different geography/currency;
- stale market data.

## Rule 1 — benchmark group first

Price/performance is only allowed inside one I04 comparable benchmark group:

~~~text
same model_id
+ same artifact SHA
+ same quant
+ same workload
~~~

No cross-group price/performance ranking.

## Rule 2 — explicit market selection

The tool never auto-selects a market observation.

The caller must pass exact market record IDs.

This makes the price evidence part of the comparison contract.

## Rule 3 — market contract must match

Selected market rows must use the same:

~~~text
geography
channel
cohort
condition
price_state
currency
~~~

If not, the comparison fails.

Example:

~~~text
merchant quote
!=
peer-to-peer confirmed sale
~~~

even when both are CNY.

## Derived metric

v1 may derive:

~~~text
TG tok/s per 1000 currency units
PP tok/s per 1000 currency units
~~~

only after both contracts pass.

This is a descriptive acquisition-price metric.

It is not TCO.

## Freshness

The output prints each market observation date and revalidation date.

A future production ranking should refuse or clearly flag stale market rows before a purchase decision.

## Synthetic fixture

Two synthetic hardware observations use:
- the same fake benchmark workload;
- the same fake market cohort;
- explicit fake prices.

The derived result proves tool behavior only.

## Non-goals

This view does not include:
- electricity;
- PSU/platform upgrade cost;
- repair risk;
- warranty;
- downtime;
- resale;
- software support cost;
- quality/SLO value.

Those belong to TCO/recommendation layers after feasibility.

## Next

I06 should add an explicit TCO worksheet that composes:
- purchase observation;
- platform delta;
- energy/duty cycle;
- risk reserve;
- horizon;
without hiding hard compatibility gates.
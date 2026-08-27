# Spec 0014 — Sold-Marked Listing Evidence

Status: implemented  
Date: 2026-08-28

## Problem

Active asking prices are useful, but a buyer also wants evidence closer to completed transactions.

Some peer-to-peer marketplace pages remain accessible after being marked:

```text
SOLD
```

while still showing the listing price.

That is stronger evidence of listing closure than an active ask, but it still does **not** prove the negotiated transaction amount.

## Price state

Use:

```text
SOLD_MARKED_LISTING_PRICE
```

not:

```text
CONFIRMED_SALE
```

## Required listing evidence

Each production row must preserve:

```json
{
  "listing": {
    "status": "SOLD",
    "title": "...",
    "location": "...",
    "displayed_price": 850,
    "confirmed_transaction_price": false
  }
}
```

The displayed price must equal the market observation price.

## Current cohort

Contract:

```text
geography   = US
channel     = offerup-sold-marked-listing
cohort      = used-consumer
condition   = used
price_state = SOLD_MARKED_LISTING_PRICE
currency    = USD
```

Three sold-marked listing pages are captured for each:

- RTX 3090 24GB;
- RX 7900 XTX 24GB;
- Arc A770 16GB.

## Descriptive displayed-price summary

Current sample:

```text
RTX 3090
850 / 950 / 1050
median displayed = 950 USD

RX 7900 XTX
580 / 700 / 800
median displayed = 700 USD

Arc A770 16GB
150 / 200 / 250
median displayed = 200 USD
```

These are not confirmed transaction medians.

## Why not treat the displayed price as sale price?

Peer-to-peer marketplaces may allow:
- negotiation;
- off-platform payment;
- bundled transactions;
- listing closure without an exposed final amount.

The page's SOLD state establishes only that the listing is marked sold/closed by the platform.

## Query

```bash
python3 tools/intelligence/sold_marked_market.py intelligence/catalog
```

## Validator

Production SOLD_MARKED_LISTING_PRICE requires:
- listing.status = SOLD;
- listing.displayed_price = price.value;
- confirmed_transaction_price = false;
- source URL.

A record claiming confirmed_transaction_price=true under this price state must fail validation.

## Non-goals

This cohort is not:
- a China-market proxy;
- a confirmed-sale database;
- a fair-value score;
- a purchase recommendation.

It is a separate evidence state between active asking listings and a truly verified transaction record.

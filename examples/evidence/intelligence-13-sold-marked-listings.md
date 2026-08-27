# Evidence — Intelligence I13: Sold-Marked Listing Evidence

Date: 2026-08-28  
Status: implemented; exact-blob contract verified

## Claim

A marketplace page marked SOLD can be represented without falsely claiming the displayed price is the actual transaction amount.

## Production state

```text
price_state = SOLD_MARKED_LISTING_PRICE
listing.status = SOLD
listing.confirmed_transaction_price = false
```

## Current cohort

Nine used OfferUp pages:

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

## Exact-blob verification

Latest main blobs:

```text
market.jsonl
77715e5d3d78a7a756df671c081f3bc5eb8147bd

sold_marked_market.py
0f367055e391e326b33a392f6e36eb1463d5eed6

validate_catalog.py
c5a087317489ce42963bbeee450965e8e656f8a0

selftest.py
b71732c66197229b1c634afe0f300a0d999c86e6
```

Contract verification confirmed:
- observations = 9;
- hardware groups = 3;
- each group has n=3;
- medians = 950 / 700 / 200 USD;
- every page status is SOLD;
- every record has confirmed_transaction_price=false;
- every displayed price matches price.value;
- all records are used-condition entries;
- validator rejection path exists;
- self-test assertions exist.

## Validator gate

SOLD_MARKED_LISTING_PRICE requires:
- listing object;
- status=SOLD;
- positive displayed price;
- displayed price equals market price;
- title/location;
- confirmed_transaction_price=false.

A record that flips the confirmation flag to true must fail validation.

## Boundary

```text
SOLD page label
!=
confirmed transaction price
```

The median produced by the tool is a descriptive median of displayed sold-marked listing prices, not a confirmed-sale median.

## Source snapshot

See:
- intelligence/market/offerup-sold-marked-gpu-listings-2026-08-28.md
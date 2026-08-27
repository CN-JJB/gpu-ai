# Evidence — Intelligence I15: China Secondary Watch

Date: 2026-08-28  
Status: implemented; exact-blob contract verified

## Production contract

~~~text
CN
secondary-summary
used-consumer
working-unverified
SECONDARY_REPORTED
CNY
~~~

## Current records

~~~text
RTX 3090  → 7400 CNY
Arc A770  → 1450 CNY
~~~

## Exact-blob verification

~~~text
market.jsonl
196383675b3e3c03467afe2699af7c46cc389a57

validate_catalog.py
3ffee24bbd1cd94c1ffaad312811d2210206769c

selftest.py
0bc3d54891f0814c1506dafb214f707ac33ed117
~~~

Verified:
- observations = 2;
- one exact market contract;
- values = 7400 / 1450 CNY;
- direct_listing_capture=false on both;
- confirmed_sale=false on both;
- validator guardrail present;
- malformed confirmed-sale self-test assertion present.

## Boundary

~~~text
SECONDARY_REPORTED
!=
direct listing sample
!=
confirmed sale
~~~

## Freshness

The A770 observation is due for revalidation on 2026-08-28.

This is intentional: a fast-moving local market signal should not silently persist as current truth.

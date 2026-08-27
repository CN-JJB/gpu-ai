# Evidence — Intelligence I05: Explicit Price / Performance

Status: explicit market-observation pairing implemented.

## Claim

Price/performance may only be derived after:
1. one comparable benchmark group is selected;
2. exact market observation records are explicitly named;
3. market cohort/state/currency contracts match.

## Guardrail

The tool does not auto-select a latest price.

~~~text
explicit market record IDs
→ required
~~~

## Market contract

Selected rows must match:

~~~text
geography
channel
cohort
condition
price_state
currency
~~~

A merchant quote cannot silently enter the same comparison as a peer-to-peer sold price.

## Derived metric

v1 can show PP/TG per 1000 currency units inside one benchmark group.

It explicitly prints:

~~~text
This is not TCO and not a purchase recommendation.
~~~

## Synthetic proof

Synthetic fixture:
- 24 GiB synthetic GPU: TG 50, price 2000 CNY;
- 16 GiB synthetic GPU: TG 40, price 1200 CNY.

Derived fixture-only TG per 1000 CNY:
- 25.000;
- 33.333.

These numbers are fake and prove arithmetic/contract behavior only.
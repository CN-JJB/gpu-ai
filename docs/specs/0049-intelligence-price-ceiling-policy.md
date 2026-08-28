# Spec 0049 — Intelligence explicit price-ceiling policy

Status: implemented in I48.

## Problem

Experiment 38 requires a personal maximum sticker price and optional watch band.

The Intelligence lane must not infer that ceiling from market averages or price/performance.

## Policy

I48 adds:

~~~json
{
  "price_ceiling_policy_schema_version": 1,
  "policy_id": "...",
  "market_record_id": "...",
  "hardware_id": "...",
  "max_sticker": {
    "currency": "CNY",
    "value": 7000
  },
  "watch_band_pct": 10
}
~~~

The ceiling is an explicit learner policy.

## Market contract

The selected record must:
- exist exactly once;
- match hardware_id;
- carry the expected M-grade for its price_state;
- be current on the supplied date;
- satisfy the existing Experiment 38 market component;
- use exactly the same currency as the policy.

I48 does not infer FX conversions.

## Neutral price bands

The existing Experiment 38 arithmetic is preserved but renamed to avoid an automatic purchase conclusion:

~~~text
market price <= max sticker
→ WITHIN-CEILING

market price <= max sticker * (1 + watch_band_pct/100)
→ WATCH-BAND

otherwise
→ ABOVE-BAND
~~~

`WITHIN-CEILING` is explicitly not BUY.

## Reproducible artifact

The result records:
- policy SHA;
- market catalog SHA;
- selected market identity/grade/freshness;
- price and currency;
- ceiling and watch limit;
- neutral decision;
- synthetic_input.

An independent verifier rebuilds the object.

## Synthetic boundary

Synthetic market fixtures require explicit `--allow-synthetic` and remain labeled.

A later readiness bridge must reject them as production evidence.

## Trust boundary

I48 only applies the learner's explicit price policy to one selected current market observation.

It does not infer fair value, rank hardware, convert currencies or recommend a purchase.

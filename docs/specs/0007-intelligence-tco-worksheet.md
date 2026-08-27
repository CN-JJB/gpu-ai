# Spec 0007 — Evidence-Linked TCO Worksheet

Status: implemented foundation  
Date: 2026-08-27

## Problem

Sticker price is not total ownership cost.

For Local-LLM hardware, a cheap accelerator can require:
- a platform upgrade;
- a larger PSU;
- more cooling;
- more electricity;
- more maintenance/risk reserve.

A TCO tool must keep these assumptions visible rather than hiding them inside one magic score.

## Input

The TCO worksheet uses:
- one explicitly selected market observation;
- a scenario JSON file.

The scenario declares:
- horizon months;
- average system power;
- hours/day;
- electricity rate;
- platform delta;
- risk reserve;
- resale estimate;
- evidence/source note for each material assumption.

## Formula

v1:

~~~text
energy_kwh
=
average_system_power_w / 1000
× hours_per_day
× 365
× horizon_months / 12

electricity_cost
=
energy_kwh × electricity_rate

tco
=
purchase_price
+ platform_delta
+ electricity_cost
+ risk_reserve
- resale_estimate
~~~

## Scope

This is a scenario calculation.

It does not claim that:
- average system power is guaranteed;
- future electricity price is known;
- resale value will occur;
- repair reserve is statistically calibrated.

Those assumptions remain visible inputs.

## Evidence rule

Every material scenario input must include an evidence/source string.

Synthetic fixture assumptions are allowed only in fixture mode.

Production TCO should link:
- measured energy evidence where available;
- exact market observation;
- actual platform quotes/cost;
- declared risk policy.

## No automatic recommendation

A lower TCO does not rescue:
- insufficient VRAM;
- unsupported runtime;
- unsafe PSU path;
- failed quality/SLO.

Feasibility/support gates still run first.

## Synthetic fixture

The fixture is intentionally fake and exists to verify arithmetic and provenance checks.

## Next

A future recommendation view may compare feasible candidates using:
- compatibility gate;
- benchmark group;
- quality/SLO;
- explicit TCO scenarios.

No weighted score may average away a hard failure.
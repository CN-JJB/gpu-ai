# Evidence — Intelligence I06: Evidence-Linked TCO Worksheet

Status: scenario TCO calculator implemented.

## Claim

TCO must expose its assumptions rather than hiding them inside a recommendation score.

## Formula

~~~text
TCO
=
purchase
+ platform delta
+ electricity
+ risk reserve
- resale estimate
~~~

Energy is derived from:
- average system power;
- hours/day;
- horizon.

## Evidence rule

The case must preserve an evidence/source string for:
- average system power;
- electricity rate;
- platform delta;
- risk reserve;
- resale estimate.

Purchase price comes from an explicitly selected market observation.

## Synthetic proof

Fixture assumptions:
- purchase = 2000 CNY;
- platform = 300;
- average system power = 300 W;
- 4 h/day;
- 12 months;
- electricity = 1 CNY/kWh;
- risk reserve = 200;
- resale estimate = 1000.

Derived:

~~~text
energy = 438.000 kWh
TCO = 1938.00 CNY
~~~

All values are synthetic.

## Guardrail

The tool states that TCO is:
- scenario output;
- not a feasibility gate;
- not a purchase recommendation.

A lower TCO cannot rescue a failed compatibility, capacity or safety gate.
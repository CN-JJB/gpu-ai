# Learning / Build Record — 2026-08-27 Intelligence TCO Worksheet

## Frontier

Phase 4 Intelligence Stations — I06.

## Implemented

Spec:
- docs/specs/0007-intelligence-tco-worksheet.md

Tool:
- tools/intelligence/tco_worksheet.py

Fixture:
- tools/intelligence/fixtures/tco-case.json

Self-test verifies:
- 438.000 kWh fixture energy;
- 1938.00 CNY fixture TCO;
- explicit evidence strings.

## Stable rule

~~~text
TCO scenario
!=
feasibility
!=
recommendation
~~~

Hard gates remain first.
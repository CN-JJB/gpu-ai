# Experiment 92 — Graduation Design Review Validator

硬件等级：L0

## Goal

Verify that a final machine-design conclusion is consistent with:
- the required hard gates;
- material-claim evidence completeness;
- revision coverage;
- explicit non-claims.

This experiment does not recommend or purchase hardware.

## Run

~~~bash
python3 validate.py case-accept.json
python3 validate.py case-revise.json
python3 validate.py case-blocked.json
~~~

## Case A — ACCEPT

Expected:
- all required gates PASS;
- every material claim has a non-placeholder evidence reference;
- final decision ACCEPT;
- explicit non-claims exist.

## Case B — REVISE

Expected:
- one required gate FAILS;
- no blocking required UNKNOWN remains;
- at least one revision names that failed gate;
- final decision REVISE.

## Case C — BLOCKED

Expected:
- at least one required gate is UNKNOWN or missing evidence;
- final decision BLOCKED.

## What the validator does not do

It does not:
- score GPU brands;
- estimate real performance from model names;
- choose a revision;
- verify that a path/URL contains truthful evidence;
- buy or modify hardware.

It checks the internal consistency and completeness of the design-review packet.
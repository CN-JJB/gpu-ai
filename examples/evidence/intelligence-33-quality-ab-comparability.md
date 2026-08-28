# Intelligence I33 — exact quality A/B comparability

Date: 2026-08-28

## Added

~~~text
tools/intelligence/compare_quality_metrics.py
tools/intelligence/quality_comparison_selftest.py
docs/specs/0034-intelligence-quality-ab-comparability.md
~~~

## Contract

Both sides must independently pass I31/I32 quality-metric verification.

Then the comparator requires exact match of:
- tokenizer identity;
- corpus SHA;
- fixture revision;
- evaluation argv;
- parser contract / metric name;
- quality executable SHA256 + bytes.

Only then does it compute descriptive PPL delta, ratio and percent change.

## Negative cases

The dedicated self-test blocks:
- candidate evaluation argv changes;
- candidate quality executable byte changes.

## Synthetic-only boundary

The self-test PPL values exist only to verify comparison arithmetic.

They are not real model-quality measurements or recommendation evidence.

## CI verification

~~~text
workflow: Intelligence Self-Test
run #141
run id: 33169970758
head: 2070476cd272f904476dff4100779a12ec534f59
job id: 98844439875
conclusion: success
~~~

The job explicitly passed:
- quality metric self-test;
- quality comparison self-test;
- quality execution + metric intake self-test;
- every historical Intelligence gate;
- market refresh self-test.

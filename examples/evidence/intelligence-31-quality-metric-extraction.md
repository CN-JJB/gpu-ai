# Intelligence I31 — fail-closed quality metric extraction

Date: 2026-08-28

## Added

~~~text
tools/intelligence/extract_quality_metric.py
tools/intelligence/verify_quality_metric.py
tools/intelligence/quality_metric_selftest.py
docs/specs/0032-intelligence-quality-metric-extraction.md
~~~

## Supported contract

~~~text
Final estimate: PPL = VALUE +/- UNCERTAINTY
~~~

Exactly one such line must exist across sealed stdout/stderr.

## Negative cases

The dedicated self-test confirms:
- manually changed metric JSON is rejected by independent reparse;
- chunk-only progress output is not treated as a final PPL;
- multiple Final estimate lines are ambiguous and blocked.

## Synthetic fixture boundary

All PPL numbers in the self-test are parser fixtures only.

They are not real model-quality measurements and must never be promoted into production benchmark/catalog data.

## CI verification

~~~text
workflow: Intelligence Self-Test
run #139
run id: 33169511764
head: fd8dc8065c790e72871e40994a70cdd1b35f9965
job id: 98842925807
conclusion: success
~~~

The job explicitly passed the dedicated quality metric self-test and every earlier Intelligence gate.

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

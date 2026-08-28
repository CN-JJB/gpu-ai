# Spec 0033 — Intelligence mandatory quality metric admission

Status: implemented in I32.

## Problem

I31 can extract and verify a machine-readable PPL artifact, but I29/I30 real intake can still reach READY without supplying that artifact.

That permits a real intake whose quality execution is authenticated but whose quality number is still absent from the admission contract.

## Decision

For non-synthetic intake, add:

~~~text
--quality-metric /path/to/quality-metric.json
~~~

The main `verify_real_intake.py` gate requires:
1. I28/I30 quality execution status PASS;
2. I31 metric verifier PASS;
3. only then may the overall intake reach READY.

## Reusable verifier

`verify_quality_metric.py` now exports a reusable verifier that:
- rechecks the sealed quality execution;
- reparses raw stdout/stderr;
- reconstructs the expected metric artifact;
- requires exact equality with the supplied artifact.

The main intake gate imports that verifier rather than duplicating parsing logic.

## Regression migration

Every older non-synthetic-style I22–I27 gate fixture now carries an explicitly synthetic quality metric artifact.

The synthetic helper labels the raw output as fixture-only and uses a parser value solely to exercise code paths.

No fixture quality number is production evidence.

## Fail-closed behavior

For real non-synthetic intake:
- missing `--quality-metric` -> BLOCKED;
- quality execution failure -> metric BLOCKED;
- unsupported/no-final raw format -> BLOCKED;
- changed metric JSON -> BLOCKED;
- only independently reproducible metric evidence -> PASS.

## Trust boundary

I32 makes machine-readable quality evidence mandatory.

It still does not make PPL:
- a universal quality score;
- a target-task score;
- a causal A/B conclusion;
- a purchase recommendation.

# Intelligence I32 — mandatory quality metric admission

Date: 2026-08-28

## Admission change

Real non-synthetic `verify_real_intake.py` now requires:

~~~text
--quality-metric quality-metric.json
~~~

after the existing I28/I30 quality execution evidence.

## Required chain

~~~text
sealed quality command/raw streams
→ I28/I30 execution PASS
→ I31 independent raw-output parse
→ quality-metric.json exact reproduction
→ QUALITY METRIC status=PASS
→ intake may continue to READY
~~~

## Regression coverage

The historical non-synthetic-style I22–I27 tests are migrated with synthetic-only metric fixtures.

The I29 intake self-test now explicitly proves:
- execution evidence without a metric is blocked;
- adding a valid independently reproducible metric reaches READY;
- tampered execution remains blocked even when a metric artifact is present.

## No fake production measurements

The helper metric value exists only inside synthetic tests.

Production benchmark data remains empty until learner-owned real evidence is acquired.

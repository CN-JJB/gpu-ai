# Intelligence I30 — exact quality evaluation argv binding

Date: 2026-08-28

## Gap closed

Before I30, `evaluation_args` was authenticated as a field but not tied to the actual executed quality argv.

I30 changes it from free-form text to an exact JSON token array and binds it to the executed command.

## New invariants

~~~text
quality_identity_schema_version = 2
quality_capture_schema_version = 2

quality identity evaluation_args
=
quality-command.json evaluation_args
=
actual argv after removing executable + model/corpus selectors
~~~

Order, duplicate tokens and exact string values are preserved.

## Fail-closed cases

The dedicated self-test verifies:
- a declared/actual evaluation-argument mismatch is rejected before launch;
- a matching v2 token list seals and verifies;
- a tampered command plus freshly recomputed PACKET is still blocked when the evaluation token vector differs from quality identity.

## Synthetic-only boundary

The self-tests use fixture flags and synthetic output strings only.

They contain no real PPL or GPU performance measurements and must never enter production benchmark data.

## CI verification

~~~text
workflow: Intelligence Self-Test
run #138
run id: 33169307905
head: d976103ecdaf848cf72dc6d28b9b53babb3dfdee
job id: 98842259986
conclusion: success
~~~

The job explicitly passed:
- Compile intelligence tools;
- every historical Intelligence evidence gate;
- Run quality execution self-test;
- Run quality evaluation argv self-test;
- Run quality execution intake self-test;
- Run market refresh self-test.


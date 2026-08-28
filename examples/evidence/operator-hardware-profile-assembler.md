# Operator Evidence — Hardware Profile Assembler

## Purpose

Close the setup gap between I54 raw semantic-source capture and the concrete hardware-profile artifact required by I24/I53.

Tool:

~~~text
tools/intelligence/assemble_hardware_profile.py
~~~

This is an operator artifact builder, not I55.

## Input contract

Input must be an I54 bundle with:

~~~text
status = READY-FOR-SEMANTIC-REVIEW
required_failures = []
~~~

Every referenced stdout/stderr path must:
- remain inside the semantic bundle directory;
- exist;
- match the recorded byte count;
- match the recorded SHA256.

## Output

~~~text
profile.txt
~~~

The output is canonical UTF-8 JSON containing:
- source bundle identity;
- each probe's argv/purpose/status/timestamps;
- return/timeout/launch metadata;
- stdout/stderr byte count and SHA256;
- exact stdout/stderr bytes encoded losslessly as base64.

The artifact records:

~~~text
automatic_semantic_inference = NOT-PERMITTED
automatic_manifest_update = NOT-PERMITTED
~~~

No GPU name, runtime build, backend, or execution field is inferred from raw text.

## Failure behavior

Assembly is blocked for:
- non-READY I54 bundles;
- required failures;
- stream tampering;
- byte-count mismatch;
- SHA256 mismatch;
- path traversal outside the bundle;
- an already existing output path.

The source bundle and raw streams are never modified.

## CI verification

~~~text
workflow: Intelligence Self-Test
run #178
run id 33195425859
head d308acbc62f3d540ed26181d23ed8a1602d127d1
job id 98931209062
conclusion success
~~~

Dedicated step:

~~~text
HARDWARE PROFILE ASSEMBLER SELFTEST: PASS
~~~

The same run also passed the first-real workspace bootstrap self-test and the complete I01–I54 suite.

No real GPU benchmark or production compatibility claim is represented by the self-test.

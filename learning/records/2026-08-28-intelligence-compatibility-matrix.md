# Learning / Build Record — 2026-08-28 Compatibility Coverage Matrix

## Frontier

Phase 4 Intelligence Stations — I09.

## Implemented

Spec:
- docs/specs/0010-intelligence-compatibility-coverage-matrix.md

Tool:
- tools/intelligence/compatibility_matrix.py

Evidence:
- examples/evidence/intelligence-09-compatibility-coverage-matrix.md

## Verified behavior

For Qwen3-8B + llama.cpp:

~~~text
observations=4
NEEDS-TEST=4
COVERAGE: PRESENT
~~~

The full self-test passes.

## Stable rule

~~~text
coverage
!=
ranking
~~~

The matrix answers “what evidence state do we have?” rather than “which GPU is fastest?”.
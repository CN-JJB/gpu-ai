# Learning / Build Record — 2026-08-27 Intelligence Compatibility Preflight

## Frontier

Phase 4 Intelligence Stations — I02.

## Problem

A yes/no compatibility field would collapse three different claims:

~~~text
mechanism documented
exact path measured
unknown/partial support
~~~

That would recreate the same evidence problem the stable course teaches learners to avoid.

## Implemented

Spec:
- docs/specs/0003-intelligence-compatibility-preflight.md

Production catalog:
- intelligence/catalog/runtimes.jsonl
- intelligence/catalog/compatibility.jsonl

Tool:
- tools/intelligence/compatibility_preflight.py

Validation:
- tools/intelligence/validate_catalog.py now validates runtime and compatibility records;
- tools/intelligence/selftest.py now checks documented-support semantics.

Evidence:
- examples/evidence/intelligence-02-compatibility-preflight.md

## Stable rule

~~~text
official docs say mechanism/path supported
→ NEEDS-TEST

real exact-path Evidence succeeds
→ PASS-MEASURED
~~~

Do not promote DOCUMENTED_SUPPORTED to MEASURED_SUPPORTED.

## Freshness

Compatibility is dynamic.

A stale support observation returns:

~~~text
STALE-REVALIDATE
~~~

before using it for a current purchase/deployment decision.

## Next

I03 should add measured compatibility ingestion and additional vendor/backend support observations before any broad “compatible GPUs” ranking is built.
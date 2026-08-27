# Learning / Build Record — 2026-08-27 Measured Compatibility Ingestion

## Frontier

Phase 4 Intelligence Stations — I03.

## Implemented

Spec:
- docs/specs/0004-intelligence-measured-compatibility-ingestion.md

Tool:
- tools/intelligence/ingest_measured_compatibility.py

Updated:
- compatibility_preflight.py now prefers exact artifact/build Evidence;
- benchmark records now require canonical runtime_id;
- validate_catalog.py validates benchmark runtime references;
- selftest covers exact measured upgrade and artifact mismatch fallback.

Evidence:
- examples/evidence/intelligence-03-measured-compatibility.md

## Stable rule

~~~text
one measured exact path
!=
family-wide compatibility
~~~

Exact Evidence may upgrade only the scope it actually proves.
# Machine-Readable Intelligence Catalog

This directory is the queryable counterpart to the dated Markdown snapshots under intelligence/.

## Production rule

Only auditable records belong here.

~~~text
no source
→ no production record
~~~

Synthetic demonstrations belong under:

~~~text
tools/intelligence/fixtures/
~~~

## Current seed

The initial catalog deliberately contains only a very small number of records.

That is intentional.

The goal is to prove:
- canonical IDs;
- provenance;
- freshness;
- cross-record validation;
- Hardware ↔ Model ↔ Benchmark joins.

It is not yet a comprehensive GPU/model database.

## Validate

~~~bash
python3 tools/intelligence/validate_catalog.py intelligence/catalog
~~~

## Query

~~~bash
python3 tools/intelligence/query_bridge.py intelligence/catalog --hardware-id hw:nvidia:geforce-rtx-3090:24g --model-id model:qwen:qwen3-8b
~~~

If no real benchmark has been ingested, the correct result is:

~~~text
NO MATCHING BENCHMARK OBSERVATIONS
~~~

Do not fill that gap with guessed performance.
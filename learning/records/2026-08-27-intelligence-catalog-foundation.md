# Learning / Build Record — 2026-08-27 Intelligence Catalog Foundation

## Frontier

Phase 4 Intelligence Stations — I01.

This is infrastructure/dynamic-data work, not Slice 50 of the stable course mainline.

## Problem

The repository already had useful dated Markdown intelligence snapshots, but no canonical machine-readable join layer.

That prevented reliable queries across:

~~~text
hardware
↔ model
↔ benchmark
↔ market
~~~

without manually copying facts.

## Implemented

Spec:
- docs/specs/0002-intelligence-stations-data-contract.md

Schema/docs:
- intelligence/schema/README.md
- intelligence/catalog/README.md

Production seed:
- intelligence/catalog/hardware.jsonl
- intelligence/catalog/models.jsonl
- intelligence/catalog/market.jsonl
- intelligence/catalog/benchmarks.jsonl

Tools:
- tools/intelligence/validate_catalog.py
- tools/intelligence/query_bridge.py
- tools/intelligence/ingest_llama_bench.py
- tools/intelligence/selftest.py

Fixtures:
- tools/intelligence/fixtures/catalog/
- tools/intelligence/fixtures/experiment61/

Evidence:
- examples/evidence/intelligence-01-catalog-foundation.md

## Stable design

Use:

~~~text
canonical ENTITY
+
dated OBSERVATION
~~~

rather than one mutable “GPU row” containing identity, price, support and performance.

## Benchmark rule

Real benchmark observations should come from the existing Evidence path:

~~~text
Experiment 61
→ raw llama-bench
→ Evidence Packet
→ intelligence ingester
~~~

Do not manually type tok/s into the catalog when the raw Evidence exists elsewhere.

## Ranking rule

No universal leaderboard yet.

Before ranking:
- workload identity must be comparable;
- runtime/model artifact identity must be visible;
- market cohort/evidence state must be explicit;
- price/performance observations must be deliberately paired.

## Production data discipline

The initial benchmark catalog is intentionally empty.

A missing real benchmark is represented as missing evidence, not a synthetic estimate.

## Next

Intelligence I02:
- compatibility observation schema;
- runtime/backend/quant/hardware support states;
- OFFICIAL vs MEASURED vs UNKNOWN;
- freshness triggers;
- compatibility preflight query.
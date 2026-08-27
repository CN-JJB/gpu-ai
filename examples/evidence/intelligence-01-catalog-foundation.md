# Evidence — Intelligence I01: Catalog + Benchmark Bridge Foundation

Status: machine-readable intelligence foundation implemented.

## Claim

Dynamic intelligence can be queried without turning volatile observations into stable Lesson facts and without creating a second manual benchmark truth source.

## Implemented contract

The Phase 4 foundation separates:

~~~text
ENTITY
→ canonical hardware/model join identity

OBSERVATION
→ dated + sourced + condition-bound market/benchmark fact
~~~

Production JSONL catalog:

~~~text
intelligence/catalog/hardware.jsonl
intelligence/catalog/models.jsonl
intelligence/catalog/market.jsonl
intelligence/catalog/benchmarks.jsonl
~~~

## Production seed

The production catalog intentionally starts small:
- one official hardware entity;
- one official model entity;
- one secondary market observation;
- zero guessed benchmark observations.

The empty production benchmark catalog is a feature, not missing filler.

~~~text
no Evidence Packet
→ no benchmark row
~~~

## Benchmark bridge

Preferred ingestion path:

~~~text
Experiment 61 manifest
+ raw llama-bench JSON
+ Evidence Packet
→ tools/intelligence/ingest_llama_bench.py
→ benchmark observation
~~~

The importer preserves:
- hardware canonical ID;
- model canonical ID;
- artifact SHA/bytes/quant;
- runtime/backend/build identity;
- workload conditions;
- PP/TG;
- source paths.

## Query discipline

tools/intelligence/query_bridge.py:
- joins Hardware ↔ Model ↔ Benchmark by canonical IDs;
- shows market observations separately;
- groups benchmarks by workload fingerprint;
- performs no implicit price/performance merge;
- performs no cross-workload leaderboard ranking.

## Validator gates

tools/intelligence/validate_catalog.py rejects:
- duplicate IDs;
- broken hardware/model references;
- invalid provenance;
- placeholder benchmark identity;
- missing raw/manifest references;
- synthetic records in production mode.

Stale observations are warnings rather than automatically false.

## Synthetic fixture

Synthetic fixture values:

~~~text
PP = 1000 tok/s
TG = 50 tok/s
~~~

exist only under tools/intelligence/fixtures/.

They prove tool behavior only.

They are not performance claims.

## Self-test contract

tools/intelligence/selftest.py verifies:
1. production catalog validates;
2. fixture catalog validates only with explicit synthetic allowance;
3. the bridge returns the fixture benchmark;
4. the Experiment 61 importer reproduces fixture PP/TG;
5. a benchmark with a broken hardware reference is rejected.

Expected final line:

~~~text
SELFTEST: PASS
~~~

## Stable boundary preserved

The catalog does not move:
- used price;
- current backend support;
- current model ecosystem;
- benchmark numbers

into stable Lessons.

Those remain dated intelligence observations.

## Next

Intelligence I02 should add:
- runtime/backend/quant compatibility observations;
- exact support status semantics;
- freshness/revalidation rules for support matrices;
- join queries that answer “can this runtime/artifact/hardware path be tested?” without converting UNKNOWN into PASS.
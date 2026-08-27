# Spec 0002 — Intelligence Stations Data Contract v1

Status: implemented foundation  
Date: 2026-08-27

## Problem

The repository already contains dated dynamic-intelligence snapshots, but most are human-readable Markdown.

Phase 4 needs a machine-readable layer that can answer:

~~~text
which hardware?
+ which exact model/artifact?
+ which runtime/backend?
+ which workload?
+ which measured result?
+ which market observation?
+ what source and freshness?
~~~

without copying benchmark numbers into an unrelated ranking table.

## Scope

This first vertical slice implements:

1. canonical Hardware entities;
2. canonical Model entities;
3. Market observations;
4. Benchmark observations;
5. a validator;
6. an Experiment-61 / llama-bench ingestion bridge;
7. a query bridge that joins Hardware ↔ Model ↔ Benchmark.

It does not implement:
- a universal recommendation score;
- automatic web scraping;
- automatic purchasing;
- cross-workload benchmark ranking;
- truth verification of external sources;
- silent conversion of Markdown snapshots into trusted facts.

## Core design

Use two categories:

~~~text
ENTITY
→ stable-ish identity used for joins

OBSERVATION
→ dated, sourced, condition-bound dynamic fact
~~~

Example entity:

~~~text
hardware_id = hw:nvidia:geforce-rtx-3090:24g
~~~

Example observation:

~~~text
secondary reported price = 7400 CNY on 2026-08-22
~~~

A TG number is only a benchmark observation when hardware, model, runtime, workload and evidence are also present.

## Canonical join IDs

IDs are opaque stable strings, not display names.

Recommended prefixes:

~~~text
hw:
model:
market:
bench:
~~~

Display names may change without breaking joins.

## Catalog files

v1 uses JSON Lines:

~~~text
intelligence/catalog/hardware.jsonl
intelligence/catalog/models.jsonl
intelligence/catalog/market.jsonl
intelligence/catalog/benchmarks.jsonl
~~~

One line equals one complete record.

JSONL is chosen because it is diff-friendly, appendable, easy to stream, and easy to import into SQLite/DuckDB later.

## Provenance contract

Every production record must preserve enough provenance to audit it.

Minimum source block:

~~~json
{
  "evidence_class": "OFFICIAL",
  "url": "https://...",
  "observed_at": "2026-08-27"
}
~~~

Allowed evidence classes:

- OFFICIAL
- MEASURED
- DERIVED
- SECONDARY
- SELLER
- SYNTHETIC

SYNTHETIC is rejected from the production catalog by default.

## Freshness contract

Dynamic observations may include:

~~~json
"revalidate_after": "2026-09-03"
~~~

The validator warns when a record is stale relative to the chosen as-of date.

Stale does not mean false. It means the observation should not be used as current without revalidation.

## Hardware entity

Required:
- hardware_id;
- canonical_name;
- vendor;
- accelerator_kind;
- source.

Useful stable identity fields may include:
- memory_gib;
- memory_type;
- architecture;
- product_class.

Do not store current used price in the hardware entity.

## Model entity

Required:
- model_id;
- canonical_name;
- repository;
- architecture;
- source.

Optional:
- license;
- family;
- model_type.

Do not store a particular quantized artifact as if it were the whole model identity.

Exact artifact SHA, bytes and quant belong in the benchmark observation.

## Market observation

Required:
- hardware_id;
- geography/channel;
- cohort/condition;
- price state;
- currency/value;
- observed_at;
- source.

A merchant quote and a peer-to-peer confirmed sale are different cohorts/evidence states.

Do not average them silently.

## Benchmark observation

Required join keys:
- hardware_id;
- model_id;
- runtime_id.

Required identity:
- exact model artifact SHA/bytes/quant;
- runtime/backend/build identity;
- workload protocol;
- execution conditions;
- measured PP/TG if present;
- raw result source;
- manifest source;
- packet/evidence source where available.

Benchmark rows must never be interpreted outside their workload identity.

## Workload comparability

Two benchmark observations are directly comparable only when the relevant workload/semantic identity is equivalent.

The v1 query bridge groups by workload fingerprint instead of pretending all tok/s values belong to one leaderboard.

Future ranking code must preserve this rule.

## Benchmark ingestion

Preferred path:

~~~text
Experiment 61 manifest
+ raw llama-bench JSON
+ Evidence Packet
→ ingest_llama_bench.py
→ benchmark JSONL record
~~~

This prevents a second manual benchmark truth source.

The importer does not prove the benchmark was honestly executed; it preserves the evidence chain.

## Derived metrics

Do not compute tokens/s/元, J/token or TCO score unless the exact observations being combined are explicitly selected and compatible.

v1 query output therefore does not silently merge a random market price with a benchmark.

## Validation gates

Production catalog fails validation for:
- duplicate IDs;
- broken hardware/model references;
- missing source/date;
- invalid evidence class;
- placeholder benchmark identity;
- benchmark without raw/manifest evidence references;
- synthetic records unless explicitly allowed.

Staleness is warning-level by default.

## Synthetic fixtures

Tool fixtures live under:

~~~text
tools/intelligence/fixtures/catalog/
~~~

They exist to prove join/validator behavior and must not be presented as real hardware performance.

## Migration rule for existing Markdown intelligence

Existing dated Markdown snapshots remain valid historical evidence.

Migration is incremental:

~~~text
read snapshot
→ extract one bounded claim
→ preserve original source/path/date/evidence class
→ create machine-readable observation
→ validate
~~~

Do not bulk-convert prose into PASS facts.

## Success condition

The vertical slice is successful when:

~~~text
hardware entity
+ model entity
+ benchmark observation
→ one auditable bridge query
~~~

and a malformed or missing-evidence record is rejected.

## Next slice

After the foundation is verified:
1. ingest real Experiment 61 benchmark packets;
2. add runtime/quant compatibility observations;
3. add normalized market observations;
4. build comparable-workload views;
5. only then add recommendation/TCO queries.
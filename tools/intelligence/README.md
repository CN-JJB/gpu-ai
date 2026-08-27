# Intelligence Tooling

## 1. Validate a catalog

~~~bash
python3 validate_catalog.py ../../intelligence/catalog
~~~

Checks:
- duplicate IDs;
- record structure;
- provenance;
- canonical references;
- benchmark evidence identity;
- synthetic leakage;
- freshness warnings.

## 2. Validate synthetic fixtures

~~~bash
python3 validate_catalog.py fixtures/catalog --allow-synthetic
~~~

## 3. Query Hardware ↔ Model ↔ Benchmark

~~~bash
python3 query_bridge.py fixtures/catalog --hardware-id hw:fixture:24g --model-id model:fixture:8b --include-synthetic
~~~

The output groups benchmark observations by workload fingerprint.

## 4. Ingest a real llama-bench result

Preferred input is the Experiment 61 manifest plus raw llama-bench JSON.

~~~bash
python3 ingest_llama_bench.py --manifest /path/to/baseline-manifest.json --result /path/to/baseline.json --hardware-id hw:... --model-id model:... --record-id bench:... --observed-at 2026-08-27 --packet-source /path/to/PACKET.json --out benchmark-record.jsonl
~~~

Review the generated JSON before appending it to the production catalog.

The importer:
- extracts PP/TG means from llama-bench JSON;
- copies exact artifact/runtime/workload identity from the manifest;
- records evidence paths;
- does not invent missing data.

## Non-goals

These tools do not:
- scrape marketplaces;
- prove external sources are truthful;
- create a universal GPU score;
- compare unlike workloads;
- auto-purchase hardware.
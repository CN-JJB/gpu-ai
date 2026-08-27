# Evidence — Intelligence I07: Real Benchmark Intake Gate

Date: 2026-08-27  
Status: verified

## Claim

A benchmark must pass an Evidence-intake gate before it is allowed into the production intelligence benchmark catalog.

## Required intake bundle

~~~text
catalog
+ Experiment 61 manifest
+ raw benchmark result
+ PACKET.json
+ hardware_id
+ model_id
+ runtime_id
+ observed_at
~~~

The intake verifier does not mutate the catalog.

## Gates

### Canonical IDs

The hardware, model and runtime IDs must already exist in the selected catalog.

Unknown IDs block intake.

### Manifest completeness

Required identity includes:
- hardware device identity/profile SHA;
- runtime/backend/build;
- artifact SHA/bytes/quant/source revision;
- context/sequences;
- PP/TG/repetitions;
- prompt token-ID SHA;
- tokenizer/corpus/fixture identity.

Placeholders block intake.

### Raw result

At least one positive PP/TG avg_ts must exist.

No missing metric is invented.

### Packet integrity

The supplied manifest and raw result must be indexed by PACKET.json with matching:
- SHA256;
- byte count.

## Verified synthetic cases

Intact synthetic packet:

~~~text
INTAKE: READY
~~~

Tampered manifest SHA in packet:

~~~text
INTAKE: BLOCKED
SHA256 not indexed by packet
~~~

The full intelligence self-test remains:

~~~text
SELFTEST: PASS
~~~

## READY boundary

READY means only:

> the evidence bundle is internally complete enough to pass to ingestion.

It does not prove benchmark honesty, hardware health, quality, serving SLO or purchase suitability.

## Production result

Repository search found no existing real Experiment 61-compatible packet/result bundle.

Therefore:

~~~text
production benchmarks.jsonl
remains empty
~~~

This is correct evidence discipline, not missing implementation.
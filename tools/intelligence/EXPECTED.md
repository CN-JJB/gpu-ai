# Expected — Intelligence Tooling Self-Test

Run from repository root:

~~~bash
python -m py_compile tools/intelligence/*.py
python tools/intelligence/selftest.py
~~~

## Current verified frontier

~~~text
I01–I53
~~~

Latest implementation verification:

~~~text
workflow: Intelligence Self-Test
run #172
run id 33193068222
head 0f40cc26466c21730bdea2e2b7e2a1e687b28612
job id 98923186654
conclusion success
Python 3.12
Ubuntu 24.04
~~~

## Major verified chains

### Real benchmark + quality intake

~~~text
I20–I32
raw identity
→ model artifact
→ command binding
→ hardware profile
→ prompt evidence
→ corpus
→ quality identity
→ sealed quality execution
→ exact evaluation argv
→ machine PPL
→ mandatory non-synthetic admission
~~~

### Model tradeoff

~~~text
I33 → I36 → I37 → I38
~~~

### Execution-variable tradeoff

~~~text
I35 → I39 → I40 → I41
~~~

### Unified route + readiness

~~~text
I42 route
→ I43 gap matrix
→ I44/I45 used-GPU acceptance
→ I46/I47 explicit performance target
→ I48/I49 explicit price ceiling
→ I50/I51 condition-evidence provenance
~~~

The complete run includes dedicated tests for every listed stage.

### I52 — real evidence session orchestration

~~~text
explicit session JSON
→ benchmark capture
→ quality capture
→ machine PPL extraction
→ full I20–I32 intake
~~~

The dedicated self-test proves the runner can reach `REAL SESSION: READY` through the existing gates, preserves failed-step evidence, never overwrites a non-empty output directory, and indexes profile/prompt/corpus/quality identity in the main benchmark PACKET.

All I52 self-test metrics are synthetic fixtures only.

### I53 — byte-derived session preparation

~~~text
explicit semantic session
+ local source bytes
→ materialized manifest / quality identity
→ READY-TO-RUN-I52
~~~

The dedicated self-test verifies:
- GGUF SHA/bytes materialization;
- profile/corpus SHA materialization;
- prompt identity synchronization;
- quality argv ↔ identity exactness;
- source files are never modified in place;
- unresolved runtime/device/model-source/execution placeholders block before launch.

I53 produces no PP/TG/PPL values.

## Decision boundary

I43 can only emit:

~~~text
BLOCKED
READY-FOR-HUMAN-REVIEW
~~~

It always records:

~~~text
automatic_purchase_decision = NOT-PERMITTED
~~~

No weighted recommendation score exists.

## Condition contract

~~~text
C0 no production-usable evidence / synthetic
C1 seller/listing claim only
C2 current external evidence without learner-owned reproducible acceptance
C3 learner-owned PACKET-bound independently reproducible I44 evidence
C4 reserved
~~~

Health outcome remains separate:

~~~text
ACCEPT
REVIEW
REJECT
~~~

## Synthetic fixture boundary

All synthetic PP/TG/PPL/market/acceptance/policy fixtures prove tool behavior only.

They are not:
- GPU performance claims;
- model-quality claims;
- market transaction evidence;
- card-health certificates;
- purchase recommendations.

Production benchmark rows remain zero until learner-owned real evidence is admitted.

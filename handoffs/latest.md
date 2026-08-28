# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

- CN-JJB/gpu-ai
- main

## Stable course

~~~text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
~~~

## Phase 4 frontier

~~~text
I01–I30 implemented and CI verified
~~~

## Latest CI

~~~text
run #133
run id 33157503815
head 96c805572b7e4f3c9f2882ec175045e25674a672
job id 98803698443
conclusion success
full SELFTEST: PASS
market refresh SELFTEST: PASS
~~~

## Benchmark boundary

Production benchmark catalog remains empty.

Required:

~~~text
manifest + raw result + PACKET + canonical IDs
→ I07 READY
→ ingest
→ validate
→ exact MEASURED_SUPPORTED
~~~

## Market evidence

~~~text
SECONDARY_REPORTED        → M1
MEDIAN_ASK                → M2
SOLD_MARKED_LISTING_PRICE → M3
~~~

Current active signals:

~~~text
eBay asks:
3090 1499
7900 XTX 1020
A770 330 USD

OfferUp SOLD-marked displayed medians:
3090 950
7900 XTX 700
A770 200 USD

China secondary:
3090 7400
A770 1400 CNY
~~~

## A770 append-only refresh

Historical:

~~~text
2026-08-21
1450 CNY
~~~

Current:

~~~text
2026-08-25
1400 CNY
revalidate_after=2026-09-01
~~~

Lineage:

~~~text
old.superseded_by = new
new.supersedes = old
~~~

The old row remains audit history but is not current purchase evidence.

## Active-view semantics

~~~text
market_matrix
→ hides superseded by default

freshness_report
→ SUPERSEDED, not active stale queue

market_evidence_gate
→ SUPERSEDED-USE-NEWER-OBSERVATION
~~~

Use --include-superseded for audit history.

## Watchlist freshness

~~~text
CURRENT + M2/M3 → ELIGIBLE
DUE/STALE/INVALID → not purchase-eligible
~~~

Experiment 38 cannot emit BUY-CANDIDATE from stale/due/invalid market evidence.

## I19 reusable refresh helper

```text
tools/intelligence/market_refresh.py
```

Use a complete new observation candidate plus the active old record.

The helper creates reciprocal append-only lineage and rejects:
- already-superseded forks;
- cross-hardware links;
- non-newer observations.

CI run #67 verifies the helper and keeps the original full self-test green.

## I20 raw benchmark identity gate

```text
verify_real_intake.py
→ PACKET hash/bytes
+ exact PP/TG protocol rows
+ manifest ↔ raw llama-bench identity/config agreement
→ RAW IDENTITY: PASS
→ INTAKE: READY
```

The verifier now blocks a recomputed, hash-consistent packet when the manifest claims a different GPU/backend/build/model/config than the raw benchmark evidence.

Implementation checkpoint: run #74.  
Final documented head: run #76, success.

## I21 capture/seal helper

```text
capture_real_benchmark.py
→ explicit argv, shell=False
→ stdout + stderr + command identity + exit code
→ optional evidence copies
→ PACKET.json
→ CAPTURE: SEALED
```

`SEALED` is not admission.

The sealed bundle must still pass I07/I20.

CI run #81 keeps the full suite, I21 capture self-test and I19 refresh self-test green.

## I22 local model artifact gate

For non-synthetic intake:

```text
--model-artifact MODEL.gguf
→ local bytes + SHA256
↔ manifest artifact_bytes + artifact_sha256
↔ I20 raw llama-bench model_size
→ MODEL ARTIFACT status=PASS
```

CI run #86 keeps full, capture, artifact and refresh tests green.

## I23 command ↔ model binding

For non-synthetic intake:

```text
I21 command.json exact argv
↔ -m/--model path
↔ I22 locally verified GGUF
↔ manifest artifact identity
↔ raw llama-bench model_size
```

command.json must itself be PACKET-indexed.

A tampered argv plus freshly recomputed PACKET is still blocked.

CI run #93 keeps full, capture, artifact, command-binding and refresh tests green.

## I25 prompt evidence gate

Experiment 57 prompt evidence now backs Experiment 61 `variant.prompt.*`.

For non-synthetic intake, the prompt-evidence manifest must be PACKET-indexed and match messages/template/rendered/token-ID hashes plus token count.

CI run #110 keeps the full suite green.

## I26 quality corpus gate

Non-synthetic intake now requires the concrete quality corpus.

Its SHA256 must match `fixed.quality_eval.corpus_sha256`, and the artifact must be PACKET-indexed.

CI run #122 is green.

## I27 quality identity gate

Experiment 59 now has a machine-readable quality identity artifact.

Tokenizer identity, corpus SHA, fixture revision and evaluation args must match Experiment 61 `fixed.quality_eval.*` and be PACKET-indexed.

CI run #133 is green.

## I28 quality execution evidence

Experiment 59 quality execution now has a dedicated capture + verification lane:

~~~text
capture_quality_eval.py
→ exact argv, shell=False
→ exact -m/--model + -f/--file bindings
→ model/corpus SHA256 + bytes
→ I27 quality identity artifact binding
→ raw stdout.txt + stderr.txt
→ quality-command.json + PACKET.json
→ QUALITY CAPTURE: SEALED

verify_quality_execution.py
→ independent argv reparse + re-hash
→ QUALITY EXECUTION: PASS
~~~

Run #134 is green, including the dedicated quality execution self-test.

I28 intentionally does not parse PPL.

## I29 mandatory quality execution admission

For non-synthetic intake, `verify_real_intake.py` now requires:

~~~text
--quality-command-record
--quality-stdout
--quality-stderr
--quality-packet
~~~

These are checked against the same I22 model artifact, I26 corpus and I27 quality identity.

The quality PACKET remains separate from the benchmark PACKET.

Run #136 is green, including the new quality execution intake self-test and every prior Intelligence gate.

## I30 exact evaluation argv binding

Quality identity is now schema v2:

~~~text
evaluation_args = exact JSON argv-token list
~~~

Capture and verification independently remove only:
- argv[0] executable;
- exactly one model selector;
- exactly one corpus selector.

Every remaining token must match `evaluation_args` exactly and in order.

Quality command records are schema v2 and store the derived evaluation token list.

Run #138 is green, including the dedicated I30 self-test plus every prior Intelligence gate.

## Next work

1. I31: add fail-closed machine-readable quality metric extraction/admission from sealed raw output.
2. Acquire the first learner-owned real Experiment 61 packet through I21 → I07/I20/I22/I23/I24/I25/I26/I27/I29/I30.
3. Use the market refresh helper for due/stale evidence and stronger RTX 3090 China evidence when auditable.
4. No recommendation leaderboard yet.

No auto-purchase or unsafe hardware modification.

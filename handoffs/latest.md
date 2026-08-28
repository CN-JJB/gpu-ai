# Handoff — GPU × Local LLM Course / Intelligence Stations

## Repo

~~~text
CN-JJB/gpu-ai
branch: main
~~~

## Stable course

~~~text
Slices 01–49
Experiments 01–93
v1 stable mainline complete
~~~

## Phase 4 frontier

~~~text
I01–I54 implemented
operator bootstrap + hardware-profile assembler added without creating I55
latest implementation CI: run #178 success
~~~

CI identity:

~~~text
run id 33195425859
head d308acbc62f3d540ed26181d23ed8a1602d127d1
job id 98931209062
~~~

## Production boundary

~~~text
real production benchmark rows = 0
~~~

Do not promote synthetic benchmark, PPL, market, acceptance, price-policy or readiness fixtures into production evidence.

## Real benchmark / quality admission

Non-synthetic Experiment 61 admission requires:
- manifest + raw result + benchmark PACKET;
- canonical hardware/model/runtime IDs;
- exact local model artifact;
- benchmark command record;
- hardware profile;
- Experiment 57 prompt evidence;
- concrete quality corpus;
- quality identity schema v2;
- sealed quality execution command/raw streams + quality PACKET;
- exact evaluation argv;
- independently reproducible PPL metric.

Only then may `verify_real_intake.py` return `INTAKE: READY`.

## Verified tradeoff lanes

~~~text
model:
I33 → I36 → I37 → I38

execution variable:
I35 → I39 → I40 → I41

routing:
I42
variant.model* → I38
variant.execution.* → I41
other → BLOCKED
~~~

No tradeoff artifact is a recommendation.

## Decision-readiness lane

I43 independently checks:
- verified tradeoff route;
- real MEASURED benchmark provenance;
- exact current MEASURED_SUPPORTED compatibility;
- current M2/M3 market evidence;
- Experiment 90 whole-machine feasibility;
- I44 real used-GPU ACCEPT;
- I46 explicit performance target PASS;
- I48 explicit price result WITHIN-CEILING using the same market record;
- I50 C3/C4 condition provenance.

Output is only:

~~~text
BLOCKED
or
READY-FOR-HUMAN-REVIEW
~~~

and always:

~~~text
automatic_purchase_decision = NOT-PERMITTED
~~~

## Condition evidence contract

I50 introduced the first stable C0–C4 definition because Experiment 38 previously referenced C3/C4 without defining them.

~~~text
C0 no production-usable evidence / synthetic
C1 seller/listing claim only
C2 current external evidence without learner-owned reproducible acceptance
C3 learner-owned PACKET-bound independently reproducible I44 evidence
C4 reserved: C3 + independent corroborating inspection provenance
~~~

Evidence strength is separate from technical health:

~~~text
C3 + ACCEPT → both condition-related gates can pass
C3 + REJECT → strong evidence, but used_gpu_acceptance blocks
~~~

I50 does not emit C4.

## Price policy contract

I48 does not infer fair value.

The learner supplies:
- exact market record;
- hardware ID;
- currency;
- personal max sticker;
- watch band.

Neutral outputs:

~~~text
WITHIN-CEILING
WATCH-BAND
ABOVE-BAND
~~~

Only real WITHIN-CEILING can satisfy the I49 price component. It is still not BUY.

## Performance policy contract

I46 uses only explicit hard thresholds:
- min candidate PP;
- min candidate TG;
- optional max candidate PPL;
- optional max PPL percent change.

No weighted score is used.

## I52 real evidence session runner

Use:

~~~text
labs/experiments/61-real-benchmark-evidence-packet/real-evidence-session.template.json
tools/intelligence/run_real_evidence_session.py
~~~

The session runner orchestrates only existing gates:

~~~text
benchmark capture
→ quality capture
→ PPL extraction
→ verify_real_intake
~~~

It accepts explicit argv arrays and uses no shell.

On success it emits `REAL SESSION: READY`, `session-summary.json`, and `intake-args.json`.

Do not ingest automatically. Review the real evidence first.

## First-real workspace bootstrap

Preferred entry point on the actual machine:

~~~text
tools/intelligence/bootstrap_real_evidence_workspace.py
~~~

For the NVIDIA-first path:

~~~bash
python3 tools/intelligence/bootstrap_real_evidence_workspace.py \
  --out-dir /path/to/e61-real \
  --profile rtx3090-qwen3-8b-llamacpp
~~~

The output includes `RUN.md`, `workspace.json`, `baseline-manifest.json`, `quality-identity.json`, `real-session.json`, `semantic-probes.json`, and an empty `prompt-evidence/`.

It deliberately creates no fake hardware/model/prompt/corpus/benchmark evidence and launches nothing automatically.

This tool is operator ergonomics, not I55.

## Hardware profile assembler

After a READY I54 bundle, use:

~~~text
tools/intelligence/assemble_hardware_profile.py
~~~

Preferred workspace command:

~~~bash
python3 tools/intelligence/assemble_hardware_profile.py \
  /path/to/e61-real/semantic-source-evidence/bundle.json \
  --out /path/to/e61-real/profile.txt
~~~

The assembler re-hashes every referenced raw stream, embeds the exact bytes losslessly, and refuses blocked/tampered/path-escaping bundles.

It performs no semantic inference and does not modify the manifest.

It exists to produce the concrete profile artifact already required by I24/I53; it is not I55.

## I54 semantic source capture

Before manually filling the semantic fields that I53 refuses to infer, use:

~~~text
tools/intelligence/capture_semantic_sources.py
~~~

The NVIDIA-first probe plan is:

~~~text
labs/experiments/61-real-benchmark-evidence-packet/semantic-source-probes.rtx3090-llamacpp.json
~~~

I54 runs only explicit argv arrays with no shell and preserves raw stdout/stderr, return codes, timestamps and SHA256.

It always records:

~~~text
automatic_manifest_update = NOT-PERMITTED
~~~

A successful capture emits `READY-FOR-SEMANTIC-REVIEW`, not manifest truth. Review the raw sources and deliberately fill device/runtime/build/backend/execution semantics.

## I53 real session materializer

Before I52, prefer:

~~~text
tools/intelligence/prepare_real_evidence_session.py
~~~

I53 writes a new prepared copy and safely materializes only byte-derived fields:

~~~text
model SHA256 + bytes
hardware profile SHA256
quality corpus SHA256
prompt identity
quality identity corpus SHA256
Experiment 61 fixed.quality_eval
~~~

It does not infer:
- device identity;
- runtime/build/backend;
- model quant/source revision;
- execution semantics.

Those must already be explicitly filled or I53 blocks before any benchmark launch.

Main acquisition order:

~~~text
clean real workspace bootstrap
→ explicit probe plan
→ I54 READY-FOR-SEMANTIC-REVIEW
→ assemble verified profile.txt
→ human semantic review/fill
→ I53 READY-TO-RUN-I52
→ I52 REAL SESSION: READY
→ human benchmark/quality review
→ deliberate ingestion
~~~

## Next work

1. Bootstrap a clean NVIDIA-first real workspace on the actual benchmark machine.
2. Follow its `RUN.md`: run I54 and require `READY-FOR-SEMANTIC-REVIEW`.
3. Assemble `profile.txt` from that READY bundle and require `HARDWARE PROFILE ASSEMBLER: READY`.
4. Review raw/profile observations and deliberately fill explicit device/runtime/model-source/execution semantics plus real Experiment 57/59 artifacts.
5. Run I53 and require `READY-TO-RUN-I52`.
6. Run the prepared session through I52 and require `REAL SESSION: READY`; manually review before ingestion.
7. After reviewed ingestion, derive exact measured compatibility.
8. Acquire real Experiment 87/I44 acceptance, create I46/I48 policies, and run I43.
9. Refresh market evidence only with newer/stronger provenance; no leaderboard before real evidence.

No auto-purchase, no unsafe hardware modification.

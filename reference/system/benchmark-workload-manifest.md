# Benchmark / Workload Manifest Contract

## Purpose

A benchmark number is not meaningful until its workload identity is reconstructable.

The manifest freezes the experiment into:

```
fixed protocol
+
semantic variant blocks
+
audit/output files
```

The validator then checks that baseline and candidate differ only in one declared semantic path.

---

# Structure

```json
{
  "schema_version": 1,
  "comparison_id": "one-stable-id",
  "label": "baseline",
  "intentional_variable": "variant.execution.flash_attention",
  "fixed": {},
  "variant": {},
  "audit": {}
}
```

## fixed

Fields that define the comparison protocol and should not move during the A/B.

Typical:

```
fixed.protocol
fixed.quality_eval
```

Examples:
- PP/TG token counts;
- repetitions/warmup;
- quality corpus SHA;
- tokenizer identity;
- fixture revision.

## variant

Semantic system blocks that may be compared one at a time.

Recommended blocks:

```
variant.hardware
variant.runtime
variant.model
variant.execution
variant.prompt
variant.sampler
```

## audit

Paths/records that naturally differ between baseline/candidate but are not semantic workload variables.

Examples:
- exact command string;
- raw output path;
- telemetry file path;
- quality log path;
- timestamp.

Audit fields are still checked for placeholders.

---

# Declaring one variable

## Leaf variable

FlashAttention A/B:

```
intentional_variable
=
variant.execution.flash_attention
```

Only that leaf may change.

## Semantic block

Quantization A/B changes several fields together:

```
artifact SHA
artifact bytes
quant label
```

Those are one semantic intervention:

```
intentional_variable
=
variant.model
```

All differences beneath `variant.model` are allowed.

Everything outside that block must remain equal.

This avoids the false rule:

> model SHA must never change.

That rule would make a real Q8 → Q4 comparison impossible.

---

# Required identity

Current validator requires at least:

```
schema_version
comparison_id
intentional_variable

fixed.protocol.pp_tokens
fixed.protocol.tg_tokens
fixed.protocol.repetitions

fixed.quality_eval.tokenizer_identity
fixed.quality_eval.corpus_sha256

variant.hardware.device_identity
variant.runtime.runtime_identity
variant.model.artifact_sha256
variant.execution.context
variant.prompt.token_ids_sha256
variant.prompt.token_count
variant.sampler.mode
```

These are a minimum reproducibility contract, not a claim that hidden machine state is perfectly controlled.

---

# Prompt identity

Prefer Experiment 57 outputs:

```
messages_sha256
chat_template_sha256
rendered_sha256
token_ids_sha256
token_count
```

The strongest comparison key is the actual token-ID identity.

---

# Model identity

Record:
- source revision;
- exact artifact SHA256;
- artifact bytes;
- quant/type.

For a model-variant experiment, declare the whole:

```
variant.model
```

block.

---

# Runtime identity

Record:
- runtime name;
- commit/version;
- backend;
- build identity if available;
- driver/runtime versions where relevant.

If comparing runtime builds, declare:

```
variant.runtime
```

and freeze model/prompt/execution protocol.

---

# Hardware comparison

If comparing GPUs:

```
intentional_variable
=
variant.hardware
```

Then:
- same model;
- same runtime capability path where technically possible;
- same prompt/workload;
- same quality protocol.

Cross-vendor comparison may necessarily change backend/runtime.

If two semantic blocks must change together because the hardware requires a different backend, this is **not** a one-variable A/B.

Treat it as:
- a system comparison;
- not a causal single-variable experiment.

Do not force it through this validator.

---

# Sampling

For model-throughput-only `llama-bench` runs, sampler may be recorded as:

```
mode = "not-applicable-model-eval"
```

For end-to-end generation, record:
- greedy/stochastic;
- temperature;
- top-k/top-p/min-p;
- seed;
- sampler chain/order if relevant.

---

# Quality identity

Quality evaluation remains in `fixed.quality_eval` for optimization A/B.

That prevents a candidate from getting a better-looking quality score by silently changing:
- corpus;
- tokenizer;
- fixtures;
- evaluation args.

---

# Evidence Packet

An Evidence Packet should contain hashes for:
- manifest;
- hardware profile;
- model artifact or recorded model SHA;
- prompt manifest;
- raw benchmark output;
- telemetry;
- quality logs;
- comparison output.

The packet index is an integrity map.

It is not a digital signature or proof that the measurements are honest.

---

# Validator semantics

PASS means:

```
required manifest fields exist
+
no placeholders
+
comparison ID matches
+
declared variable is under variant.*
+
at least one field under it changed
+
nothing outside it changed
```

PASS does **not** prove:
- thermals were identical;
- background load was identical;
- benchmark implementation is correct;
- result is statistically significant;
- quality is acceptable.

Those are separate evidence requirements.

---

# Claims to avoid

- "same command = same workload";
- "model SHA can never change in a valid A/B";
- "a validator proves benchmark truth";
- "cross-vendor system comparison is a one-variable causal test";
- "timestamps/raw-output filenames should be identical";
- "prompt text is enough; token IDs need not be frozen";

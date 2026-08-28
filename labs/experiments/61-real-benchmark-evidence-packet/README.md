# Experiment 61 — Real Benchmark / Workload Evidence Packet

硬件等级：L1/L2/L3，取决于被测机器。

## Goal

Upgrade Experiment 40 from a small A/B manifest to a complete reproducibility contract.

Final packet should connect:

```
hardware
→ runtime
→ model artifact
→ execution config
→ prompt token identity
→ sampler
→ PP/TG
→ quality evaluation
→ telemetry
→ raw evidence hashes
```

## 1. Start from template

```bash
cp manifest.template.json baseline-manifest.json
cp manifest.template.json candidate-manifest.json
```

Use one stable:
```
comparison_id
```

for both.

## 2. Fill fixed protocol

Freeze:
- PP tokens;
- TG tokens;
- repetitions/warmup;
- tokenizer identity;
- quality corpus SHA;
- fixture revision/eval args.

## 3. Fill semantic variant blocks

### Hardware
Use exact device identity and hash the profile packet.

### Runtime
Record runtime commit/version/backend/build.

### Model
Record exact:
- artifact SHA;
- bytes;
- quant;
- source revision.

### Execution
Record:
- context;
- sequences;
- offload;
- FA;
- KV types;
- split parameters;
- threads.

### Prompt
Prefer Experiment 57:
- rendered SHA;
- token-ID SHA;
- token count.

### Sampler
For real end-to-end generation, record exact sampling identity.

For a pure `llama-bench` model-eval run, use an explicit:
```
mode = "not-applicable-model-eval"
```
rather than inventing sampler settings.

## 4. Declare the intervention

Examples:

```
variant.execution.flash_attention
variant.execution.kv_k
variant.model
variant.runtime
variant.hardware
```

If multiple semantic blocks must change together, do not force the run through the one-variable validator.

Label it a system comparison.

## 5. Validate

```bash
python3 validate_manifest_ab.py \
  baseline-manifest.json \
  candidate-manifest.json
```

Save:

```
validator.txt
```

## 6. Run performance + quality

Performance:
- reuse Experiment 40.

### Recommended capture/seal path

After the manifest is filled, prefer the Intelligence capture helper for the raw performance command:

```bash
python3 ../../../tools/intelligence/capture_real_benchmark.py \
  --manifest baseline-manifest.json \
  --out-dir baseline-run \
  --include profile.txt \
  -- \
  llama-bench -m /path/to/model.gguf -p 512 -n 128 -r 5 ... -o json
```

Use the exact current `llama-bench --help` for the argv after `--`.

The helper does not invent flags. It executes the argv without a shell, preserves stdout/stderr/command identity, and builds a PACKET integrity index.

Success here is only:

```text
CAPTURE: SEALED
```

Then run `verify_real_intake.py` with canonical IDs. Only the strengthened I07/I20 gate may return `INTAKE: READY`.

For a failed benchmark, the helper preserves the evidence but returns `CAPTURE: BLOCKED`.

Prompt identity:
- reuse Experiment 57.

Quality:
- reuse Experiment 59.

## 7. Build packet index

Example:

```bash
python3 build_packet.py \
  baseline-manifest.json \
  candidate-manifest.json \
  profile.txt \
  prompt-evidence/manifest.json \
  baseline.json \
  candidate.json \
  validator.txt \
  comparison.txt \
  baseline-ppl.txt \
  candidate-ppl.txt \
  --out PACKET.json
```

Only list files that actually exist.

## 8. Fill result

Use:
`RESULT-TEMPLATE.md`

## Important

`PACKET.json` is an integrity index.

It does not prove:
- the benchmark was honestly executed;
- thermal/background state was identical;
- statistical conclusions are valid.

Those require experiment discipline and interpretation.

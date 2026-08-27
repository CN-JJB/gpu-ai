# Evidence — Experiment 22: Capstone Measure → Diagnose → One-Variable A/B

状态：stable capstone framework complete; L0 diagnosis verified; real controlled-A/B runner ready.

## Claim

> A valid optimization result requires a frozen hardware/runtime/model/workload identity, an evidence-backed bottleneck hypothesis, exactly one intentional configuration change, and raw before/after results. A negative result is still useful if the experiment is controlled.

## Stable capstone chain

```
hardware profile
→ runtime identity
→ model SHA256
→ workload identity
→ baseline PP/TG + telemetry
→ bottleneck hypothesis
→ one intentional variable
→ candidate run
→ A/B validation
→ comparison
→ interpretation
→ next experiment
```

## Experiment 39 — bottleneck diagnosis

Seven deterministic cases cover:

- TG memory-bandwidth roof;
- PP/kernel path;
- KV/context pressure;
- serving queue/slots;
- interconnect;
- prefix reuse;
- speculative opportunity.

Reference mapping was checked locally:

```
7 / 7
```

The important pedagogical rule is:

```
observed evidence
→ choose next variable
```

rather than:

```
popular optimization
→ turn it on
```

## Experiment 40 — real capstone

The real experiment records:

### Identity
- model SHA256;
- llama.cpp version/commit;
- device identity;
- PP token count;
- TG token count;
- repetitions.

### Semantic config
Examples:
- GPU layers;
- FlashAttention;
- KV types;
- context/depth;
- split mode;
- tensor split;
- threads.

### Audit command
The exact command string is kept in `command_record`.

It is **not** counted as a second semantic variable because changing one semantic option naturally changes the command line too.

## A/B validator

Expected valid output:

```
IDENTITY CHECK: PASS
ONE-VARIABLE CHECK: PASS
PLACEHOLDER CHECK: PASS
```

The validator fails if:
- model SHA changes;
- runtime changes;
- device changes;
- PP/TG/repeats change;
- more than one semantic config field changes;
- template placeholders remain.

## Validation bug caught during build

Initial manifest design stored both:
- `config.flash_attention`;
- full `config.extra_args`.

Changing FA therefore produced two apparent config differences.

The design was corrected:

```
semantic config
→ validator

command_record
→ audit only
```

Private self-check confirms the semantic diff is now exactly:

```
config.flash_attention
```

This is an example of the course applying its own experimental discipline to course tooling.

## Raw benchmark comparison

`compare_bench.py` reads llama-bench JSON/JSONL and reports:

- baseline PP;
- candidate PP;
- PP speedup;
- baseline TG;
- candidate TG;
- TG speedup.

No benchmark values ship with the experiment.

## Completion rule

Both are valid outcomes:

```
candidate improves target metric
```

or:

```
candidate is neutral/worse
```

provided the conclusion matches raw evidence.

## Learner should reject

- fastest config found = understood optimization;
- changing many settings is valid A/B;
- PP/TG can be collapsed into one score;
- 1% gain automatically proves improvement;
- negative optimization is failed learning;
- backend flag alone proves the intended kernel was used;
- one vendor telemetry command applies to all ecosystems.

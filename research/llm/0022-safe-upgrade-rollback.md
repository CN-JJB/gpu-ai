# Research Note 0022 — Safe Upgrade / Rollback Release Gates

日期：2026-08-27

## Research question

How do you upgrade a local LLM stack without turning:

```
newer
```

into:

```
better
```

by assumption?

A release can change:
- runtime binary;
- model/quant artifact;
- backend build;
- execution config;
- server scheduling config.

A safe release decision combines:

```
identity
+ readiness
+ performance
+ quality
+ serving SLO
```

and defines rollback triggers **before** interpreting the candidate result.

---

# Part I — Release identity

A release is not just a version string.

Record:

```
runtime binary SHA
model artifact SHA
launch/config hash
backend/device identity
prompt/workload identity
```

If any of these change accidentally, the experiment/release identity changed.

---

# Part II — Upgrade categories

## Runtime upgrade

Example:

```
llama.cpp commit A
→ commit B
```

Keep model/prompt/workload fixed where possible.

## Model artifact upgrade

Example:

```
Q8
→ Q4
```

This is a model semantic block change.

## Configuration upgrade

Example:

```
FlashAttention off
→ on
```

or:
```
KV f16
→ q8_0
```

## Multi-block release

A production release may change:
- runtime;
- model;
- config;

together.

That can be valid engineering, but it is no longer a clean one-variable causal A/B.

Use Slice 33 language:

```
system release comparison
```

not:
```
one-variable experiment
```

---

# Part III — Preserve baseline immutably

Do not overwrite:

```
known-good binary
known-good model
known-good config
```

in place before the candidate is proven.

Prefer:
- separate artifact paths;
- hashes;
- immutable release directories;
- versioned config.

Rollback cannot work if the baseline artifact was destroyed.

---

# Part IV — Define policy before candidate results

A release policy can contain:

```
max readiness recovery
max first-inference recovery
minimum performance
maximum quality degradation
TTFT/ITL SLO
minimum request compliance
critical fixtures must pass
```

The thresholds are project-specific.

The course does not invent universal values.

---

# Part V — Readiness gate

Candidate must:
- start;
- reach readiness;
- complete smoke inference.

Example policy:

```
ready <= 8 s
first smoke complete <= 9 s
```

A faster TG benchmark is irrelevant if the candidate cannot reliably become ready.

---

# Part VI — Performance gate

Possible candidate rules:

```
TG speedup >= 1.0×
PP speedup >= chosen target
VRAM <= budget
```

But not every release must be faster.

A security/bugfix release may be accepted with neutral/slightly lower performance if policy allows.

So performance criteria must reflect the release goal.

---

# Part VII — Quality gate

For model/numerical changes, reuse Slice 32:

```
same tokenizer
same corpus
same eval
→ PPL ratio
+ critical fixtures
```

Example:

```
candidate PPL / baseline PPL <= 1.02
critical fixtures = all pass
```

This is only an example policy.

---

# Part VIII — Serving SLO gate

Reuse Slice 34.

For an interactive release:

```
TTFT p95 <= target
SLO compliance >= target
error rate <= target
```

A candidate can improve aggregate tokens/s while violating interactive SLO.

That release should fail for the interactive workload.

---

# Part IX — Synthetic release

Baseline:

```
readiness = 5000 ms
first inference = 5800 ms
TG = 50 tok/s
PPL = 5.0
TTFT p95 = 400 ms
SLO compliance = 99.5%
```

Good candidate:

```
readiness = 5200 ms
first inference = 5900 ms
TG = 54 tok/s
PPL = 5.05
TTFT p95 = 450 ms
SLO = 99.3%
```

With example policy:
- ready <= 8000 ms;
- first inference <= 9000 ms;
- TG >= baseline;
- PPL ratio <= 1.02;
- TTFT p95 <= 500 ms;
- SLO >= 99%;

result:

```
ACCEPT
```

---

# Part X — Fast but bad candidate

Candidate:

```
TG = 60 tok/s
```

looks great.

But:

```
PPL = 5.20
PPL ratio = 1.04
TTFT p95 = 900 ms
SLO compliance = 92%
```

Result:

```
ROLLBACK
```

This is the central lesson:

```
performance win
does not override failed quality/SLO gates
```

---

# Part XI — Rollback means identity restoration

Rollback is not:

```
restart candidate
```

Rollback means restoring the known-good:
- runtime binary;
- model artifact;
- config.

Then verify:
- exact hashes/config identity;
- readiness;
- smoke inference.

Only then:

```
rollback verified
```

---

# Part XII — Rollback recovery can fail too

Possible rollback failures:
- baseline file missing;
- config overwritten;
- incompatible persisted state;
- port still occupied;
- driver/runtime environment changed;
- baseline no longer starts.

Therefore test rollback before you need it.

A backup that has never been restored is weaker evidence than a tested rollback path.

---

# Part XIII — Cache/state compatibility

Candidate releases may alter:
- prompt-cache behavior;
- slot/cache serialization;
- runtime state.

Do not assume persisted candidate state is readable by baseline runtime.

For a simple local release:
- preserve immutable artifacts;
- treat ephemeral caches as disposable unless compatibility is explicitly documented.

---

# Part XIV — Canary intuition

If multiple replicas/capacity exist:

```
small candidate traffic
→ observe gates
→ expand
```

can reduce blast radius.

For a one-GPU single-replica local system, a true no-downtime canary may not be possible.

Do not pretend the topology supports it.

You can still run an offline candidate on a different port/time window.

---

# Part XV — Rollback trigger examples

Define before candidate:

```
health deadline exceeded
smoke request fails
critical fixture fails
PPL ratio beyond budget
TTFT p95 exceeds SLO
error rate exceeds limit
unexpected model/runtime identity
```

One critical gate can be enough to reject.

Do not average unrelated failures into one score unless your policy explicitly justifies it.

---

# Part XVI — Preserve failed candidate Evidence

Rollback should restore service, not erase diagnosis.

Keep:
- candidate logs;
- manifest;
- benchmark raw output;
- quality output;
- serving trace;
- gate decision.

This enables root-cause analysis later.

Do not leave secrets/private prompts in those logs.

---

# Part XVII — Release decision states

Useful:

```
ACCEPT
ROLLBACK
BLOCKED_MISSING_EVIDENCE
ROLLBACK_FAILED
```

Avoid a vague:
```
probably okay
```

---

# Part XVIII — Real workflow

1. Freeze known-good release identity.
2. Write release policy.
3. Preserve baseline artifacts.
4. Validate candidate manifest.
5. Start candidate locally.
6. Readiness/smoke.
7. Performance A/B.
8. Quality gate.
9. Serving SLO.
10. Gate.
11. If failed: restore baseline identity.
12. Verify rollback readiness/smoke.
13. Preserve candidate Evidence.

---

# Claims to avoid

- "newer runtime is automatically better";
- "higher TG means release accepted";
- "rollback means restart";
- "same filename means same artifact";
- "quality gate can be skipped for quant/numerical changes";
- "failed candidate logs should be deleted after rollback";
- "one universal release threshold exists";
- "multi-block production upgrade is automatically a one-variable experiment";
- "a rollback path exists because old files are somewhere on disk".

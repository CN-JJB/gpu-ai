# Evidence — Experiment 40: Safe Upgrade / Rollback

状态：stable release-gate lesson complete; synthetic ACCEPT/ROLLBACK paths verified; real evidence gate hardened.

## Claim

> A local-LLM release should be accepted only after identity, readiness, performance, quality and serving-SLO gates are checked against a policy defined before candidate interpretation. Rollback is complete only after exact baseline identity is restored and readiness/smoke are re-verified.

## Release identity

A release records at least:

```
runtime SHA
model SHA
config SHA
manifest SHA
```

Same filename/port is not sufficient identity.

## Synthetic policy

Example only:

```
ready <= 8000 ms
first inference <= 9000 ms
TG speedup >= 1.0×
PPL ratio <= 1.02
critical fixtures pass
TTFT p95 <= 500 ms
SLO compliance >= 99%
```

These thresholds are project-specific teaching values, not universal recommendations.

## Experiment 74 — good candidate

Baseline:

```
TG = 50 tok/s
PPL = 5.0
TTFT p95 = 400 ms
SLO = 99.5%
```

Candidate-good:

```
TG = 54 tok/s
PPL = 5.05
TTFT p95 = 450 ms
SLO = 99.3%
```

Verified:

```
TG speedup = 1.08×
PPL ratio = 1.01
all configured gates PASS
DECISION: ACCEPT
```

## Experiment 74 — fast-but-bad candidate

Candidate:

```
TG = 60 tok/s
PPL = 5.20
TTFT p95 = 900 ms
SLO = 92%
```

Verified:

```
TG speedup = 1.20×
→ performance PASS

PPL ratio = 1.04
→ quality FAIL

TTFT p95 = 900 ms
→ latency FAIL

SLO compliance = 92%
→ SLO FAIL
```

Decision:

```
ROLLBACK
```

The rollback artifact restores the exact synthetic baseline identity and passes readiness/smoke, so:

```
ROLLBACK: VERIFIED
```

## Central result

```
faster
!= release accepted
```

Performance cannot override failed critical quality/SLO gates unless the predeclared release policy explicitly says so.

## Experiment 75

Real release gating consumes evidence from:
- Experiment 61 — manifest / A/B identity;
- Experiment 59 — quality;
- Experiment 63 — serving SLO;
- Experiment 73 — readiness/restart.

It does not install or replace a system service.

## Hardened missing-evidence behavior

The real gate blocks unresolved string placeholders.

It also validates numeric evidence so unfinished zeros cannot create divide-by-zero or fake results.

Examples:
- baseline TG must be > 0;
- baseline/candidate PPL must be > 0;
- SLO/error fractions must be in [0,1];
- policy ranges must be sane.

Incomplete evidence returns:

```
GATE: BLOCKED_MISSING_EVIDENCE
```

rather than guessing.

## Rollback semantics

A candidate failure triggers rollback only if rollback evidence is supplied.

Verified rollback requires:
1. identity block exactly equals baseline;
2. readiness within policy;
3. smoke succeeds.

```
restart
!= rollback
```

## Artifact preservation

Known-good baseline binary/model/config should not be overwritten before candidate proof.

Failed-candidate evidence should be retained for diagnosis:
- logs;
- manifests;
- performance;
- quality;
- serving traces;

with secret/private-data redaction.

## Causal boundary

A production release can validly change multiple blocks.

But:

```
runtime + model + config
```

is a system release comparison, not a one-variable causal A/B.

Release acceptance and causal attribution are separate questions.

## Learner should reject

- newer means better;
- higher TG means release accepted;
- rollback means restart;
- same filename means same artifact;
- missing evidence can be assumed good;
- quality can be skipped for quant/numerical changes;
- failed-candidate evidence should be deleted after rollback;
- multi-block release automatically proves which change caused the result.

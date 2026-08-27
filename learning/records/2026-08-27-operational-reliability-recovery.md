# Learning / Build Record — 2026-08-27 Operational Reliability / Recovery

## Slice

39 — Liveness/readiness, restart recovery, cold/warm state and configuration identity.

## Production output

Research:
- `research/llm/0021-operational-reliability-recovery.md`

Reference:
- `reference/llm/operational-reliability-recovery.md`

Lesson:
- `lessons/39-operational-reliability/01-readiness-restart-recovery.html`

Labs:
- `labs/experiments/72-lifecycle-readiness-model/`
- `labs/experiments/73-real-local-restart-readiness/`

Evidence:
- `examples/evidence/experiment-39-operational-reliability-recovery.md`

## Verified L0

Cold:
```
HTTP 400 ms
ready 5000 ms
first inference 5800 ms
warm 150 ms
```

Restart:
```
HTTP 450 ms
ready 5100 ms
first inference 6300 ms
warm 160 ms
```

Synthetic only.

## Real-lab safety

Experiment 73:
- loopback forced;
- hidden LLAMA_ARG_* overrides removed;
- model/network/auth/tools overrides forbidden;
- only own child process is terminated.

## Stable skill

Learner can now define recovery as:
```
identity preserved
+
ready again
+
smoke inference succeeds
```

instead of checking only PID/port.

## Next

Safe upgrade / rollback:
- baseline release identity;
- candidate runtime/model/config;
- readiness;
- performance;
- quality;
- serving SLO;
- rollback trigger;
- rollback verification.

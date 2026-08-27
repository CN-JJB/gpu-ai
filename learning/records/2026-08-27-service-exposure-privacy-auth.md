# Learning / Build Record — 2026-08-27 Service Exposure / Privacy / Auth

## Slice

38 — Defensive service exposure, authentication/TLS boundaries, endpoint/privacy audit and model-license separation.

## Production output

Research:
- `research/llm/0020-service-exposure-privacy-auth.md`

Reference:
- `reference/llm/service-exposure-privacy-auth.md`

Lesson:
- `lessons/38-service-exposure/01-bind-auth-tls-privacy.html`

Labs:
- `labs/experiments/70-service-exposure-config-linter/`
- `labs/experiments/71-real-service-exposure-audit/`

Evidence:
- `examples/evidence/experiment-38-service-exposure-privacy-auth.md`

## Verified L0 result

Loopback synthetic config:
- local trust assumption only.

Wildcard synthetic config:
- no-auth HIGH;
- no-TLS REVIEW;
- metrics/slots REVIEW;
- prompt logging PRIVACY.

## Safety guard

Real endpoint probe is hard-limited to:
```
127.0.0.1 / localhost / ::1
```

and never prints API keys or response bodies.

## Stable skill

Learner can separate:
```
listen scope
authentication
TLS
CORS
endpoint exposure
logs/privacy
tool capability
model licensing
```

without making public exposure part of the course lab.

## Next

Operational reliability:
- process lifecycle;
- readiness vs liveness;
- model-load/warmup state;
- crash/restart evidence;
- graceful shutdown/drain;
- cold-start recovery time;
- configuration persistence.

# Operational Reliability / Recovery Card

## Startup states

```
spawn
→ first HTTP/listener
→ /health 200
→ smoke inference succeeds
→ warm steady state
```

Record all separately.

## Pinned llama-server health

```
503 = Loading model
200 = model loaded / ready
```

## Identity after restart

- server binary SHA/version:
- model SHA:
- launch args/config:
- backend/device:
- context/KV/slots:

## Recovery metrics

- first HTTP after spawn:
- readiness after spawn:
- first inference complete:
- first-request latency:
- warm-request latency:

## Stop semantics

- stop admission?:
- in-flight drained?:
- process signal:
- interrupted requests:
- exit code:

## Cache

Assume process-local:
- KV;
- prompt cache;
- runtime warm state;

are cold after restart unless exact persistence/restore evidence exists.

## Never equate

```
process alive
=
port listening
=
ready
=
warm
```

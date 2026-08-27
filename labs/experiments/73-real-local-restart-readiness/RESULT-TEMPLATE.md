# Result — Experiment 73

## Identity

- server binary:
- server SHA:
- model:
- model SHA before:
- model SHA after:
- exact extra args:
- device/backend:

## Cold start

- first HTTP:
- health transitions:
- readiness:
- first smoke inference duration:
- first inference complete after spawn:
- exit code:
- forced kill?:

## Restart

- first HTTP:
- health transitions:
- readiness:
- first smoke inference duration:
- first inference complete after spawn:
- exit code:
- forced kill?:

## Delta

- readiness delta:
- smoke latency delta:
- identity unchanged?:

## Warm-state note

- prefix/KV cache expected cold after restart?:
- explicit persistence/restore used?:
- warm steady-state measurement added?:

## Drain semantics

- new traffic stopped before shutdown?:
- in-flight requests drained?:
- evidence:
- note: default lab stops only while idle.

## Recovery target

Defined before interpretation:
- readiness target:
- first-inference target:

Measured:
- PASS/FAIL:

## Diagnosis

If recovery is slow/fails, separate:
- model I/O/load;
- GPU allocation;
- backend init;
- first-inference cold cost;
- port conflict;
- runtime/model identity mismatch.

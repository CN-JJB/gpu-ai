# Spec 0045 — Intelligence packet-bound used-GPU acceptance artifact

Status: implemented in I44.

## Problem

Experiment 38 requires condition evidence C3/C4, but the Intelligence lane has no machine-readable used-GPU acceptance artifact.

Experiments 86/87 already define a stable ACCEPT / REVIEW / REJECT teaching model.

I44 machineizes that existing model without inventing a C-grade mapping.

## Input case

I44 adds an Intelligence case template compatible with the Experiment 86 fields and adds:
- `hardware_id`;
- explicit `synthetic` boolean;
- schema version.

The case records:
- claimed vs observed VRAM;
- driver recognition;
- target runtime recognition;
- sustained workload completion;
- TG first/last;
- uncorrectable error telemetry or null when unsupported;
- PCIe capability/current/expected width and under-load state;
- display requirement/test state.

## PACKET binding

The case must be indexed in a packet-schema-v1 `PACKET.json`.

I44 verifies every indexed file:
- stays inside the packet directory;
- exists;
- matches byte count;
- matches SHA256.

The case itself must be covered.

This binds the machine summary to an auditable evidence packet but does not prove the packet content is truthful.

## Decision semantics

I44 mirrors Experiment 86:
- major VRAM mismatch → REJECT;
- driver/runtime not recognized → REJECT;
- sustained workload not completed → REJECT;
- uncorrectable errors >0 → REJECT;
- PCIe anomalies → REVIEW;
- >15% sustained TG decline → REVIEW;
- required display output untested → REVIEW;
- otherwise ACCEPT.

Unsupported uncorrectable-error telemetry remains explicit null/info, not fake zero.

## Reproducible artifact

The output records:
- decision;
- exact info/review/reject reasons;
- case SHA/bytes;
- PACKET SHA/bytes;
- hardware_id;
- synthetic flag;
- acceptance model contract.

An independent verifier rebuilds the entire object and requires exact equality.

## C-grade boundary

The artifact always states:

~~~text
condition_grade_mapping = UNDEFINED
~~~

I44 does **not** claim:
- ACCEPT = C3;
- ACCEPT = C4;
- REVIEW = any C grade.

That mapping does not yet have a stable machine contract in the course.

## Trust boundary

This is a packet-bound reproducible teaching acceptance decision, not a GPU health certificate or purchase recommendation.

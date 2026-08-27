# Result — Experiment 81

## Artifact identity

- model path:
- model bytes:
- trusted pre-existing SHA:
- was a new full hash run before timing?:
- runtime SHA:
- load mode:
- device/offload:

## Cache-state evidence

### Before
- fincore available?:
- raw fincore file:
- resident pages/bytes if confidently parsed:
- initial cache state:
  - KNOWN PARTIAL/FULL/LOW
  - UNKNOWN

### After read pass
- raw fincore:
- interpretation:

## File read

- bytes/pass:
- block:
- pass 1 MiB/s:
- label: initial-state-unknown
- pass 2 MiB/s:
- label: after-same-file-read
- ratio:
- note about read probe warming cache:

## Server startup

### First measured start
- first HTTP:
- health ready:
- first inference complete:

### Restart after same-model access
- first HTTP:
- health ready:
- first inference complete:

## Steady inference

- PP:
- TG:
- workload manifest:
- same model/config?:

## Diagnosis

Which stage appears material?
- storage/page faults:
- host/backend init:
- device upload:
- first-inference cold work:
- unknown:

## Claims

Supported:
-

Not supported:
-

## Hardware decision

Would faster storage improve:
- startup:
- first inference:
- steady PP:
- steady TG:

Evidence:

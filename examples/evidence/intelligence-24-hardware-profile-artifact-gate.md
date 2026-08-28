# Evidence — Intelligence I24: Hardware Profile Artifact Gate

Date: 2026-08-28  
Status: CI verified

## Claim

A non-synthetic Experiment 61 intake can no longer satisfy `variant.hardware.profile_sha256` with an unbacked manifest string.

It must provide:

```text
--hardware-profile /path/to/profile.txt
```

and the profile artifact must both match the manifest SHA256 and be indexed by PACKET.

## Evidence chain

```text
profile.txt SHA256
↕
manifest.variant.hardware.profile_sha256
+
manifest.variant.hardware.device_identity
↕
I20 raw llama-bench gpu_info
```

I24 intentionally does not parse vendor-specific profile content.

## Dedicated self-test

The I24 fixture uses a non-synthetic catalog path and proves:

```text
missing hardware profile
→ INTAKE: BLOCKED

matching profile SHA + PACKET coverage
→ HARDWARE PROFILE status=PASS
→ INTAKE: READY

same-size wrong profile
+ freshly recomputed PACKET
→ profile SHA mismatch
→ INTAKE: BLOCKED
```

No real GPU performance is represented.

## CI

```text
workflow: Intelligence Self-Test
run #98
run id 33156607865
head 536fcf7b5857639a3c3530bdc76b294551bab222
job id 98800758535
conclusion success
```

Successful steps:

```text
Compile intelligence tools
Run intelligence self-test
Run real benchmark capture self-test
Run model artifact gate self-test
Run command-model binding self-test
Run hardware profile gate self-test
Run market refresh self-test
```

## Boundary

I24 authenticates the profile artifact named by the manifest hash.

It does not prove that every line inside the profile is truthful, nor benchmark honesty, quality, causality, or purchase suitability.

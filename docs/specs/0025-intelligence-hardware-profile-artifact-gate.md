# Spec 0025 — Hardware Profile Artifact Admission Gate

Status: implemented and CI verified  
Date: 2026-08-28

## Problem

Experiment 61 requires:

```text
variant.hardware.device_identity
variant.hardware.profile_sha256
```

I20 already cross-checks raw `llama-bench gpu_info` against manifest `device_identity`.

But `profile_sha256` was only checked for presence.

A manifest could therefore contain an arbitrary profile hash without presenting the actual hardware profile artifact.

## Decision

Strengthen:

```text
tools/intelligence/verify_real_intake.py
```

with:

```text
--hardware-profile /path/to/profile.txt
```

For non-synthetic hardware intake, this argument is required.

The verifier computes the profile SHA256 and requires:

```text
sha256(hardware-profile)
==
manifest.variant.hardware.profile_sha256
```

The hardware profile file must also be indexed by `PACKET.json` SHA256 + byte count.

## Evidence chain

The resulting hardware identity chain is:

```text
profile.txt SHA256
↕
manifest.variant.hardware.profile_sha256
+
manifest.variant.hardware.device_identity
↕
I20 raw llama-bench gpu_info
```

The profile file may come from Experiment 40 `collect-profile.sh` or another learner-owned collector.

## Vendor neutrality

I24 does not parse one vendor's profile format into another vendor's schema.

A valid profile may contain:
- NVIDIA `nvidia-smi`;
- AMD `amd-smi` / `rocminfo`;
- Apple `system_profiler`;
- Intel `sycl-ls`;
- OS/runtime/model identity evidence.

I24 only authenticates the artifact named by the manifest SHA.

## Synthetic fixture exception

An explicitly synthetic hardware record may omit the profile file only when the caller uses:

```text
--allow-synthetic
```

If a profile is supplied even for a synthetic path, its SHA is still checked.

## Failure behavior

Block intake when:
- non-synthetic hardware omits `--hardware-profile`;
- the profile path is missing/not a file;
- the SHA differs from the manifest;
- the profile is not indexed by PACKET.

A hash-consistent manifest/result/command bundle is not enough if the hardware profile artifact is absent or mismatched.

## Scope boundary

I24 proves profile-file identity, not the truthfulness of every line inside the profile.

It does not prove:
- benchmark honesty;
- thermal equivalence;
- causal validity;
- quality;
- purchase suitability.

## CI verification

```text
workflow: Intelligence Self-Test
run #98
run id 33156607865
head 536fcf7b5857639a3c3530bdc76b294551bab222
job id 98800758535
conclusion success
```

The dedicated I24 self-test proves:
- non-synthetic hardware intake without `--hardware-profile` is blocked;
- a matching profile SHA256 + PACKET entry passes;
- a same-size wrong profile remains blocked after PACKET is freshly recomputed.

Runs #94–#95 were intermediate migration heads while I22/I23 non-synthetic fixtures were being carried through the new profile requirement. Runs #96–#98 restored the full suite; #98 is the accepted I24 checkpoint.

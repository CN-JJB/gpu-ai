# Spec 0046 — Intelligence used-GPU acceptance readiness bridge

Status: implemented in I45.

## Problem

I44 creates independently reproducible used-GPU ACCEPT / REVIEW / REJECT evidence.

I43 should be able to see that evidence, but must not treat ACCEPT as Experiment 38 C3/C4 without a defined mapping contract.

## Bridge

I43 adds optional inputs:

~~~text
--used-gpu-acceptance
--used-gpu-acceptance-case
--used-gpu-acceptance-packet
~~~

All three must be supplied together.

The bridge:
1. independently reconstructs the I44 artifact;
2. requires acceptance hardware_id to equal the candidate benchmark hardware_id;
3. rejects synthetic acceptance as production evidence;
4. requires decision=ACCEPT before the used-GPU acceptance component can pass.

## Deliberate separation

I43 now has two distinct components:

~~~text
used_gpu_acceptance
condition_acceptance
~~~

A real I44 ACCEPT may satisfy only `used_gpu_acceptance`.

The separate `condition_acceptance` component remains BLOCKED because Experiment 38 requires C3/C4 and the course still has no stable machine mapping:

~~~text
ACCEPT ↔ C3/C4
~~~

I45 does not invent that mapping.

## Synthetic test

The dedicated test passes a fully reproducible synthetic I44 ACCEPT artifact.

I43 correctly:
- verifies it;
- reports decision=ACCEPT;
- blocks it as production evidence because `synthetic=true`;
- keeps the C3/C4 condition component blocked.

## Trust boundary

I45 bridges evidence availability, not grade semantics.

It does not make a purchase decision.

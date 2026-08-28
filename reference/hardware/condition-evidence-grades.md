# Condition Evidence Grades — v1

This contract was introduced in Intelligence I50 because Experiment 38 used C0–C4 without a prior stable repository definition.

The grade describes **condition-evidence provenance strength**.

It does not describe whether the GPU is healthy.

Health remains a separate result such as:

~~~text
ACCEPT
REVIEW
REJECT
~~~

## Grades

### C0 — no production-usable condition evidence

Examples:
- no condition evidence;
- unknown condition;
- synthetic fixture;
- unverifiable or broken packet.

### C1 — seller/listing claim only

Examples:
- prose claim;
- listing description;
- unbound screenshot with no independently verifiable acceptance packet.

C1 is context, not purchase-grade condition evidence.

### C2 — current external test/inspection evidence without learner-owned reproducible acceptance

Examples may include:
- current seller test video;
- platform inspection result;
- third-party test record;

when identity/scope are useful but the evidence does not satisfy the learner-owned I44 packet contract.

I50 does not currently emit C2 automatically.

### C3 — learner-owned packet-bound reproducible technical acceptance evidence

Requirements:
- Experiment 87 / I44 compatible case;
- PACKET-bound case and raw evidence;
- I44 acceptance artifact independently reproducible;
- non-synthetic evidence.

The I44 health decision can still be:

~~~text
ACCEPT
REVIEW
REJECT
~~~

All three can be strong evidence. A strong REJECT is still strong evidence that the card should not be accepted.

### C4 — C3 plus independent corroborating inspection provenance

Reserved in v1.

A future C4 producer must define:
- independent source identity;
- exact card identity linkage;
- inspection scope;
- timestamp/freshness;
- packet/hash binding where practical.

I50 does not emit C4.

## Experiment 38 rule

Experiment 38 may treat:

~~~text
C3 / C4
~~~

as sufficient **evidence strength** for its condition-evidence component.

That does not mean the card passes condition.

The separate acceptance/health result must also be considered.

## Synthetic boundary

Synthetic self-tests remain C0.

They may exercise code paths but never become purchase-grade condition evidence.

# Spec 0052 — Intelligence condition-evidence readiness bridge

Status: implemented in I51.

## Problem

I50 defines the missing C0–C4 provenance contract.

I43 can now stop hardcoding the condition component as permanently unresolved.

## Input

I43 adds:

~~~text
--condition-evidence-result
~~~

The same I44 roots are also required:

~~~text
--used-gpu-acceptance
--used-gpu-acceptance-case
--used-gpu-acceptance-packet
~~~

## Independent verification

I43 rebuilds the I50 condition artifact from the same I44 acceptance roots.

The result must:
- match candidate hardware_id;
- be non-synthetic;
- have provenance grade C3 or C4.

## Separation remains mandatory

Two I43 components remain distinct:

~~~text
used_gpu_acceptance
condition_acceptance
~~~

Examples:

~~~text
C3 + REJECT
→ condition provenance may be strong
→ used_gpu_acceptance BLOCKED
→ overall readiness BLOCKED

C3 + ACCEPT
→ both condition components may PASS
~~~

This prevents an evidence-strength grade from being confused with a health outcome.

## Synthetic boundary

Synthetic I44 evidence stays C0 and cannot satisfy the condition component.

Editing a synthetic C0 artifact to C3 is blocked by independent reconstruction.

## Trust boundary

I51 removes the last structural hardcoded evidence gap.

It still cannot produce READY-FOR-HUMAN-REVIEW without real passing evidence across every independent I43 component.

Automatic purchase remains not permitted.

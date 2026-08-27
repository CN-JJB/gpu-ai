# Expected — Experiment 92

## ACCEPT case

~~~text
FAILED GATES: -
BLOCKERS: none
IMPLIED DECISION: ACCEPT
DECLARED DECISION: ACCEPT
~~~

## REVISE case

~~~text
FAILED GATES: model_vram
BLOCKERS: none
IMPLIED DECISION: REVISE
DECLARED DECISION: REVISE
~~~

At least one revision must explicitly address model_vram and state the new evidence required.

## BLOCKED case

~~~text
psu_cables: UNKNOWN
IMPLIED DECISION: BLOCKED
DECLARED DECISION: BLOCKED
~~~

## Stable lesson

The validator must reject:
- missing material-claim evidence;
- missing evidence scope;
- an ACCEPT declaration with a required FAIL/UNKNOWN;
- a REVISE case with no revision addressing the failed gate;
- a final packet that omits explicit non-claims.

It does not verify real-world truth of the referenced evidence.
# Expected — Experiment 93

There is no universal expected machine decision.

Valid final machine decisions are:

~~~text
ACCEPT
REVISE
BLOCKED
~~~

The graduation validator independently checks packet completeness.

## Valid combinations

~~~text
MACHINE DECISION: ACCEPT
CAPSTONE COMPLETENESS: COMPLETE
~~~

~~~text
MACHINE DECISION: REVISE
CAPSTONE COMPLETENESS: COMPLETE
~~~

~~~text
MACHINE DECISION: BLOCKED
CAPSTONE COMPLETENESS: COMPLETE
~~~

All three can be valid graduation outcomes.

## Invalid example

~~~text
MACHINE DECISION: ACCEPT
CAPSTONE COMPLETENESS: INCOMPLETE
~~~

This means the linked dossier says the design is feasible, but the submitted graduation argument is not auditable enough to count as complete.

## The validator checks

- Experiment 91 identity and machine decision;
- Evidence Packet index identity;
- material-claim evidence/type/scope;
- revision quality for REVISE;
- evidence-triggered upgrade roadmap;
- at least four explicit non-claims;
- all rubric dimensions at INDEPENDENT or TRANSFER.

## The validator does not prove

- real evidence is truthful;
- the machine is universally optimal;
- future driver/runtime compatibility;
- long-term hardware reliability;
- future secondhand market price.
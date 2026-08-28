# Intelligence I28 — quality execution evidence

Date: 2026-08-28

## Gap closed

Before I28, the course could prove:
- the concrete quality corpus bytes (I26);
- the machine-readable quality identity artifact (I27).

It still could not prove that an actual quality command was bound to those artifacts.

## Added

~~~text
tools/intelligence/capture_quality_eval.py
tools/intelligence/verify_quality_execution.py
tools/intelligence/quality_execution_selftest.py
docs/specs/0029-intelligence-quality-execution-evidence.md
~~~

The capture path records exact argv, executable identity when hashable, model SHA/bytes, corpus SHA/bytes, the I27 identity artifact SHA/bytes, raw stdout/stderr and an integrity packet.

## Negative cases

The dedicated self-test checks that:
1. a command whose -f/--file path differs from --quality-corpus is rejected before launch;
2. an argv tamper remains blocked after PACKET is freshly recomputed;
3. an I27 identity-artifact tamper remains blocked after PACKET is freshly recomputed;
4. a non-zero quality command preserves evidence but returns BLOCKED.

## Synthetic-only test boundary

The self-test uses a tiny fake perplexity executable and tiny fixture files.

Those values are test fixtures only. They are not real GPU/model PPL measurements and must never be promoted into the production benchmark catalog.

## Result semantics

~~~text
QUALITY CAPTURE: SEALED
!=
QUALITY EXECUTION: PASS
!=
quality metric correctness
!=
purchase recommendation
~~~

## CI verification

~~~text
workflow: Intelligence Self-Test
run #134
run id: 33158569119
head: 10e93deada5af2e0b72a8b22c5ee38c34c22b2f8
job id: 98807199018
conclusion: success
~~~

The job explicitly passed:
- Compile intelligence tools;
- Run quality identity gate self-test;
- Run quality execution self-test;
- Run market refresh self-test.


# Expected — Experiment 38

The template row should produce:

```text
NEEDS EVIDENCE
```

because:
- hard gates are UNKNOWN;
- market evidence is M0;
- condition is C0;
- max sticker is unset/zero.

A BUY-CANDIDATE in the legacy CSV evaluator requires:
- FIT PASS;
- SOFTWARE PASS;
- PERFORMANCE PASS;
- market evidence M2/M3;
- condition evidence C3/C4;
- current market evidence;
- ask <= personal max sticker.

Phase 4 now defines C0–C4 explicitly in `reference/hardware/condition-evidence-grades.md`.

C3/C4 are evidence-provenance strength, not health outcomes.

For the Intelligence path, a used card also needs a separate I44 ACCEPT result.

Freshness is now a decision gate.

```text
CURRENT
→ may continue through the remaining gates

DUE-TODAY
STALE
UNKNOWN
INVALID
→ NEEDS EVIDENCE
```

If `revalidate_after` is present, it is authoritative.

If it is absent, the evaluator retains the older fallback:

```text
observed_at age > 7 days
→ STALE
```

A stale row must not print BUY-CANDIDATE.

The script still does not purchase or contact a seller.

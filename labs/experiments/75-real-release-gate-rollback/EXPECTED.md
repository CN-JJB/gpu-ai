# Expected — Experiment 75

No universal real release decision.

A valid ACCEPT requires all configured gates to pass.

A valid ROLLBACK requires:
1. candidate gate failure;
2. exact baseline identity restored;
3. rollback readiness;
4. rollback smoke success.

Missing evidence must produce:

```
BLOCKED_MISSING_EVIDENCE
```

rather than guessing.

A faster candidate can still be rejected.

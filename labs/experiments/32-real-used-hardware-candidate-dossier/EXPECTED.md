# Expected — Experiment 32

The untouched `candidate-template.json` should output:

```
decision_status: NEEDS EVIDENCE
```

because critical identity/workload/support fields are intentionally null.

That is the correct behavior.

The tool must never invent:
- VRAM；
- seller condition；
- benchmark；
- backend support；
- price。

When all hard-gate fields are filled, the script may output:
- SKIP / CHANGE WORKLOAD；
- NEEDS SOFTWARE DECISION；
- NEEDS EVIDENCE；
- READY FOR SCENARIO DECISION。

It intentionally never outputs BUY automatically.

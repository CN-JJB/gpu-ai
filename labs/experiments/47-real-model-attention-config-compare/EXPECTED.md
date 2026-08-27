# Expected — Experiment 47

No universal model result.

A valid comparison must preserve:
- same requested context;
- same KV precision;
- same sequence count.

The tool should make it obvious that:
```
parameter count alone
```
cannot determine:
```
KV cache cost
```

If architecture caveats are present, they must be investigated before treating the homogeneous KV estimate as exact.

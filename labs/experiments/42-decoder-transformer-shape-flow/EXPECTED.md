# Expected — Experiment 42

Default run should include:

```text
SYNTHETIC TOY MODEL

=== prefill ===
X       [1,8,16]
Q       [1,4,8,4]
K       [1,2,8,4]
V       [1,2,8,4]
scores  [1,4,8,8] (conceptual)
score elements: 256

=== KV ===
KV bytes/token across all layers: 64
KV bytes after prompt: 512

=== one-token decode ===
X_new    [1,1,16]
Q_new    [1,4,1,4]
K_new    [1,2,1,4]
V_new    [1,2,1,4]
K cache  [1,2,9,4] per layer after append
V cache  [1,2,9,4] per layer after append
scores   [1,4,1,9] (conceptual)
score elements: 36
KV bytes after append: 576
```

Rough projection counts:

```
attention Q/K/V/O baseline: 768
gated MLP 3-matrix baseline: 1536
```

All values are synthetic.

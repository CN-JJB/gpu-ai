# Expected — Experiment 44

Default values are approximately:

```
RMS(x) ≈ 2.738613
RMSNorm(x)
≈ [0.365148, -0.730297, 1.095445, -1.460593]
```

The mean is not zero:

```
≈ -0.182574
```

For 3x, normalized values should be nearly identical, with only tiny epsilon-related difference.

LayerNorm-style output mean should be approximately zero.

## Lesson

```
RMSNorm
!=
LayerNorm without parameters
```

It is a different normalization rule.

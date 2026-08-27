# Expected — Experiment 45

Expected structural result:

```
||q|| == ||R(p)q||
||k|| == ||R(s)k||
```

within floating-point error.

Also:

```
dot1
≈
dot2
```

when both q/k positions are shifted by the same amount.

```
|dot1-dot2|
```

should be close to floating-point zero.

When only the key position changes:

```
dot3 != dot1
```

for the default vectors.

## Lesson

Base RoPE attention geometry encodes relative position through paired rotations.

This does not imply full-model shift invariance.

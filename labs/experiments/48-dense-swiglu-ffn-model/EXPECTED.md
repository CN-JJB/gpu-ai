# Expected — Experiment 48

Default:

```
attention Q/K/V/O: 67,108,864
SwiGLU gate/up/down: 135,266,304
FFN / attention ratio: 2.015625
attention + FFN: 202,375,168
across 32 layers: 6,476,005,376
```

FP16 FFN storage/layer:

```
270,532,608 bytes
258.0000 MiB
```

Weight-only AI proxy:

```
prefill M=512, 16-bit → 512 FLOP/weight-byte
decode M=1, 16-bit   → 1 FLOP/weight-byte
```

With:

```bash
--weight-bits 4.5
```

FFN storage/layer should be:

```
76,087,296 bytes
72.5625 MiB
```

All are formula outputs, not real hardware traffic measurements.

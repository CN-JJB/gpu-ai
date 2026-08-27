# Expected — Experiment 46

Default:

```
L=32
d=4096
Hq=32
Dh=128
KV=16 bits
context=32768
```

Expected:

| type | Hkv | group | KV/token | KV total | attention params/layer |
|---|---:|---:|---:|---:|---:|
| MHA | 32 | 1 | 512 KiB | 16 GiB | 67,108,864 |
| GQA-8 | 8 | 4 | 128 KiB | 4 GiB | 41,943,040 |
| MQA | 1 | 32 | 16 KiB | 0.5 GiB | 34,603,008 |

All values are synthetic formula outputs.

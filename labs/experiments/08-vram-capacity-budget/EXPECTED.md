# Expected result

Verified for the built-in abstract demo.

Run:

```bash
python budget.py --demo
```

Expected:

```text
Abstract 7B-like GQA demo; not a real checkpoint/runtime guarantee.
7B params, 4.5 effective bpw, 32 layers, 32 Q heads, 8 KV heads, head_dim=128, FP16 KV, context=4096, reserve=1.5 GiB, VRAM=8 GiB

 conc    weights         KV    reserve      total   headroom   status
------------------------------------------------------------------------
    1     3.667G     0.500G     1.500G     5.667G     2.333G    ROOMY
    2     3.667G     1.000G     1.500G     6.167G     1.833G    ROOMY
    4     3.667G     2.000G     1.500G     7.167G     0.833G    ROOMY
    8     3.667G     4.000G     1.500G     9.167G    -1.167G     OVER

KV architecture comparison @ 4096 tokens, FP16, 32 layers:
  type  kv heads    KiB/token   GiB/seq
--------------------------------------------
   MHA        32        512.0     2.0000
   GQA         8        128.0     0.5000
   MQA         1         16.0     0.0625
```

## Interpretation

### Weight baseline

```text
7e9 × 4.5 / 8 / 1024³
= 3.667 GiB
```

### GQA KV per token

```text
2
× 32 layers
× 8 KV heads
× 128 head_dim
× 2 bytes
= 131072 bytes
= 128 KiB
```

### At 4096 tokens

```text
128 KiB × 4096
= 512 MiB
= 0.5 GiB
```

### Concurrency

4 active sequences:

```text
0.5 GiB × 4 = 2 GiB KV
```

8 active sequences:

```text
0.5 GiB × 8 = 4 GiB KV
```

## Why concurrency=4 is still not “guaranteed fit”

The baseline leaves about 0.833 GiB on an 8 GiB target.

Real runtime can use more because of:

- weight conversion/layout；
- workspace；
- temporary activations；
- allocator fragmentation；
- preallocated paged/static KV pool；
- GPU runtime/context；
- other processes。

The exercise requires a real runtime test before claiming compatibility.

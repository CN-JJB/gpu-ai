# Expected — Experiment 41

There is no universal PASS output.

## Valid preflight

A valid vendor run records both:

```
vendor runtime/device identity
+
llama.cpp device identity
```

Examples:

### NVIDIA
`nvidia-smi` sees GPU but llama.cpp shows no CUDA device:
```
NOT READY
```

### AMD
`rocminfo` shows gfx target but exact GPU requires community override:
```
READY only if the learner explicitly accepts community-enabled support
```

### Apple
Apple Silicon + system memory detected but llama.cpp build lacks Metal:
```
NOT READY for Metal capstone
```

### Intel
`sycl-ls` has Level Zero GPU but llama.cpp SYCL device is absent:
```
NOT READY
```

Preflight failure is useful evidence.

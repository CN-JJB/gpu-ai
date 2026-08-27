# llama.cpp Model Load Mode Snapshot — 2026-08-27

Pinned upstream:

```
repo: ggml-org/llama.cpp
commit: d7a2074112d27649303fa107eb8c94db1ee435f3
```

This file records **dynamic CLI facts**, not stable course theory.

## Current server flags

Pinned `tools/server/README.md` documents:

```
-lm, --load-mode MODE
```

default:

```
auto
```

Current listed modes:

```
auto
none
mmap
mlock
mmap+mlock
dio
```

Current descriptions summarize:

- `auto`: mmap unless a device does not support it;
- `none`: no special loading mode;
- `mmap`: memory-map model;
- `mlock`: keep model in RAM rather than swapping/compressing;
- `mmap+mlock`: mmap plus memory locking;
- `dio`: use DirectIO if available.

## Deprecated compatibility flags

Current docs mark these as deprecated in favor of `--load-mode`:

```
--mlock
--mmap / --no-mmap
-dio / --direct-io
-ndio / --no-direct-io
```

Pinned `common/arg.cpp` also warns when old loading flags and `--load-mode` are combined; the last command-line flag wins.

## Dynamic-fact rule

Before a real lab:

```
llama-server --help
```

must be treated as the source of truth for the installed build.

Do not assume this 2026-08-27 flag surface is permanent.

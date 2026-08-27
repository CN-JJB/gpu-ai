# Experiment 81 — Real Read-Only Storage / Model-Startup Evidence

硬件等级：L1/L2。

## Goal

Collect evidence for:

```
file/cache behavior
vs
llama-server startup readiness
```

without globally dropping page cache.

## Safety

This lab:
- reads an existing regular model file;
- never modifies the model;
- does not call `drop_caches`;
- does not use `posix_fadvise(DONTNEED)`;
- does not change mount/storage settings;
- uses Experiment 73 for a loopback child server.

The read probe itself **does change page-cache state**.

## 1. Before hashing

If you want to study initial startup/cache behavior, do not first run a fresh full-file SHA merely for this experiment.

Hashing reads the artifact and can warm page cache.

Use an already-recorded trusted SHA from prior Evidence where possible.

## 2. Bounded read probe

Default reads the first:

```
512 MiB
```

twice:

```bash
python3 file_read_probe.py /path/to/model.gguf
```

Custom bounded size:

```bash
python3 file_read_probe.py MODEL.gguf \
  --bytes 1073741824
```

Whole file only when intentional:

```bash
python3 file_read_probe.py MODEL.gguf --full
```

Labels are deliberately:

```
pass 1 = initial-state-unknown
pass 2 = after-same-file-read
```

not automatically cold/warm.

## 3. Linux file-cache evidence

If `fincore` exists, the script saves raw:

```
fincore --json --output-all MODEL
```

before and after reads.

This is evidence of Linux file-page residency.

It is not:
- SSD controller-cache evidence;
- GPU-residency evidence;
- proof that storage is the startup bottleneck.

If unavailable, record UNKNOWN.

## 4. Startup/restart

Run Experiment 73 with the same exact model.

Current pinned load-mode example:

```bash
--extra-arg=-lm
--extra-arg=mmap
```

but first confirm:

```
llama-server --help
```

because load-mode flags are dynamic runtime facts.

Experiment 73 already records:
- binary SHA;
- model SHA;
- first HTTP;
- health ready;
- first smoke;
- restart.

## 5. Join evidence

```bash
python3 summarize.py \
  file-read-probe.json \
  ../73-real-local-restart-readiness/restart-evidence/restart-result.json
```

## 6. Interpret

Allowed:

```
second read/start was faster after prior same-model access
```

Not justified without stronger evidence:

```
SSD bandwidth = second-pass MiB/s
first run was cold
startup gain came only from disk
```

## 7. Steady-state control

After startup, measure PP/TG separately.

If:
- startup changes;
- TG is unchanged;

that is evidence that storage/loading and steady decode are different bottlenecks.

## Complete

Use:
`RESULT-TEMPLATE.md`.

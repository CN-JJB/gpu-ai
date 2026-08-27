#!/usr/bin/env python3
import argparse
import contextlib
import json
import time

import torch
import torch.nn.functional as F

try:
    from torch.nn.attention import SDPBackend, sdpa_kernel
except Exception as e:
    raise SystemExit(f"current torch.nn.attention API unavailable: {e}")

def dtype_from_name(name):
    return {
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "float32": torch.float32,
    }[name]

def backend_ctx(name):
    if name == "auto":
        return contextlib.nullcontext()
    if name == "math":
        return sdpa_kernel(SDPBackend.MATH)
    if name == "flash":
        return sdpa_kernel(SDPBackend.FLASH_ATTENTION)
    raise ValueError(name)

def run_once(q, k, v, backend, causal):
    with backend_ctx(backend):
        return F.scaled_dot_product_attention(q, k, v, dropout_p=0.0, is_causal=causal)

def bench_backend(q, k, v, backend, causal, warmup, reps, reference):
    for _ in range(warmup):
        out = run_once(q, k, v, backend, causal)
    torch.cuda.synchronize()

    torch.cuda.reset_peak_memory_stats()
    base = torch.cuda.memory_allocated()

    t0 = time.perf_counter()
    out = None
    for _ in range(reps):
        out = run_once(q, k, v, backend, causal)
    torch.cuda.synchronize()
    dt = time.perf_counter() - t0

    peak = torch.cuda.max_memory_allocated()
    peak_delta = max(0, peak - base)
    err = None
    if reference is not None and out is not None:
        err = (out.float() - reference.float()).abs().max().item()

    return {
        "mean_ms": dt * 1000.0 / reps,
        "peak_delta_mib": peak_delta / (1024**2),
        "max_abs_error_vs_math": err,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seq", type=int, nargs="+", default=[512, 1024, 2048])
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--heads", type=int, default=8)
    p.add_argument("--dim", type=int, default=64)
    p.add_argument("--dtype", choices=["float16","bfloat16","float32"], default="float16")
    p.add_argument("--warmup", type=int, default=3)
    p.add_argument("--reps", type=int, default=20)
    p.add_argument("--causal", action="store_true")
    p.add_argument("--backends", nargs="+", default=["math","flash","auto"])
    a = p.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("torch.cuda.is_available() is false; this real GPU experiment needs a CUDA/HIP-visible GPU")

    device = torch.device("cuda")
    dtype = dtype_from_name(a.dtype)

    meta = {
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "hip_version": torch.version.hip,
        "device": torch.cuda.get_device_name(0),
        "dtype": a.dtype,
        "batch": a.batch,
        "heads": a.heads,
        "dim": a.dim,
        "causal": a.causal,
        "warmup": a.warmup,
        "reps": a.reps,
    }

    results = []
    for n in a.seq:
        torch.manual_seed(0)
        q = torch.randn(a.batch, a.heads, n, a.dim, device=device, dtype=dtype)
        k = torch.randn_like(q)
        v = torch.randn_like(q)

        reference = None
        ref_error = None
        try:
            reference = run_once(q, k, v, "math", a.causal)
            torch.cuda.synchronize()
        except Exception as e:
            ref_error = repr(e)

        for backend in a.backends:
            row = {
                "seq": n,
                "backend": backend,
                "status": "ok",
                "reference_math_error": ref_error,
            }
            try:
                stats = bench_backend(
                    q, k, v, backend, a.causal,
                    a.warmup, a.reps, reference
                )
                row.update(stats)
                row["sequence_per_second_proxy"] = n / (stats["mean_ms"] / 1000.0)
            except Exception as e:
                row["status"] = "unsupported_or_error"
                row["error"] = repr(e)
                try:
                    torch.cuda.empty_cache()
                except Exception:
                    pass
            results.append(row)

        del q, k, v, reference
        torch.cuda.empty_cache()

    print(json.dumps({"meta": meta, "results": results}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

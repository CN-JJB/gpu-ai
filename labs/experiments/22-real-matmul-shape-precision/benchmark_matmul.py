#!/usr/bin/env python3
import argparse
import json
import time
import torch

def dtype_obj(name):
    return {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }[name]

def bench_one(m, n, k, dtype, warmup, reps):
    device = torch.device("cuda")
    a = torch.randn(m, k, device=device, dtype=dtype)
    b = torch.randn(k, n, device=device, dtype=dtype)

    for _ in range(warmup):
        c = a @ b
    torch.cuda.synchronize()

    t0 = time.perf_counter()
    c = None
    for _ in range(reps):
        c = a @ b
    torch.cuda.synchronize()
    dt = time.perf_counter() - t0

    mean_s = dt / reps
    ops = 2.0 * m * n * k
    tflops = ops / mean_s / 1e12
    checksum = float(c.float().mean().item())
    return {
        "mean_ms": mean_s * 1000.0,
        "tflops": tflops,
        "checksum_mean": checksum,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--prefill-m", type=int, default=512)
    p.add_argument("--decode-m", type=int, default=1)
    p.add_argument("--n", type=int, default=4096)
    p.add_argument("--k", type=int, default=4096)
    p.add_argument("--warmup", type=int, default=5)
    p.add_argument("--reps", type=int, default=20)
    p.add_argument("--dtypes", nargs="+", default=["float32","float16","bfloat16"])
    p.add_argument("--fp32-precision", choices=["highest","high","medium"], default="highest")
    a = p.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("GPU not visible through torch.cuda namespace")

    torch.set_float32_matmul_precision(a.fp32_precision)

    meta = {
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda,
        "hip_version": torch.version.hip,
        "device": torch.cuda.get_device_name(0),
        "fp32_matmul_precision": torch.get_float32_matmul_precision(),
        "warmup": a.warmup,
        "reps": a.reps,
    }

    profiles = [
        ("prefill_like", a.prefill_m, a.n, a.k),
        ("decode_like", a.decode_m, a.n, a.k),
    ]

    rows = []
    for profile, m, n, k in profiles:
        for name in a.dtypes:
            row = {
                "profile": profile,
                "m": m, "n": n, "k": k,
                "dtype": name,
                "status": "ok",
            }
            try:
                row.update(bench_one(
                    m, n, k, dtype_obj(name),
                    a.warmup, a.reps
                ))
            except Exception as e:
                row["status"] = "unsupported_or_error"
                row["error"] = repr(e)
                try:
                    torch.cuda.empty_cache()
                except Exception:
                    pass
            rows.append(row)

    print(json.dumps({"meta": meta, "results": rows}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()

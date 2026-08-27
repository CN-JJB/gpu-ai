#!/usr/bin/env python3
try:
    import mlx
    import mlx.core as mx
except Exception as e:
    print(f"MLX unavailable: {e!r}")
    raise SystemExit(0)

print("mlx module version:", getattr(mlx, "__version__", "<not exposed>"))
try:
    print("default_device:", mx.default_device())
except Exception as e:
    print("default_device error:", repr(e))

for label, device in [("cpu", mx.cpu), ("gpu", mx.gpu)]:
    try:
        print(f"{label}.count:", mx.device_count(device))
    except Exception as e:
        print(f"{label}.count error:", repr(e))
    try:
        print(f"{label}.info:", mx.device_info(device))
    except Exception as e:
        print(f"{label}.info error:", repr(e))

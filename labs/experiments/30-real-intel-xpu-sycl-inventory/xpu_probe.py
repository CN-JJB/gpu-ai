#!/usr/bin/env python3
try:
    import torch
except Exception as e:
    print("PyTorch unavailable:", repr(e))
    raise SystemExit(0)

print("torch:", torch.__version__)
print("has torch.xpu:", hasattr(torch, "xpu"))

if not hasattr(torch, "xpu"):
    raise SystemExit(0)

try:
    available = torch.xpu.is_available()
except Exception as e:
    print("torch.xpu.is_available error:", repr(e))
    raise SystemExit(0)

print("torch.xpu.is_available:", available)
if not available:
    raise SystemExit(0)

try:
    count = torch.xpu.device_count()
except Exception as e:
    print("device_count error:", repr(e))
    raise SystemExit(0)

print("device_count:", count)
for i in range(count):
    try:
        print(f"device[{i}].name:", torch.xpu.get_device_name(i))
    except Exception as e:
        print(f"device[{i}].name error:", repr(e))
    try:
        props = torch.xpu.get_device_properties(i)
        print(f"device[{i}].properties:", props)
    except Exception as e:
        print(f"device[{i}].properties error:", repr(e))
    try:
        print(f"device[{i}].memory_used:", torch.xpu.memory_allocated(i))
    except Exception as e:
        print(f"device[{i}].memory_used error:", repr(e))

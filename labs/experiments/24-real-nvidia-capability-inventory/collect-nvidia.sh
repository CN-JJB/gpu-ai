#!/usr/bin/env bash
set -u

echo "=== date ==="
date -Is 2>/dev/null || date

echo
echo "=== uname ==="
uname -a || true

echo
echo "=== nvidia-smi version ==="
nvidia-smi --version 2>&1 || true

echo
echo "=== name + compute capability ==="
nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader 2>&1 || true

echo
echo "=== selected inventory ==="
nvidia-smi --query-gpu=name,uuid,driver_version,memory.total,pci.bus_id,pstate,power.limit,pcie.link.gen.current,pcie.link.width.current --format=csv 2>&1 || true

echo
echo "=== topology ==="
nvidia-smi topo -m 2>&1 || true

echo
echo "=== full query ==="
nvidia-smi -q 2>&1 || true

echo
echo "=== optional PyTorch ==="
python3 - <<'PY'
try:
    import torch
    print("torch:", torch.__version__)
    print("torch.version.cuda:", torch.version.cuda)
    print("cuda available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(i, torch.cuda.get_device_name(i), torch.cuda.get_device_capability(i))
        try:
            print("compiled arch list:", torch.cuda.get_arch_list())
        except Exception as e:
            print("get_arch_list:", repr(e))
except Exception as e:
    print("PyTorch unavailable:", repr(e))
PY

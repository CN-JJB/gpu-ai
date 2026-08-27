#!/usr/bin/env bash
set -u

echo "=== date ==="
date -Is 2>/dev/null || date

echo
echo "=== uname ==="
uname -a || true

echo
echo "=== PCI display devices ==="
if command -v lspci >/dev/null 2>&1; then
  lspci -nn | grep -Ei 'VGA|3D|Display' || true
else
  echo "lspci: not available"
fi

echo
echo "=== amd-smi ==="
if command -v amd-smi >/dev/null 2>&1; then
  amd-smi --help 2>&1 | sed -n '1,220p' || true
  echo
  amd-smi version 2>&1 || true
  echo
  amd-smi list 2>&1 || true
  echo
  amd-smi static 2>&1 || true
  echo
  amd-smi topology 2>&1 || true
else
  echo "amd-smi: not available"
fi

echo
echo "=== rocminfo ==="
if command -v rocminfo >/dev/null 2>&1; then
  rocminfo 2>&1 || true
else
  echo "rocminfo: not available"
fi

echo
echo "=== hipconfig ==="
if command -v hipconfig >/dev/null 2>&1; then
  hipconfig --full 2>&1 || true
else
  echo "hipconfig: not available"
fi

echo
echo "=== optional PyTorch ==="
python3 - <<'PY'
try:
    import torch
    print("torch:", torch.__version__)
    print("torch.version.cuda:", torch.version.cuda)
    print("torch.version.hip:", torch.version.hip)
    print("torch.cuda.is_available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        for i in range(torch.cuda.device_count()):
            print(i, torch.cuda.get_device_name(i))
except Exception as e:
    print("PyTorch unavailable:", repr(e))
PY

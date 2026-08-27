#!/usr/bin/env bash
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== date ==="
date -Is 2>/dev/null || date

echo
echo "=== uname ==="
uname -a || true

echo
echo "=== Intel display PCI devices ==="
if command -v lspci >/dev/null 2>&1; then
  lspci -nn | grep -Ei 'VGA|3D|Display|Intel.*graphics' || true
fi

echo
echo "=== oneAPI compiler ==="
if command -v icpx >/dev/null 2>&1; then
  icpx --version || true
else
  echo "icpx: unavailable"
fi

echo
echo "=== SYCL devices ==="
if command -v sycl-ls >/dev/null 2>&1; then
  sycl-ls 2>&1 || true
else
  echo "sycl-ls: unavailable"
fi

echo
echo "=== OpenCL devices ==="
if command -v clinfo >/dev/null 2>&1; then
  clinfo -l 2>&1 || true
else
  echo "clinfo: unavailable"
fi

echo
echo "=== torch.xpu ==="
python3 "$DIR/xpu_probe.py" 2>&1 || true

echo
echo "=== llama.cpp devices ==="
if command -v llama-bench >/dev/null 2>&1; then
  llama-bench --version 2>&1 || true
  llama-bench --list-devices 2>&1 || true
else
  echo "llama-bench: unavailable"
fi

if command -v llama-ls-sycl-device >/dev/null 2>&1; then
  echo
  llama-ls-sycl-device 2>&1 || true
else
  echo "llama-ls-sycl-device: unavailable"
fi

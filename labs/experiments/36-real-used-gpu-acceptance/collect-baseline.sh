#!/usr/bin/env bash
set -u

echo "=== timestamp ==="
date -Is 2>/dev/null || date

echo
echo "=== system ==="
uname -a || true

echo
echo "=== PCI display devices ==="
if command -v lspci >/dev/null 2>&1; then
  lspci -nn | grep -Ei 'VGA|3D|Display' || true
else
  echo "lspci unavailable"
fi

echo
echo "=== NVIDIA ==="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi -L || true
  nvidia-smi --query-gpu=name,uuid,serial,memory.total,vbios_version,pci.bus_id,driver_version,temperature.gpu,power.draw,pstate --format=csv 2>&1 || true
  echo
  nvidia-smi -q 2>&1 || true
else
  echo "nvidia-smi unavailable"
fi

echo
echo "=== AMD ==="
if command -v amd-smi >/dev/null 2>&1; then
  amd-smi version 2>&1 || true
  amd-smi list 2>&1 || true
  amd-smi static 2>&1 || true
else
  echo "amd-smi unavailable"
fi

if command -v rocminfo >/dev/null 2>&1; then
  echo
  rocminfo 2>&1 || true
fi

echo
echo "=== Intel/SYCL ==="
if command -v sycl-ls >/dev/null 2>&1; then
  sycl-ls 2>&1 || true
else
  echo "sycl-ls unavailable"
fi

echo
echo "=== llama.cpp devices ==="
if command -v llama-bench >/dev/null 2>&1; then
  llama-bench --version 2>&1 || true
  llama-bench --list-devices 2>&1 || true
else
  echo "llama-bench unavailable"
fi

echo
echo "=== recent kernel GPU errors (best effort) ==="
if command -v journalctl >/dev/null 2>&1; then
  journalctl -k -b --no-pager 2>/dev/null | grep -Ei 'NVRM|Xid|amdgpu|GPU reset|device lost|i915|xe.*error|AER' | tail -n 250 || true
elif command -v dmesg >/dev/null 2>&1; then
  dmesg 2>/dev/null | grep -Ei 'NVRM|Xid|amdgpu|GPU reset|device lost|i915|xe.*error|AER' | tail -n 250 || true
else
  echo "no journalctl/dmesg"
fi

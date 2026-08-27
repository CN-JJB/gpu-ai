#!/usr/bin/env bash
set -u

echo "=== date ==="
date -Is 2>/dev/null || date

echo
echo "=== uname ==="
uname -a || true

echo
echo "=== PCI tree ==="
if command -v lspci >/dev/null 2>&1; then
  lspci -tv || true
  echo
  lspci | grep -Ei 'VGA|3D|Display' || true
else
  echo "lspci: not available"
fi

echo
echo "=== NVIDIA ==="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi -L || true
  echo
  nvidia-smi topo -m || true
  echo
  nvidia-smi topo -p2p p || true
  echo
  nvidia-smi topo -p2p n || true
else
  echo "nvidia-smi: not available"
fi

echo
echo "=== AMD / ROCm ==="
if command -v rocminfo >/dev/null 2>&1; then
  rocminfo | sed -n '1,220p' || true
else
  echo "rocminfo: not available"
fi

if command -v amd-smi >/dev/null 2>&1; then
  echo
  echo "--- amd-smi version/help ---"
  amd-smi version || true
  amd-smi --help | sed -n '1,220p' || true
else
  echo "amd-smi: not available"
fi

echo
echo "=== llama-bench ==="
if command -v llama-bench >/dev/null 2>&1; then
  llama-bench --version 2>&1 || true
  llama-bench --list-devices 2>&1 || true
else
  echo "llama-bench: not available in PATH"
fi

echo
echo "=== optional peer bandwidth tools ==="
for cmd in nvbandwidth TransferBench; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "$cmd: $(command -v "$cmd")"
  else
    echo "$cmd: not available"
  fi
done

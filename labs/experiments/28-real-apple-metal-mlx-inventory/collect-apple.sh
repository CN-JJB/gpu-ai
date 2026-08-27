#!/usr/bin/env bash
set -u

DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== date ==="
date -Is 2>/dev/null || date

echo
echo "=== macOS ==="
sw_vers 2>&1 || true
uname -a 2>&1 || true
uname -m 2>&1 || true

echo
echo "=== hardware ==="
system_profiler SPHardwareDataType SPDisplaysDataType 2>&1 || true

echo
echo "=== total memory ==="
sysctl hw.memsize 2>&1 || true

echo
echo "=== vm_stat ==="
vm_stat 2>&1 || true

echo
echo "=== memory_pressure ==="
if command -v memory_pressure >/dev/null 2>&1; then
  memory_pressure 2>&1 | sed -n '1,120p' || true
else
  echo "memory_pressure: unavailable"
fi

echo
echo "=== Metal inventory ==="
if command -v xcrun >/dev/null 2>&1; then
  xcrun swift "$DIR/metal_inventory.swift" 2>&1 || true
else
  echo "xcrun: unavailable"
fi

echo
echo "=== MLX inventory ==="
python3 "$DIR/mlx_probe.py" 2>&1 || true

echo
echo "=== llama.cpp / Metal ==="
if command -v llama-bench >/dev/null 2>&1; then
  llama-bench --version 2>&1 || true
  llama-bench --list-devices 2>&1 || true
else
  echo "llama-bench: unavailable"
fi

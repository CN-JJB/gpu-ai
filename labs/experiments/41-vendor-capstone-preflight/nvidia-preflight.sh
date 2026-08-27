#!/usr/bin/env bash
set -u
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"

echo "=== NVIDIA preflight ==="
date -Is 2>/dev/null || date

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi -L || true
  nvidia-smi --query-gpu=name,compute_cap,driver_version,memory.total,pci.bus_id --format=csv 2>&1 || true
else
  echo "FAIL: nvidia-smi unavailable"
fi

echo
echo "=== llama.cpp ==="
"$LLAMA_BENCH" --version 2>&1 || true
"$LLAMA_BENCH" --list-devices 2>&1 || true

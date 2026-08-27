#!/usr/bin/env bash
set -u
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"

echo "=== Intel preflight ==="
date -Is 2>/dev/null || date

if command -v sycl-ls >/dev/null 2>&1; then
  sycl-ls 2>&1 || true
else
  echo "FAIL: sycl-ls unavailable"
fi

if command -v llama-ls-sycl-device >/dev/null 2>&1; then
  echo
  llama-ls-sycl-device 2>&1 || true
else
  echo "llama-ls-sycl-device unavailable"
fi

echo
echo "=== llama.cpp ==="
"$LLAMA_BENCH" --version 2>&1 || true
"$LLAMA_BENCH" --list-devices 2>&1 || true

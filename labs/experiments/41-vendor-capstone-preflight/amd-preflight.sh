#!/usr/bin/env bash
set -u
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"

echo "=== AMD preflight ==="
date -Is 2>/dev/null || date

if command -v amd-smi >/dev/null 2>&1; then
  amd-smi version 2>&1 || true
  amd-smi list 2>&1 || true
  amd-smi static 2>&1 || true
else
  echo "amd-smi unavailable"
fi

if command -v rocminfo >/dev/null 2>&1; then
  echo
  echo "=== rocminfo gfx targets ==="
  rocminfo 2>&1 | grep -E '\bgfx[0-9a-z]+\b' | sort -u || true
else
  echo "FAIL: rocminfo unavailable"
fi

if command -v hipconfig >/dev/null 2>&1; then
  echo
  hipconfig --full 2>&1 || true
else
  echo "FAIL: hipconfig unavailable"
fi

echo
echo "=== llama.cpp ==="
"$LLAMA_BENCH" --version 2>&1 || true
"$LLAMA_BENCH" --list-devices 2>&1 || true

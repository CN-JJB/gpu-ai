#!/usr/bin/env bash
set -u

LLAMA_CLI="${LLAMA_CLI:-llama-cli}"
MODEL="${MODEL:-}"

echo "=== timestamp ==="
date -Is 2>/dev/null || date

echo
echo "=== OS ==="
uname -a || true

if command -v lscpu >/dev/null 2>&1; then
  echo
  echo "=== CPU ==="
  lscpu || true
elif command -v sysctl >/dev/null 2>&1; then
  echo
  echo "=== CPU ==="
  sysctl -n machdep.cpu.brand_string 2>/dev/null || true
fi

echo
echo "=== memory ==="
if command -v free >/dev/null 2>&1; then
  free -h || true
elif command -v sysctl >/dev/null 2>&1; then
  sysctl hw.memsize 2>/dev/null || true
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  echo
  echo "=== NVIDIA ==="
  nvidia-smi -L || true
  nvidia-smi --query-gpu=name,driver_version,memory.total,power.limit --format=csv,noheader || true
fi

if command -v rocminfo >/dev/null 2>&1; then
  echo
  echo "=== ROCm device summary ==="
  rocminfo 2>/dev/null | grep -E '^[[:space:]]*(Name:|Marketing Name:)' | head -n 20 || true
fi

echo
echo "=== llama.cpp ==="
"$LLAMA_CLI" --version 2>&1 || true

echo
echo "=== llama.cpp devices ==="
"$LLAMA_CLI" --list-devices 2>&1 || true

if [[ -n "$MODEL" && -f "$MODEL" ]]; then
  echo
  echo "=== model artifact ==="
  echo "path: $MODEL"

  if stat --version >/dev/null 2>&1; then
    stat -c 'bytes: %s' "$MODEL" || true
  else
    stat -f 'bytes: %z' "$MODEL" 2>/dev/null || true
  fi

  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$MODEL"
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$MODEL"
  else
    echo "SHA256 tool not found"
  fi
else
  echo
  echo "MODEL is unset or file not found; skipping artifact hash."
fi

#!/usr/bin/env bash
set -u

MODEL="${MODEL:-}"
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"

echo "=== timestamp ==="
date -Is 2>/dev/null || date

echo
echo "=== OS ==="
uname -a || true

echo
echo "=== system memory ==="
if command -v free >/dev/null 2>&1; then
  free -h || true
elif command -v sysctl >/dev/null 2>&1; then
  sysctl hw.memsize 2>/dev/null || true
fi

echo
echo "=== NVIDIA ==="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi -L || true
  nvidia-smi --query-gpu=name,uuid,driver_version,memory.total,power.limit,pci.bus_id --format=csv 2>&1 || true
  nvidia-smi topo -m 2>&1 || true
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
  rocminfo 2>/dev/null | grep -E '^[[:space:]]*(Name:|Marketing Name:)' | head -n 40 || true
fi

echo
echo "=== Apple ==="
if command -v system_profiler >/dev/null 2>&1; then
  system_profiler SPHardwareDataType SPDisplaysDataType 2>&1 || true
fi

echo
echo "=== Intel / SYCL ==="
if command -v sycl-ls >/dev/null 2>&1; then
  sycl-ls 2>&1 || true
else
  echo "sycl-ls unavailable"
fi

echo
echo "=== llama.cpp ==="
"$LLAMA_BENCH" --version 2>&1 || true
"$LLAMA_BENCH" --list-devices 2>&1 || true

echo
echo "=== model artifact ==="
if [[ -n "$MODEL" && -f "$MODEL" ]]; then
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
    echo "SHA256 tool unavailable"
  fi
else
  echo "MODEL unset or file missing"
fi

#!/usr/bin/env bash
set -u

OUT="${1:-evidence-hardware}"
mkdir -p "$OUT"

{
  echo "date: $(date -Iseconds 2>/dev/null || date)"
  uname -a 2>/dev/null || true
} > "$OUT/host.txt"

if command -v lspci >/dev/null 2>&1; then
  lspci -nnk > "$OUT/lspci-nnk.txt" 2>&1 || true
  lspci -vv > "$OUT/lspci-vv.txt" 2>&1 || true
else
  echo "lspci unavailable" > "$OUT/lspci-unavailable.txt"
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi -L > "$OUT/nvidia-smi-L.txt" 2>&1 || true
  nvidia-smi -q > "$OUT/nvidia-smi-q.txt" 2>&1 || true
  nvidia-smi topo -m > "$OUT/nvidia-smi-topo.txt" 2>&1 || true
else
  echo "nvidia-smi unavailable" > "$OUT/nvidia-smi-unavailable.txt"
fi

if command -v amd-smi >/dev/null 2>&1; then
  amd-smi version > "$OUT/amd-smi-version.txt" 2>&1 || true
  amd-smi list > "$OUT/amd-smi-list.txt" 2>&1 || true
  amd-smi static > "$OUT/amd-smi-static.txt" 2>&1 || true
  amd-smi metric --pcie > "$OUT/amd-smi-pcie.txt" 2>&1 || true
  amd-smi metric --ecc > "$OUT/amd-smi-ecc.txt" 2>&1 || true
  amd-smi bad-pages > "$OUT/amd-smi-bad-pages.txt" 2>&1 || true
else
  echo "amd-smi unavailable" > "$OUT/amd-smi-unavailable.txt"
fi

if command -v dmesg >/dev/null 2>&1; then
  # Read only; may be permission-restricted. Keep failure as evidence.
  dmesg 2>&1 | grep -Ei 'NVRM|Xid|amdgpu|pcie|aer|gpu' > "$OUT/kernel-gpu-filtered.txt" || true
fi

cat > "$OUT/collector-note.txt" <<'EOF'
Read-only collection only.
No firmware flash, OC/UV, power/fan changes, error injection or destructive VRAM stress performed.
Unsupported telemetry is UNKNOWN/N/A, not zero.
EOF

echo "wrote $OUT"

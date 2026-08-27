#!/usr/bin/env bash
set -u

echo "=== listener inventory (read-only) ==="
echo "date: $(date -Iseconds 2>/dev/null || date)"

if command -v ss >/dev/null 2>&1; then
  echo
  echo "--- ss -ltnp ---"
  ss -ltnp 2>&1 || true
elif command -v lsof >/dev/null 2>&1; then
  echo
  echo "--- lsof TCP LISTEN ---"
  lsof -nP -iTCP -sTCP:LISTEN 2>&1 || true
else
  echo "Neither ss nor lsof is available."
fi

echo
echo "No firewall/router/NAT setting was changed."
echo "Do not paste secrets or raw Authorization headers into Evidence."

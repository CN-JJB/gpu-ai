#!/usr/bin/env bash
set -u
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"

echo "=== Apple preflight ==="
date -Is 2>/dev/null || date
sw_vers 2>&1 || true
uname -m 2>&1 || true
system_profiler SPHardwareDataType SPDisplaysDataType 2>&1 || true
sysctl hw.memsize 2>&1 || true

echo
echo "=== llama.cpp ==="
"$LLAMA_BENCH" --version 2>&1 || true
"$LLAMA_BENCH" --list-devices 2>&1 || true

echo
echo "For recommendedMaxWorkingSetSize/threadExecutionWidth use Experiment 28."

#!/usr/bin/env bash
set -eu

MODEL="${MODEL:?set MODEL=/path/to/model.gguf}"
OUT="${OUT:?set OUT=baseline.json or candidate.json}"
LLAMA_BENCH="${LLAMA_BENCH:-llama-bench}"
PP="${PP:-512}"
TG="${TG:-128}"
REPEATS="${REPEATS:-5}"
EXTRA_ARGS="${EXTRA_ARGS:-}"

echo "=== capstone benchmark ==="
echo "MODEL=$MODEL"
echo "OUT=$OUT"
echo "PP=$PP"
echo "TG=$TG"
echo "REPEATS=$REPEATS"
echo "EXTRA_ARGS=$EXTRA_ARGS"
echo
echo "Confirm current CLI options with: $LLAMA_BENCH --help"
echo

# EXTRA_ARGS is intentionally shell-split so current llama-bench flags can be supplied.
# Record the exact string in the manifest.
# shellcheck disable=SC2086
"$LLAMA_BENCH"   -m "$MODEL"   -p "$PP"   -n "$TG"   -r "$REPEATS"   $EXTRA_ARGS   -o json > "$OUT"

echo "wrote: $OUT"

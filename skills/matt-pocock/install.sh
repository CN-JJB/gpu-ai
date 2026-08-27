#!/usr/bin/env bash
set -euo pipefail
AGENT="${1:-codex}"
SCOPE="${2:-project}"
scope_args=()
if [[ "$SCOPE" == "global" ]]; then scope_args=(-g); elif [[ "$SCOPE" != "project" ]]; then echo "Usage: $0 [agent] [project|global]"; exit 2; fi
mapfile -t SKILLS < <(grep -v '^$' "$(dirname "$0")/manifest/stable-skills.txt")
args=()
for skill in "${SKILLS[@]}"; do args+=(--skill "$skill"); done
npx skills@latest add mattpocock/skills "${args[@]}" --agent "$AGENT" --copy -y "${scope_args[@]}"

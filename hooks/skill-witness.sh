#!/bin/bash
# Witness mesh: validate debate output structure before Claude stops
INPUT=$(cat)
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
[[ "$STOP_HOOK_ACTIVE" == "true" ]] && exit 0

MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // empty')
[[ -z "$MSG" ]] && exit 0

# Only check debate skill output (Phase/Round markers present)
echo "$MSG" | grep -qE "Phase 0|Round 1|Evidence Base" || exit 0

MISSING=""
echo "$MSG" | grep -q "Evidence Base" || MISSING+="Evidence Base, "
echo "$MSG" | grep -qE "KEPT|STRENGTHENED|CUT" || MISSING+="Component Ledger, "
echo "$MSG" | grep -q '"witness"' || MISSING+="Witness Block, "

if [[ -n "$MISSING" ]]; then
  echo "⚠ Skill output missing: ${MISSING%, }. Add before concluding." >&2
  exit 2
fi
exit 0

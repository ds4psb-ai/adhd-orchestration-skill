#!/bin/bash
# Witness mesh: validate Explore agent produces ≥3 findings
INPUT=$(cat)
MSG=$(echo "$INPUT" | jq -r '.last_assistant_message // empty')
[[ -z "$MSG" ]] && exit 0

# Count findings (lines starting with - or * or numbered)
FINDING_COUNT=$(echo "$MSG" | grep -cE '^\s*[-*]|^\s*[0-9]+\.' || true)

if [[ "$FINDING_COUNT" -lt 3 ]]; then
  echo "⚠ Explore agent produced $FINDING_COUNT findings (minimum 3). Expand investigation." >&2
  exit 2
fi
exit 0

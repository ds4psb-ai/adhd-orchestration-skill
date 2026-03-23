#!/bin/bash
# ADHD Orchestration Skill — One-liner installer for Claude Code
# Usage: bash <(curl -fsSL https://raw.githubusercontent.com/ds4psb-ai/adhd-orchestration-skill/main/install.sh)
set -euo pipefail

REPO="ds4psb-ai/adhd-orchestration-skill"
BRANCH="main"
BASE="https://raw.githubusercontent.com/$REPO/$BRANCH"

info()  { printf "\033[1;34m→\033[0m %s\n" "$1"; }
ok()    { printf "\033[1;32m✓\033[0m %s\n" "$1"; }
fail()  { printf "\033[1;31m✗\033[0m %s\n" "$1" >&2; exit 1; }

# Pre-flight
command -v curl >/dev/null 2>&1 || fail "curl is required"
[[ -d .git ]] || fail "Run this from a git repository root"

info "Installing ADHD Orchestration Skills into $(pwd)/.claude/"

# Create directories
mkdir -p .claude/skills/{adhd,tkm,tk,tkc,tktk,verify-implementation/scripts,manage-skills/scripts}
mkdir -p .claude/{commands,hooks,reports}

# Download skills
SKILLS=(adhd tkm tk tkc tktk)
for skill in "${SKILLS[@]}"; do
  curl -fsSL "$BASE/skills/$skill.md" -o ".claude/skills/$skill/SKILL.md"
done
curl -fsSL "$BASE/skills/verify-implementation.md" -o ".claude/skills/verify-implementation/SKILL.md"
ok "Skills: adhd, tkm, tk, tkc, tktk, verify-implementation"

# Download scripts
curl -fsSL "$BASE/scripts/run_registry_checks.py"  -o ".claude/skills/verify-implementation/scripts/run_registry_checks.py"
curl -fsSL "$BASE/scripts/skill_registry_sync.py"   -o ".claude/skills/manage-skills/scripts/skill_registry_sync.py"
ok "Scripts: run_registry_checks.py, skill_registry_sync.py"

# Download commands
curl -fsSL "$BASE/commands/checkpoint.md" -o ".claude/commands/checkpoint.md"
ok "Commands: checkpoint"

# Download hooks
curl -fsSL "$BASE/hooks/skill-witness.sh"  -o ".claude/hooks/skill-witness.sh"
curl -fsSL "$BASE/hooks/explore-witness.sh" -o ".claude/hooks/explore-witness.sh"
chmod +x .claude/hooks/*.sh
ok "Hooks: skill-witness.sh, explore-witness.sh"

echo ""
ok "Installation complete!"
echo ""
echo "  Add to your CLAUDE.md:"
echo ""
echo "    ## Skills"
echo "    - /adhd — Mothership orchestrator (diagnose → route → dispatch → converge)"
echo "    - /tkm  — Parallel work package generator"
echo "    - /tk   — Claude↔Codex 2-round debate"
echo "    - /tkc  — Claude self-debate (no MCP needed)"
echo "    - /tktk — Deep 3-round research debate"
echo "    - /verify-implementation — Diff-aware verification mesh"
echo "    - /checkpoint — Session state persistence"
echo ""
echo "  Optional: install Codex CLI for dual-model debates (/tk, /tktk):"
echo "    npm install -g @openai/codex"
echo ""

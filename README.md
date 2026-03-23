# ADHD Orchestration Skill for Claude Code

> **Scatter-to-Converge**: A multi-terminal orchestration system designed for developers with ADHD who build excellent skeletons across parallel sessions but struggle with completion.

**Author**: [ds4psb-ai](https://github.com/ds4psb-ai/)
**License**: MIT
**Platform**: [Claude Code](https://claude.com/claude-code) (Anthropic CLI)
**Models**: Claude Opus 4.6 (lead) + GPT-5.4 via Codex CLI (challenger, optional)

---

## What This Is

A 5-layer skill system for Claude Code that turns ADHD-style scattered parallel work into structured, convergent execution. The mothership (`/adhd`) never implements code itself — it **diagnoses** domain health, **traces** dependencies, **distributes** work across N terminal sessions, and **verifies** convergence.

### The Problem It Solves

High-intelligence ADHD developers build great foundations across 4+ parallel sessions, but:
- Checkpoints stall at 40-80%
- Hotfix chains emerge instead of completing features
- Downstream integration gets missed
- Phase 1 ships without Phase 2+

### The Solution

```
/adhd vdg embedding    →  Deep diagnosis → N conflict-free work packages → N terminals → git-based convergence
```

## Architecture — 5-Layer Stack

```
Layer 0: State Harness      — hooks + witness mesh + JSON state + SHA tracking + observability
Layer 1: ADHD Router        — diagnose / route / dispatch / converge (thin, never implements)
Layer 2: Reasoning Skills   — TKM / TKC / TK / TKTK (each sovereign, dual-mode)
Layer 3: Persistence        — checkpoint + run manifest + stream state + convergence
Layer 4: Verification Mesh  — verify-implementation (diff-aware registry) + domain verifiers
```

## Skill Inventory

| Skill | File | Role | Standalone? |
|-------|------|------|-------------|
| **ADHD** | `skills/adhd.md` | Mothership orchestrator: diagnose → route → dispatch → converge | YES |
| **TKM** | `skills/tkm.md` | Decompose problems into N conflict-free parallel work packages | YES |
| **TK** | `skills/tk.md` | 2-round Claude↔Codex debate with SoTA probe + Position Lock | YES (requires Codex MCP) |
| **TKC** | `skills/tkc.md` | Context-isolated self-debate with persona inversion + bias audit | YES (no MCP needed) |
| **TKTK** | `skills/tktk.md` | 3-round deep research debate with inter-round investigation | YES (requires Codex MCP) |
| **Verify** | `skills/verify-implementation.md` | Diff-aware dynamic check registry with Before/After revalidation | YES |
| **Checkpoint** | `commands/checkpoint.md` | Session state persistence with SHA-based staleness tracking | YES |

### Sovereignty Protocol

Every sub-skill passes the Sovereignty Test:
1. **Callable without ADHD context** — standalone invocation produces useful output
2. **Produces useful artifact alone** — not just intermediate state
3. **Explicit I/O contract** — documented input/output
4. **Dual-mode entry** — standalone OR ADHD-routed (via `--from-run`)

## How It Works

### ADHD Protocol (4 Phases)

```
Phase A    (RECON: 3 parallel Explore agents scan git + checkpoints + code gaps)
  → Phase A.5  (DEPENDENCY DEEP-DIVE: trace upstream/downstream/cross-layer per gap)
    → Phase B    (ROUTE: Tier 2-biased — default is multi-terminal distribution)
      → Phase C    (DISPATCH: /tkm → N work packages → N terminal context packets)
        → Phase D    (CONVERGE: PULL-based git scan + verify mesh)
```

### 4-Tier Routing

| Tier | When | Action |
|------|------|--------|
| **Tier 0: Direct** | 1 gap, 1 file, mechanical | Direct fix (rare) |
| **Tier 1: Solo** | 1-2 gaps, single layer | `/tkc` or `/tk` |
| **Tier 2: Multi** (DEFAULT) | 2+ gaps | `/tkm` → N terminals |
| **Tier 3: Team** | Production incident, 10+ gaps | Agent Teams |

### Debate Skills Comparison

| Skill | Model(s) | Rounds | Time | Best For |
|-------|----------|--------|------|----------|
| `/tkc` | Claude only (self-debate) | 1 subagent | ~1-3 min | Fast structured debate, MCP unavailable |
| `/tk` | Claude + Codex | 2 rounds | ~10-18 min | Cross-model diversity, SoTA decisions |
| `/tktk` | Claude + Codex | 3 rounds | ~20-30 min | Deep root-cause, inter-round research |

### Dual-LLM Architecture (Tiki-Taka)

The debate skills exploit **cognitive diversity** from different model training:

| | Claude Opus 4.6 (Lead) | GPT-5.4 via Codex CLI (Challenger) |
|---|---|---|
| **Edge** | Orchestrated deep investigation — parallel agents, code tracing | Fresh perspective + web verification (BrowseComp 82.7%) |
| **Role** | Propose, defend, synthesize | Challenge, verify, broaden |
| **Blind spot** | Training cutoff | Single-agent, no parallel deep dives |

A turn where either model doesn't leverage its core edge is a wasted turn.

### Anti-Deflation System

All debate skills enforce aggressive scope preservation:
- **Category A** (Accept): Concrete technical flaw with proof
- **Category B** (REJECT by default): Scope reduction framed as pragmatism
- **Category C** (REJECT): Generic risk aversion
- **Position Lock**: Checkpoint between defense and synthesis prevents retroactive weakening
- **Scope Preservation Report**: Must maintain ≥70% of original proposal ambition

### Witness Mesh (Anti-Laziness Enforcement)

External hook-based validation that catches step-skipping before output reaches the user. Addresses the core problem: LLMs self-assessing compliance is like students grading their own exams.

**How it works:**

```
Debate skill runs → Claude produces output → Stop hook fires
  → skill-witness.sh checks: Evidence Base? Component Ledger? Witness Block?
    → Missing? → exit 2 (Claude forced to continue and add missing parts)
    → All present? → exit 0 (output passes)

Explore agent completes → SubagentStop hook fires
  → explore-witness.sh checks: ≥3 concrete findings?
    → <3 findings? → exit 2 (agent must expand investigation)
    → ≥3 findings? → exit 0 (agent passes)
```

**Components:**

| Component | Type | Purpose |
|-----------|------|---------|
| `skill-witness.sh` | Stop hook | Validates debate output has Evidence Base, Component Ledger, Witness Block |
| `explore-witness.sh` | SubagentStop hook | Validates Explore agents produce ≥3 concrete findings |
| Frontmatter hooks | YAML in skill files | Scopes hooks to debate skill lifecycle (not global) |
| StopFailure logging | JSONL append | Observability for API errors during skill execution |
| Exit contracts | Blockquotes | Per-phase MUST requirements summarized at each Phase header |
| Witness block | JSON template | Structured output format for machine-parseable completeness |

**Witness block format** (appended at end of debate output):
```json
{"witness":{"skill":"tk","phase":"final","components":{"C1":"KEEP","C2":"STRENGTHEN"},"incomplete":[],"scope_pct_informational":85}}
```

**Design decisions:**
- Skill-scoped frontmatter hooks (not project-global) — only fire during debate skill execution
- `stop_hook_active` guard prevents infinite loops (hook re-triggering itself)
- `scope_pct_informational` is advisory only — no hard gate without upfront component weights

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- (Optional) [Codex CLI](https://github.com/openai/codex) for dual-model debates (`/tk`, `/tktk`)

### Setup

1. Copy skills to your Claude Code project:

```bash
# Create skill directories
mkdir -p .claude/skills/{adhd,tkm,tk,tkc,tktk}
mkdir -p .claude/{commands,hooks}

# Copy skill files
cp skills/adhd.md   .claude/skills/adhd/SKILL.md
cp skills/tkm.md    .claude/skills/tkm/SKILL.md
cp skills/tk.md     .claude/skills/tk/SKILL.md
cp skills/tkc.md    .claude/skills/tkc/SKILL.md
cp skills/tktk.md   .claude/skills/tktk/SKILL.md
cp skills/verify-implementation.md .claude/skills/verify-implementation/SKILL.md
cp commands/checkpoint.md .claude/commands/checkpoint.md

# Copy verification scripts
mkdir -p .claude/skills/verify-implementation/scripts
mkdir -p .claude/skills/manage-skills/scripts
cp scripts/run_registry_checks.py .claude/skills/verify-implementation/scripts/
cp scripts/skill_registry_sync.py .claude/skills/manage-skills/scripts/

# Copy witness mesh hooks (optional but recommended)
cp hooks/skill-witness.sh  .claude/hooks/skill-witness.sh
cp hooks/explore-witness.sh .claude/hooks/explore-witness.sh
chmod +x .claude/hooks/*.sh
```

2. Register skills in your `CLAUDE.md` (or project instructions):

```markdown
## Available Skills
- `/adhd` — Mothership orchestrator for multi-terminal work
- `/tkm` — Parallel work package generator
- `/tk` — Claude↔Codex 2-round debate
- `/tkc` — Claude self-debate (no MCP needed)
- `/tktk` — Deep 3-round research debate
- `/verify-implementation` — Diff-aware verification with dynamic check registry
- `/checkpoint` — Session state persistence
```

3. (Optional) Configure Codex CLI for dual-model debates:

```bash
# Install Codex CLI
npm install -g @anthropic-ai/codex

# Configure model in ~/.codex/config.toml
# The skills will use whatever model is configured there
```

## Usage Examples

```bash
# Full domain health dashboard
/adhd

# Diagnose + route for specific domain
/adhd vdg embedding

# Convergence verification (PULL-based git scan)
/adhd verify vdg

# Standalone work package generation
/tkm "Refactor auth middleware for compliance"

# Fast self-debate (no Codex needed)
/tkc "Should we use Redis or in-memory LRU for caching?"

# Cross-model debate
/tk "Migration strategy for PostgreSQL → CockroachDB"

# Deep research debate
/tktk "Event sourcing vs CQRS for audit trail"

# Diff-aware verification (runs only checks matching changed files)
/verify-implementation

# Save session state for cross-session continuity
/checkpoint
```

## ADHD-Specific Red Flags

| Trap | Recognition | Correction |
|------|-------------|------------|
| "I'll do it all in one terminal" | 2+ gaps, not distributing | Tier 2 is DEFAULT → distribute |
| "I'll merge it later" | No checkpoint at session end | `/checkpoint` is MANDATORY |
| "Let me quickly fix this too" | Drifting to another domain | Stay on current domain |
| "It'll probably be fine" | Skipping diagnosis | RECON is mandatory |
| "This is just Tier 0" | Underestimating complexity | If uncertain → Tier 2 |
| "That's only 1 gap" | Counting by category | Count INDIVIDUAL items |

## Key Design Decisions

1. **ADHD never implements** — It's a thin router. Implementation happens in sub-skills running in separate terminals.
2. **Tier 2 is the default** — ADHD exists to distribute work. Single-terminal is the exception.
3. **PULL-based convergence** — Doesn't rely on sessions self-reporting. Scans git state directly.
4. **SHA-based staleness** — Checkpoints track git SHAs, not timestamps.
5. **Sub-skill sovereignty** — Every skill works standalone OR ADHD-routed. No lock-in.
6. **External validation over self-assessment** — Witness mesh hooks enforce output completeness externally, because LLM self-grading is unreliable (Anthropic auditing agents study: single investigator 13% → parallel auditors 42% → evaluation agent 88%).

## File Structure

```
adhd-orchestration-skill/
├── README.md                       # This file
├── skills/
│   ├── adhd.md                    # Mothership orchestrator
│   ├── tkm.md                     # Work package generator
│   ├── tk.md                      # Claude↔Codex 2-round debate
│   ├── tkc.md                     # Claude self-debate
│   ├── tktk.md                    # Deep 3-round research debate
│   └── verify-implementation.md   # Diff-aware verification mesh
├── scripts/
│   ├── run_registry_checks.py     # Execute registry checks + report
│   └── skill_registry_sync.py     # Auto-extend registry from git diff
├── hooks/
│   ├── skill-witness.sh           # Stop hook: debate output completeness
│   └── explore-witness.sh         # SubagentStop hook: ≥3 findings gate
└── commands/
    └── checkpoint.md               # Session persistence
```

## Contributing

Issues and PRs welcome at [github.com/ds4psb-ai](https://github.com/ds4psb-ai/).

## License

MIT

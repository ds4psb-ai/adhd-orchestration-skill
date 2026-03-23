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
Layer 0: State Harness    — hooks + JSON state + SHA tracking + observability
Layer 1: ADHD Router      — diagnose / route / dispatch / converge (thin, never implements)
Layer 2: Reasoning Skills  — TKM / TKC / TK / TKTK (each sovereign, dual-mode)
Layer 3: Persistence      — checkpoint + run manifest + stream state + convergence
Layer 4: Verification Mesh — verify-implementation hub + domain verifiers
```

## Skill Inventory

| Skill | File | Role | Standalone? |
|-------|------|------|-------------|
| **ADHD** | `skills/adhd.md` | Mothership orchestrator: diagnose → route → dispatch → converge | YES |
| **TKM** | `skills/tkm.md` | Decompose problems into N conflict-free parallel work packages | YES |
| **TK** | `skills/tk.md` | 2-round Claude↔Codex debate with SoTA probe + Position Lock | YES (requires Codex MCP) |
| **TKC** | `skills/tkc.md` | Context-isolated self-debate with persona inversion + bias audit | YES (no MCP needed) |
| **TKTK** | `skills/tktk.md` | 3-round deep research debate with inter-round investigation | YES (requires Codex MCP) |
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

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- (Optional) [Codex CLI](https://github.com/openai/codex) for dual-model debates (`/tk`, `/tktk`)

### Setup

1. Copy skills to your Claude Code project:

```bash
# Create skill directories
mkdir -p .claude/skills/adhd
mkdir -p .claude/skills/tkm
mkdir -p .claude/skills/tk
mkdir -p .claude/skills/tkc
mkdir -p .claude/skills/tktk
mkdir -p .claude/commands

# Copy skill files
cp skills/adhd.md   .claude/skills/adhd/SKILL.md
cp skills/tkm.md    .claude/skills/tkm/SKILL.md
cp skills/tk.md     .claude/skills/tk/SKILL.md
cp skills/tkc.md    .claude/skills/tkc/SKILL.md
cp skills/tktk.md   .claude/skills/tktk/SKILL.md
cp commands/checkpoint.md .claude/commands/checkpoint.md
```

2. Register skills in your `CLAUDE.md` (or project instructions):

```markdown
## Available Skills
- `/adhd` — Mothership orchestrator for multi-terminal work
- `/tkm` — Parallel work package generator
- `/tk` — Claude↔Codex 2-round debate
- `/tkc` — Claude self-debate (no MCP needed)
- `/tktk` — Deep 3-round research debate
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

# Save session state for cross-session continuity
/checkpoint
```

## ADHD-Specific Red Flags

| Trap | Recognition | Correction |
|------|-------------|------------|
| "한 터미널에서 다 하자" | 2+ gaps, not distributing | Tier 2 is DEFAULT → distribute |
| "나중에 합치면 되지" | No checkpoint at session end | `/checkpoint` is MANDATORY |
| "이것도 빨리 고치자" | Drifting to another domain | Stay on current domain |
| "대충 되겠지" | Skipping diagnosis | RECON is mandatory |
| "이거 Tier 0이지" | Underestimating complexity | If uncertain → Tier 2 |
| "Gap 1개네" | Counting by category | Count INDIVIDUAL items |

## Key Design Decisions

1. **ADHD never implements** — It's a thin router. Implementation happens in sub-skills running in separate terminals.
2. **Tier 2 is the default** — ADHD exists to distribute work. Single-terminal is the exception.
3. **PULL-based convergence** — Doesn't rely on sessions self-reporting. Scans git state directly.
4. **SHA-based staleness** — Checkpoints track git SHAs, not timestamps.
5. **Sub-skill sovereignty** — Every skill works standalone OR ADHD-routed. No lock-in.

## File Structure

```
adhd-orchestration-skill/
├── README.md                 # This file
├── skills/
│   ├── adhd.md              # Mothership orchestrator
│   ├── tkm.md               # Work package generator
│   ├── tk.md                # Claude↔Codex 2-round debate
│   ├── tkc.md               # Claude self-debate
│   └── tktk.md              # Deep 3-round research debate
└── commands/
    └── checkpoint.md         # Session persistence
```

## Contributing

Issues and PRs welcome at [github.com/ds4psb-ai](https://github.com/ds4psb-ai/).

## License

MIT

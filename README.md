# ADHD Orchestration Skill for Claude Code

[![ADHD Verify Pipeline](https://github.com/ds4psb-ai/adhd-orchestration-skill/actions/workflows/verify-pipeline.yml/badge.svg)](https://github.com/ds4psb-ai/adhd-orchestration-skill/actions/workflows/verify-pipeline.yml)

> **"Separating the agent doing the work from the agent judging it proves to be a strong lever."**
> — [Anthropic Engineering, Harness Design for Long-Running Apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)

A multi-terminal orchestration system that turns scattered parallel work into structured, convergent execution. The core idea: **the agent writing code never judges its own work.** A blind evaluator does. And it runs until the evaluator says PASS — then runs again, because single-pass verification misses ~30% of issues.

**Author**: [ds4psb-ai](https://github.com/ds4psb-ai/)
**License**: MIT + Attribution
**Platform**: [Claude Code](https://claude.com/claude-code) (Anthropic CLI)
**Models**: Claude Opus 4.6 (lead + evaluator) + GPT-5.4 via Codex CLI (challenger, optional)

## Quick Start

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/ds4psb-ai/adhd-orchestration-skill/main/install.sh)
```

## Philosophy

This project implements the **Generator↔Evaluator harness pattern** from Anthropic's engineering research:

1. **Generator and Evaluator are separate agents.** The generator writes code. A blind evaluator — running Opus in a fresh context with zero knowledge of the generator's reasoning — judges it. This structural separation is the single biggest lever for quality.

2. **Repetition breeds excellence.** Anthropic ran 5–15 iterations per generation, each pushing in a more distinctive direction. We adopt this: more eval rounds = higher quality output. Token cost is irrelevant. The harness runs until PASS, then runs again to catch what the first pass missed.

3. **Debate before implementation.** Every non-trivial change goes through structured debate (TKC or TK) before a single line of code is written. The debate produces a `handoff.json` contract that the execution harness consumes.

4. **Scatter-to-Converge.** ADHD developers build excellent skeletons across parallel sessions but struggle with completion. This system automates the hard parts: deep diagnosis, conflict-free work distribution across N terminals, and git-based convergence verification.

## Architecture

```
         ┌─────────┐
         │  /adhd   │  Mothership: diagnose → route → dispatch → converge
         └────┬─────┘  Never implements. Only orchestrates.
              │
         ┌────▼─────┐
         │  /tkm     │  Planner: decompose into N conflict-free work packages
         └────┬─────┘  Zero file overlap. Explicit API contracts between streams.
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
  ┌──────┐ ┌──────┐ ┌──────┐
  │ /tkc │ │ /tk  │ │ /tk  │  Debate: structured reasoning before code
  │      │ │      │ │--deep│  /tkc = self-debate, /tk = Claude↔Codex
  └──┬───┘ └──┬───┘ └──┬───┘
     │        │        │
     ▼        ▼        ▼     handoff.json (debate conclusions → execution)
  ┌──────────────────────┐
  │       /ralph          │  Execution Harness: implement + blind-evaluator loop
  │  Generator ↔ Evaluator│  Minimum 2 eval rounds. Evaluator runs Opus.
  └──────────┬───────────┘
             │
         ┌───▼────┐
         │ /adhd   │  Converge: PULL-based git scan + cross-stream eval
         │ verify  │  Graded verdict (not binary). Iterate if needed.
         └────────┘
```

### The Chain

Every task follows one path:

```
/adhd diagnose → /tkm partition → /tkc|/tk debate → /ralph implement+eval → /adhd converge
```

Each link produces a structured artifact consumed by the next:
- **TKM** → work package markdown + stream JSON contracts
- **TKC/TK** → `handoff.json` (debate conclusions, target files, acceptance criteria)
- **Ralph** → `notices.md` (completion signals for ADHD convergence)

## Skills

| Skill | What it does | Standalone? |
|-------|-------------|-------------|
| **`/adhd`** | Mothership: diagnose domain health, route to tiers, dispatch work, converge | Yes |
| **`/tkm`** | Decompose problems into N conflict-free parallel work packages | Yes |
| **`/tkc`** | Self-debate via context-isolated subagent with 6-layer debiasing | Yes |
| **`/tk`** | Claude↔Codex cross-model debate (2 rounds, or 3 with `--deep`) | Yes (needs Codex MCP) |
| **`/ralph`** | Execution harness: Generator + Blind Evaluator loop with persistent state | Yes |
| **`/verify-implementation`** | Diff-aware dynamic check registry | Yes |
| **`/checkpoint`** | Session state persistence with SHA-based staleness | Yes |

Every skill passes the **Sovereignty Test**: callable without ADHD context, produces useful output alone, documented I/O contract, dual-mode entry (standalone or ADHD-routed).

## Key Concepts

### Blind Evaluators (Opus)

The evaluator agents run **Claude Opus** in a fresh context. They have:
- Zero knowledge of the generator's reasoning chain
- Read-only access to code + test commands
- A skepticism mandate: "if you find zero issues, double-check"
- Strict output contract: PASS with evidence, or FAIL with file:line gaps

Three evaluator variants:
- `blind-evaluator` — full-stack fallback
- `blind-evaluator-be` — backend only (Python, pytest, schema)
- `blind-evaluator-fe` — frontend only (TypeScript, build, i18n)

### handoff.json — Debate-to-Execution Contract

When a debate skill (`/tkc` or `/tk`) concludes that implementation is needed, it writes a structured handoff:

```json
{
  "from_skill": "tkc",
  "debate_topic": "Redis vs in-memory LRU for session caching",
  "final_decision": "Use Redis with 5min TTL — in-memory LRU breaks under horizontal scaling",
  "target_files": ["backend/services/cache.py", "backend/config.py"],
  "acceptance_criteria": ["pytest passes", "cache hit rate ≥80% in load test"],
  "evidence_summary": "Phase 0 found 3 endpoints doing redundant DB queries...",
  "iteration_hint": "normal"
}
```

Ralph reads this on startup, pre-populates its investigation hints, then deletes it (one-shot handoff). **Ralph still runs its own full investigation** — the handoff accelerates, it doesn't bypass.

### 4-Tier Routing

| Tier | When | Action |
|------|------|--------|
| **0: Direct** | 1 gap, 1 file, mechanical | Just fix it (rare) |
| **1: Solo** | 1-2 gaps, single layer | `/tkc` or `/tk` → `/ralph` |
| **2: Multi** (default) | 2+ gaps | `/tkm` → N terminals |
| **3: Team** | Production incident | Agent Teams |

**Tier 2 is the default.** ADHD exists to distribute work. Single-terminal is the exception.

### Anti-Deflation

Debate skills enforce aggressive scope preservation:
- **Category A** (accept): concrete flaw with proof
- **Category B** (reject by default): scope reduction as pragmatism
- **Category C** (reject): generic risk aversion
- **Position Lock**: prevents retroactive weakening between defense and synthesis
- **≥70% scope preservation** or explain with Category A evidence

### Witness Mesh

External hook-based validation. Addresses the core problem: LLMs grading their own work is like students grading their own exams.

```
Skill runs → output produced → Stop hook fires → witness script checks completeness
  → Missing evidence? → exit 2 (forced to continue)
  → All present? → exit 0 (passes)
```

## Installation

### One-liner

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/ds4psb-ai/adhd-orchestration-skill/main/install.sh)
```

### Manual

```bash
# Skills
mkdir -p .claude/skills/{adhd,tkm,tk,tkc,ralph}
mkdir -p .claude/{commands,hooks,agents}

cp skills/adhd.md   .claude/skills/adhd/SKILL.md
cp skills/tkm.md    .claude/skills/tkm/SKILL.md
cp skills/tk.md     .claude/skills/tk/SKILL.md
cp skills/tkc.md    .claude/skills/tkc/SKILL.md
cp skills/ralph.md  .claude/skills/ralph/SKILL.md
cp skills/verify-implementation.md .claude/skills/verify-implementation/SKILL.md
cp commands/checkpoint.md .claude/commands/checkpoint.md

# Blind evaluator agents (Opus)
cp agents/blind-evaluator.md    .claude/agents/blind-evaluator.md
cp agents/blind-evaluator-be.md .claude/agents/blind-evaluator-be.md
cp agents/blind-evaluator-fe.md .claude/agents/blind-evaluator-fe.md

# Witness mesh hooks
cp hooks/skill-witness.sh  .claude/hooks/skill-witness.sh
cp hooks/explore-witness.sh .claude/hooks/explore-witness.sh
chmod +x .claude/hooks/*.sh
```

### Optional: Codex CLI for dual-model debates

```bash
npm install -g @openai/codex
# Configure model in ~/.codex/config.toml
```

## Usage

```bash
/adhd vdg embedding          # Diagnose + distribute work for a domain
/adhd                         # Cross-domain health dashboard
/adhd verify vdg              # Git-based convergence check

/tkm "Refactor auth middleware"  # Generate N parallel work packages
/tkc "Redis vs in-memory LRU?"  # Fast self-debate (~1-3 min)
/tk "Postgres → CockroachDB"    # Cross-model debate (~10-18 min)
/ralph "Fix auth race condition" # Execute with blind-evaluator loop

/verify-implementation           # Diff-aware verification
/checkpoint                      # Save session state
```

## File Structure

```
adhd-orchestration-skill/
├── skills/
│   ├── adhd.md              # Mothership orchestrator
│   ├── tkm.md               # Work package generator
│   ├── tk.md                # Claude↔Codex debate
│   ├── tkc.md               # Claude self-debate
│   ├── ralph.md             # Execution harness (Generator↔Evaluator)
│   └── verify-implementation.md
├── agents/
│   ├── blind-evaluator.md   # Full-stack evaluator (Opus)
│   ├── blind-evaluator-be.md # Backend evaluator (Opus)
│   └── blind-evaluator-fe.md # Frontend evaluator (Opus)
├── hooks/
│   ├── skill-witness.sh     # Debate output completeness
│   └── explore-witness.sh   # ≥3 findings gate
├── commands/
│   └── checkpoint.md
├── scripts/
│   ├── run_registry_checks.py
│   └── skill_registry_sync.py
├── examples/
│   └── sample-monorepo/
├── .github/workflows/
│   └── verify-pipeline.yml
└── install.sh
```

## Design Decisions

1. **Generator never judges its own work.** Blind evaluator with fresh context, Opus model, mandatory skepticism.
2. **Minimum 2 eval rounds.** Single-pass misses ~30%. The second round catches what the first missed.
3. **Debate produces artifacts, not just conclusions.** `handoff.json` carries structured evidence from debate into execution.
4. **PULL-based convergence.** ADHD doesn't trust sessions to self-report. It scans git state directly.
5. **Every skill is sovereign.** Works standalone or ADHD-routed. No vendor lock-in to the orchestrator.
6. **External validation > self-assessment.** Witness mesh hooks enforce output completeness because LLM self-grading is unreliable.
7. **All paths end at /ralph.** Even trivial changes get blind-evaluator verification. The harness is non-negotiable.

## Contributing

Issues and PRs welcome at [github.com/ds4psb-ai](https://github.com/ds4psb-ai/).

## License

MIT + Attribution — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

> Built with [ADHD Orchestration Skill](https://github.com/ds4psb-ai/adhd-orchestration-skill) by ds4psb-ai

---

<sub>Copyright (c) 2026 [ds4psb-ai](https://github.com/ds4psb-ai). All skill files, hooks, and scripts in this repository are watermarked with origin metadata.</sub>

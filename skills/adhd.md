---
name: adhd
description: "Mothership orchestrator: deep dependency diagnosis → Tier 2-biased multi-terminal dispatch → PULL-based convergence. Never implements — only investigates deeply, decides, distributes, and converges."
---

# ADHD vNext — Mothership Orchestration Protocol

Mothership orchestrator that deeply diagnoses domain health, traces all dependency chains, distributes work across multiple terminals via `/tkm`, and drives convergence through **adversarial Generator↔Evaluator harness loops**.

**Core principle:** ADHD is the mothership — it diagnoses, routes, dispatches, and **relentlessly evaluates**. Each stream runs `/tkc → /ralph` (debate → implement with blind-evaluator loop). ADHD Phase D then runs its own **cross-stream adversarial evaluation** — not passive git scanning, but active blind-evaluator spawning that pushes each iteration in a more distinctive direction.

**Harness Philosophy (from Anthropic Engineering, 2026-03-24):**
> "I ran 5 to 15 iterations per generation, with each iteration typically pushing
> the generator in a more distinctive direction."

Repetition is not overhead — it is the mechanism that produces excellence. Token cost is irrelevant. The harness runs until the evaluator says PASS, then runs again to find what the first pass missed. **Default is multi-terminal distribution (Tier 2). Single-terminal execution requires explicit justification.**

**Why ADHD exists:** High-intelligence ADHD developers build excellent skeletons across 4+ parallel sessions, but the flesh never fills in. Checkpoints stall at 40-80%, hotfix chains emerge, and downstream integration gets missed. ADHD automates deep diagnosis, distributes work packages across N terminals via `/tkm`, and converges results.

**MCP calls: 0** | **Subagent calls: 3-5** (Phase A+A.5) | **Output: DHR + /tkm work packages + terminal dispatch instructions**

## Harness Design Principles

> Source: Anthropic Engineering, "Harness Design for Long-Running Application Development" (2026-03-24)
> These principles govern ADHD's design decisions and Tier routing.

### P1: Component Justification
"Every component in a harness encodes an assumption about what the model can't do on
its own, and those assumptions are worth stress testing, both because they may be
incorrect, and because they can quickly go stale as models improve."
→ Each Tier level encodes an assumption about model capability. Re-evaluate after model upgrades.

### P2: Simplicity First
"Find the simplest solution possible, and only increase complexity when needed."
→ Tier 0→1→2→3 already follows this. Never escalate Tier without evidence of necessity.

### P3: Evaluation Separation
"Separating the agent doing the work from the agent judging it proves to be a strong
lever. Tuning a standalone evaluator to be skeptical turns out to be far more tractable
than making a generator critical of its own work."
→ Phase C (dispatch = work) ↔ Phase D (converge = evaluation). Never self-evaluate.
  "Out of the box, Claude is a poor QA agent" — Phase D must be skeptical by design.

### P4: Grading Over Binary
"'Is this design beautiful?' is hard to answer consistently, but 'does this follow our
principles for good design?' gives something concrete to grade against."
→ Phase D uses criteria-based grading, not pass/fail. See Graded Verdict below.

### P5: Harness Evolution
"The space of interesting harness combinations doesn't shrink as models improve.
Instead, it moves, and the interesting work for AI engineers is to keep finding
the next novel combination."
→ On model upgrade: review which Tier boundaries and guard sections are still load-bearing.
  Opus 4.6 dropped sprint decomposition. What can we drop next?

### P6: Context Management
"A reset provides a clean slate, at the cost of the handoff artifact having enough state
for the next agent to pick up the work cleanly."
→ TKM terminal packets = structured handoff (stream JSON + work package md).
  Opus 4.5+: automatic compaction handles most context growth. Reset only when needed.

### P7: Iteration Loop
"I ran 5 to 15 iterations per generation, with each iteration typically pushing the
generator in a more distinctive direction. I also instructed the generator to make a
strategic decision after each evaluation: refine the current direction if scores were
trending well, or pivot to an entirely different aesthetic if the approach wasn't working."
→ Phase D → Phase C re-dispatch loop. Iteration budget in manifest.json.
  Each cycle: score trend up → refine, score trend down → pivot (re-enter Phase B).

## Sovereignty

ADHD is the **orchestration layer** — it depends on sovereign sub-skills but never replaces them:

| Sub-Skill | Harness Role | Independent? |
|-----------|-------------|-------------|
| `/tkm` | **Planner** — decompose into work packages with output contracts | YES |
| `/tkc` | **Claude Generator↔Evaluator** — single-model debate | YES |
| `/tk` | **Cross-Model Generator↔Evaluator** — Claude↔Codex (includes --deep) | YES |
| `/checkpoint` | **State Persistence** — session progress snapshots | YES |
| `/verify-implementation` | **Verification Mesh** — test/schema/hardening gate | YES |
| `/verify-ui-consistency` | **Visual Evaluator** — screenshot/a11y/design token check | YES |

## Usage

```
/adhd <domain> [topic]         # Diagnose + route for a specific domain/topic
/adhd                          # Full domain health dashboard
/adhd verify [domain]          # PULL-based convergence verification
```

**Examples:**
```
/adhd vdg embedding            # VDG embedding domain diagnosis
/adhd frontend zodiac          # Frontend Zodiac diagnosis
/adhd                          # Cross-domain dashboard
/adhd verify vdg               # Convergence check for VDG
```

## Architecture

> **The Anthropic Harness Principle (universal — applies to ALL tasks, not just UI):**
> The adversarial Generator↔Evaluator loop is not domain-specific. It applies to:
> - **Code**: Generator writes, Evaluator checks correctness + downstream impact
> - **Architecture**: Generator proposes, Evaluator challenges feasibility + blast radius
> - **Planning**: TKM generates work packages, Evaluator audits partitions + contracts
> - **Investigation**: Explorer gathers evidence, Evaluator challenges completeness + bias
> - **Convergence**: Streams produce, Cross-stream evaluator checks integration
>
> Every phase of ADHD that produces output gets an independent evaluation pass.
> "I ran 5-15 iterations... each pushing in a more distinctive direction."

```
Phase A    (RECON: git scan + checkpoint JSON + code gaps → Domain Health Report)
  → Phase A.5  (DEPENDENCY DEEP-DIVE: trace upstream/downstream/cross-layer for each gap)
    → Phase B    (ROUTE: Tier 2-biased adaptive routing — default is multi-terminal)
      → Phase C    (DISPATCH: /tkm → /tkc → /ralph chain per stream + terminal packets)
        → Phase D    (CONVERGE: git diff + checkpoint scan + evaluator + graded verdict)
                     ↺ FAIL → re-dispatch (Phase C) with evaluator feedback
                     ✓ PASS → COMPLETE
```

### Enforcement Architecture (P8)

> Source: TKC debate 2026-03-30 — analysis of 31 ADHD runs showed 0% Phase D execution,
> 60+ ad-hoc manifest fields, 5 phantom convergences. Root cause: spec existed but
> enforcement was zero. These mechanisms make the spec executable.

**Three enforcement layers:**

1. **Phase Completion Gates** — Each phase MUST output a structured gate checklist before
   the next phase can begin. Gates are structured templates (not prose MUSTs) that the
   model fills in. Missing gate = invalid phase transition.

2. **Manifest Schema Contract** — 10 required fields, fixed enum values. Ad-hoc fields
   allowed in `extra` object only. `current_phase` + `phase_history[]` track transitions.

3. **Observability Events** — JSONL events at each phase boundary. 7 event types enable
   post-hoc analysis of routing accuracy, Phase D execution rate, and failure patterns.

**Why enforcement works in prompts (vs. prose MUSTs):**
Prose "MUST" scattered in paragraphs → ignored ~70% of the time (measured).
Structured output templates with fill-in fields → followed reliably because the model
treats them as output format instructions, not behavioral constraints.

**Stream Status Enum (fixed):**
`pending` | `active` | `complete` | `failed` — no other values permitted.

## Protocol

### Phase A — RECON (MANDATORY — take the time needed, do NOT rush)

**No routing without thorough diagnosis.** Phase A always runs. Thoroughness > speed.

Launch ≥3 Explore agents in parallel. Each agent MUST produce ≥3 concrete findings (file paths, commit hashes, or gap descriptions). Agents that return fewer than 3 findings MUST be re-prompted or supplemented.

- **Agent 1: Git History Scanner**
  ```
  - git log --oneline --grep="<domain>" -50
  - git log --oneline -30
  - git log --format="%h %ad %s" --date=short -50
  - Identify: phase-based commits, hotfix chains,
    skeleton-only features (phase 1 without phase 2+)
  ```

- **Agent 2: State Scanner**
  ```
  - memory/checkpoints/*.json  (JSON sidecars — machine-readable!)
  - memory/checkpoints/*.md    (human-readable backup)
  - memory/project_*           (project state, blockers)
  - .claude/state/adhd/runs/   (active ADHD runs if any)
  - Identify: incomplete phases, stale checkpoints, active runs
  ```

- **Agent 3: Code Gap + Dependency Scanner**
  ```
  Surface gaps:
  - NotImplementedError, raise NotImplemented  (stubs)
  - Backend endpoint without frontend consumer (or vice versa)
  - Checkpoint "Remaining" sections → verify actual state
  - Identify: upstream/downstream gaps, missing tests, dead code

  Dependency tracing (MANDATORY for each gap found):
  - import/from chains: who imports this file? what does it import?
  - Cross-layer coupling: model↔service↔router↔schema↔frontend
    If gap is in service, CHECK router + schema + frontend consumers
  - Indirect dependencies: shared config, env vars, migrations,
    translation keys, test fixtures that depend on gap code
  - Caller-callee: grep for function/class name usage across codebase
  ```

#### SHA-Based Staleness

Checkpoint staleness is determined by **code changes, not time**:

```
FRESH:  key_files unchanged since base_sha AND no new commits touching domain
STALE:  ANY key_file changed since base_sha OR import contracts changed
EXPIRED: base_sha is >50 commits behind HEAD (too much drift to trust)
```

Fallback to time-based only if JSON sidecar is missing:
| Age | Status |
|-----|--------|
| 0-3 days | Fresh |
| 4-7 days | Aging |
| 7+ days | Stale |
| 14+ days | Expired |

#### Gap Counting Rule (MUST)

Count each **individual item**, not categories.
"7 endpoints missing rate limiting" = **7 gaps**, not 1 "hardening-debt" gap.
"3 services without tests" = **3 gaps**, not 1 "test-gap" gap.
The Gap Matrix Count column MUST reflect individual item count.

#### Output: Domain Health Report (DHR)

```markdown
## Domain Health Report: <domain> [topic]
> Generated: YYYY-MM-DD HH:MM

### Skeleton Map
| Feature | Phase Done | Phase Remaining | Checkpoint | Staleness |
|---------|-----------|-----------------|------------|-----------|

### Gap Matrix
| Gap Type | Count | Items |
|----------|-------|-------|
| skeleton-only | N | ... |
| missing-downstream | N | ... |
| missing-upstream | N | ... |
| hardening-debt | N | ... |
| test-gap | N | ... |
| ui-gap | N | ... |
| stale-checkpoint | N | ... |
| **TOTAL** | **N** | **(sum of all individual items)** |

### Priority Queue
1. [CRITICAL] ...
2. [HIGH] ...
3. [MED] ...

### Rule 11 Budget
- Current session domains: <domain>
- Budget remaining: 1 more domain allowed
```

**Phase A Gate (MUST output before proceeding to A.5):**
```
┌─ PHASE A GATE ─────────────────────────────────────┐
│ Agents spawned: {N} (min 3)       ✅/❌             │
│ Findings per agent: {a1:N, a2:N, a3:N} (min 3 each)│
│ Gap count (individual items): {N}                   │
│ DHR written to: {path}                              │
│ JSONL event emitted: phase_end/A                    │
│ Gate status: PASS / FAIL — {reason if fail}         │
└─────────────────────────────────────────────────────┘
```
Emit JSONL: `{"event":"phase_end","run_id":"...","phase":"A","findings":{N},"gap_count":{N},"ts":"..."}`

**Gate FAIL → STOP. Do not proceed to Phase A.5. Re-run agents or ask user for guidance.**

### Phase A.5 — DEPENDENCY DEEP-DIVE (MANDATORY)

**After DHR generation, before routing.** For each gap in the Priority Queue:

1. **Upstream trace**: What code/service/component CALLS or IMPORTS the gap area?
   If upstream consumers exist → gap is load-bearing → severity ↑
2. **Downstream trace**: What does the gap area CALL or DEPEND ON?
   If downstream is also gapped → compound risk → severity ↑
3. **Cross-layer check**: Does the gap span multiple layers (model→service→router→frontend)?
   Multi-layer gap = multi-stream candidate, CANNOT be Tier 0
4. **Blast radius**: If this gap were fixed incorrectly, what breaks?
   High blast radius → needs debate (/tkc or /tk), not direct fix

Update the DHR Priority Queue with revised severities.
Update gap count: dependency chains may reveal **hidden gaps** not found in Phase A.

**Output: Dependency Annotation Table**
```markdown
### Dependency Annotations
| Gap | Upstream Consumers | Downstream Deps | Cross-Layer? | Blast Radius |
|-----|-------------------|-----------------|-------------|-------------|
| gap-1 | router_x, service_y | config, model_z | Yes (3 layers) | HIGH |
```

**Hard Gate**: If ANY gap has 2+ upstream consumers OR spans 2+ layers → that gap CANNOT be routed to Tier 0. Period.

**Phase A.5 Gate (MUST output before proceeding to B):**
```
┌─ PHASE A.5 GATE ───────────────────────────────────┐
│ Gaps with dependency annotations: {N}/{total}       │
│ Cross-layer gaps found: {N}                         │
│ Gaps with 2+ upstream consumers: {N}                │
│ Tier 0 eligible gaps: {N} (must be 0 if cross-layer)│
│ Updated gap count after deep-dive: {N}              │
│ Gate status: PASS / FAIL — {reason if fail}         │
└─────────────────────────────────────────────────────┘
```
Emit JSONL: `{"event":"phase_end","run_id":"...","phase":"A5","cross_layer":{N},"upstream_heavy":{N},"ts":"..."}`

### Phase B — ROUTE (Tier 2-Biased Adaptive)

**DEFAULT IS TIER 2 (multi-terminal via /tkm).** ADHD exists to distribute work. Single-terminal execution is the exception, not the rule.

Based on the DHR + Phase A.5 deep-dive:

```
Tier 2: Multi-Session (DEFAULT — the common case)
  ├── Condition: 2+ gaps (most domains hit this after honest counting)
  ├── Action: Invoke /tkm → generate N work packages → N terminals
  │   - /tkm --from-run <run-id>  (pass DHR context automatically)
  │   - Default method per package: /tkc (fast)
  │   - Upgrade to /tk if: SoTA needed, vendor/API decisions, cross-model value
  │   - Upgrade to /tk --deep if: unknown root cause, SoTA comparison needed
  ├── Downgrade to Tier 1 requires ALL FOUR conditions:
  │   □ Total gap count ≤ 2 (individual items, not categories)
  │   □ All gaps in single layer (not cross-layer per Phase A.5)
  │   □ Zero upstream consumers affected
  │   □ No architecture decision needed
  └── Ceremony: /tkm partition + N terminal dispatch packets

Tier 1: Solo (JUSTIFIED DOWNGRADE — must state why)
  ├── Condition: exactly 1-2 gaps, single layer, no upstream risk
  ├── Action: /tkc or /tk
  └── MUST output: "Tier 1 justified: [which 4 downgrade conditions are met]"

Tier 0: Direct (RARE — requires strong evidence of triviality)
  ├── Condition: exactly 1 gap, 1 file, zero dependencies, <5min mechanical fix
  ├── Action: Output direct fix instructions
  └── MUST output: "Tier 0 justified: single file, zero callers, zero cross-layer, mechanical change"

Tier 3: Team (ESCALATION for production/massive scope)
  ├── Condition: production incident, cross-domain cascade, 10+ gaps
  └── Action: /team create hotfix OR /team create feature-dev
```

**Routing Decision Table:**

| Signal | Tier 0 (RARE) | Tier 1 (JUSTIFY) | Tier 2 (DEFAULT) | Tier 3 |
|--------|---------------|------------------|------------------|--------|
| Gap count | exactly 1 | exactly 1-2 | **2+** | 10+ or production |
| Cross-layer? | No | No | **ANY** | Yes |
| Upstream consumers? | 0 | 0 | **1+** | Many |
| Justification | REQUIRED | REQUIRED | Not needed | Not needed |
| Estimated time | <5min | 5-15min | 15-60min | hours-days |

**TKM Integration (Tier 2 MUST):**
When Tier 2 is selected, ADHD MUST invoke `/tkm` to generate work packages:
1. Pass the DHR + Dependency Annotations as context
2. `/tkm` produces N conflict-free work packages with file ownership
3. ADHD formats terminal dispatch packets from /tkm output
4. Each packet includes: stream title, work package path, method (/tkc or /tk), checkpoint reminder

**Phase B Gate (MUST output before proceeding to C):**
```
┌─ PHASE B GATE ──────────────────────────────────────┐
│ Tier selected: {0|1|2|3}                            │
│ Justification: {reason}                             │
│ If Tier 0/1 — downgrade conditions:                 │
│   □ Gap count ≤ 2: {yes/no}                         │
│   □ Single layer: {yes/no}                          │
│   □ Zero upstream consumers: {yes/no}               │
│   □ No architecture decision: {yes/no}              │
│ If Tier 2 — /tkm invocation planned: {yes}          │
│ Streams planned: {N}                                │
│ Gate status: PASS / FAIL — {reason if fail}         │
└─────────────────────────────────────────────────────┘
```
Emit JSONL: `{"event":"tier_decision","run_id":"...","tier":{N},"gap_count":{N},"streams":{N},"ts":"..."}`

**Invariant: Tier 0/1 with ANY downgrade condition = "no" → Gate FAIL. Escalate to Tier 2.**

### Phase C — DISPATCH

**For Tier 0:** Output fix instructions directly. Done.

**For Tier 1:** Invoke the chosen sub-skill (/tkc or /tk). Done.

**For Tier 2 (DEFAULT):** Invoke `/tkm` → generate work packages → format terminal dispatch packets.

**For Tier 3:** `/team create` with appropriate recipe.

**Tier 2 Dispatch Protocol (MUST follow):**

**Step 0: Invoke /tkm**
```
/tkm --from-run <run-id>
```
This passes the DHR + Dependency Annotations to /tkm. /tkm handles:
- Deep investigation (Phase 1 — skipped if --from-run provides sufficient evidence)
- File ownership partitioning (Phase 2)
- Conflict audit via subagent (Phase 3)
- Work package document generation (Phase 4)

Wait for /tkm to produce N work package files before proceeding to Step 1.

**For Tier 2-3:** Generate state harness + context packets.

#### Step 1: State Harness Setup

Create run directory (if not exists):
```bash
mkdir -p .claude/state/adhd/runs/<run-id>/streams
mkdir -p .claude/state/adhd/runs/<run-id>/checkpoints
```

Write `manifest.json` (ALL 10 fields required — no exceptions):
```json
{
  "run_id": "run_<date>_<domain>",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "domain": "<domain>",
  "tier": 2,
  "base_sha": "<git HEAD>",
  "streams_count": 3,
  "status": "active",
  "current_phase": "C",
  "phase_history": [
    {"phase": "A", "ts": "...", "exit": "ok"},
    {"phase": "A5", "ts": "...", "exit": "ok"},
    {"phase": "B", "ts": "...", "exit": "ok"},
    {"phase": "C", "ts": "...", "exit": "pending"}
  ],
  "dhr_path": ".claude/state/adhd/runs/<run-id>/dhr.json"
}
```
Optional fields go in `"extra": {}` — do NOT invent top-level ad-hoc fields.

Write `dhr.json` (structured DHR for machine consumption).

TKM writes `streams/stream-N.json` with ownership, contracts, acceptance criteria.
Each stream MUST use status enum: `pending` | `active` | `complete` | `failed`.

#### Step 2: Context Packets (copy-paste ready)

```markdown
## Session Setup
This work requires N sessions.
Open N terminals and start `claude` in each one.
```

Each packet:
```markdown
<domain> Stream K — <stream title>
Work package: read <path to work package md> and begin.
Method: /tkc → /ralph (debate first, then execute with blind-evaluator loop)
After completion: run /checkpoint.

MANDATORY CHAIN: /tkc (or /tk) for design decisions → /ralph for implementation.
Ralph's blind-evaluator loop (min 2 rounds) is NON-NEGOTIABLE per stream.
Do NOT claim stream complete without Ralph PASS x2.
```

#### Step 2.5: Output Contract Reminder (NEW)

Each terminal packet ends with:
```
Output contract (MUST complete before claiming done):
1. Changed files list + rationale
2. Test evidence (pytest/bun output)
3. /checkpoint with JSON sidecar
4. notices.md append if cross-stream findings
"Done" without evidence = not done.
```

Add `iteration_budget` to manifest.json:
```json
{
  "iteration_budget": 1,
  ...
}
```

Values: 3 (default — Ralph repetition is core philosophy), 5 (complex multi-stream), unlimited (user says "완벽하게" or "토큰 무제한").

> **Core Philosophy: Repetition breeds excellence.**
> Anthropic's harness ran 5-15 iterations per generation, producing "distinctive directions."
> ADHD adopts this: more eval rounds = more diverse, higher-quality output.
> Token cost is irrelevant — correctness and completeness are the only metrics.

#### Step 3: Rule 11 Budget Check

```markdown
### Rule 11 Check
- Domain: <domain> (1/2 budget)
- ✅ Within 2-domain limit
```

If 3+ domains:
```markdown
### ⚠️ Rule 11 Warning
- Touches: <domain1> + <domain2> + <domain3>
- 3+ domains = Rule 11 exceeded. FOCUS OVERRIDE required.
```

#### Step 4: Write-Stream Topology Cap

```markdown
### Write-Stream Advisory
- Read/research terminals: unlimited
- Write streams: N (based on disjoint file ownership graph)
  - Recommended max: 4 concurrent write streams
  - Current: N streams with verified zero file overlap
```

#### Step 5: Cross-Session Notices

Create `notices.md` for inter-session signaling:
```markdown
# Cross-Session Notices: <run-id>
> Any session can append. /adhd verify reads all.

<!-- Append new notices above this line -->
```

#### Step 6: Observability

Append to `~/.claude/adhd-runs.jsonl`:
```json
{"event": "run_started", "run_id": "<id>", "domain": "<domain>", "tier": 2, "streams": 3, "base_sha": "<sha>", "timestamp": "..."}
```

**Phase C Gate (MUST output before closing dispatch session):**
```
┌─ PHASE C GATE ──────────────────────────────────────┐
│ /tkm invoked (Tier 2+): {yes/no}                    │
│ Work packages generated: {N}                        │
│ File overlap verified (disjoint): {yes/no}          │
│ Terminal packets output: {N}                        │
│ manifest.json written with 10 required fields: {yes}│
│ Convergence reminder in EVERY packet: {yes/no}      │
│ JSONL run_started emitted: {yes/no}                 │
│ Gate status: PASS / FAIL — {reason if fail}         │
└─────────────────────────────────────────────────────┘
```

**CRITICAL REMINDER in final output to user:**
```
⚡ 모든 stream 완료 후 반드시 실행:
   /adhd verify <domain>
   이걸 안 하면 convergence verification이 0% — 작업이 검증 없이 끝남.
```

### Phase D — CONVERGE (`/adhd verify`)

> Design note (TKC debate 2026-03-30): Phase D was 0/31 execution rate because it was
> too heavy (2+ blind evaluator rounds mandatory). Simplified to Quick Mode default.
> The best Phase D is one that actually runs. Full mode available via `--thorough`.

**PULL-based** — does NOT rely on sessions reporting their own completion. Scans git state directly.

**Two modes:**
- `/adhd verify <domain>` — **Quick Mode (default)**: git diff + checkpoint scan + 1 eval round + graded verdict (~3 min)
- `/adhd verify <domain> --thorough` — **Full Mode**: 2+ eval rounds + deep grading (~10 min)

#### Step 1: Re-scan (PULL from git)

```bash
git log --oneline <base_sha>..HEAD -- <all owned_files across streams>
git diff --stat <base_sha>..HEAD -- <all owned_files>
```

Read checkpoint JSON sidecars for each stream (if available).
Read `notices.md` for any inter-session signals.
Read `manifest.json` — verify `phase_history` shows A→A.5→B→C completed.

#### Step 2: Convergence Report

```markdown
## Convergence Report: <domain>

### Stream Status (PULL from git + checkpoints)
| Stream | Files Changed | Commits | Checkpoint | Status |
|--------|--------------|---------|------------|--------|

### Gaps Closed (✅)
| Gap | Closed By | Commit | Evidence |
|-----|-----------|--------|----------|

### Gaps Remaining (❌)
| Gap | Reason | Next Action |
|-----|--------|-------------|

### New Gaps Discovered (⚠️)
| Gap | Source | Priority |
|-----|--------|----------|
```

#### Step 3: Cross-Stream Evaluator (1 round for Quick, 2+ for Full)

**Quick Mode (default):** Spawn 1 blind-evaluator (backend or frontend based on domain):
```
Agent tool:
  subagent_type: blind-evaluator
  prompt: "Cross-stream convergence eval for ADHD run <run-id>.
           Read manifest at .claude/state/adhd/runs/<run-id>/manifest.json.
           For EACH stream: grep target symbols, verify acceptance criteria.
           Run: pytest --testmon -x -q (backend) or bun run build (frontend).
           Check cross-stream contracts: do imports match exports?
           Return PASS or FAIL per stream + integration verdict."
```

**Full Mode (`--thorough`):** Spawn BE + FE evaluators in parallel, minimum 2 rounds:
```
Round 1: blind-evaluator-be + blind-evaluator-fe → PASS/FAIL per stream
  IF all PASS → Round 2 (mandatory for Full mode)
  IF any FAIL → report findings (user fixes manually)

Round 2: NEW evaluator pair (fresh context) → final verdict
```

#### Step 4: Graded Verdict

Grade convergence against 4 criteria:

| Criterion | Weight | Question | Grade /10 |
|---|---|---|---|
| Completeness | 30% | All gaps closed? Output contracts honored? | |
| Correctness | 25% | Tests pass? Evidence provided? | |
| Integration | 25% | Cross-stream connections work? | |
| Quality | 20% | Production-ready? Rule 14 compliance? | |

**Thresholds:**
- Weighted average ≥ 7.0 = **PASS** → COMPLETE
- Any single criterion < 5.0 = **FAIL** regardless of average
- Weighted average 5.0-6.9 = **CONDITIONAL** → user decides next action

**Iteration Decision:**
| Condition | Action |
|---|---|
| All ≥ 7.0 | COMPLETE — update manifest status + emit JSONL |
| 1-2 criteria < 7.0 | CONDITIONAL — report findings, user re-dispatches if needed |
| Any criterion < 5.0 | FAIL — report findings, recommend re-dispatch with specific QA feedback |

#### Step 5: Verify Mesh

Run verification based on touched files:
- Backend files → `verify-implementation` (pytest, schema, hardening)
- Frontend files → `verify-implementation` + `verify-ui-consistency`
- All → regression gate: `after_failures ≤ before_failures`

#### Step 6: Finalize

Update manifest.json:
```json
{
  "status": "completed",
  "current_phase": "D",
  "phase_history": [..., {"phase": "D", "ts": "...", "exit": "ok"}],
  "convergence": {
    "eval_rounds": 1,
    "grades": {"completeness": 8, "correctness": 7, "integration": 7, "quality": 7},
    "weighted_avg": 7.3,
    "verdict": "PASS"
  }
}
```

**Phase D Gate (MUST output before declaring COMPLETE):**
```
┌─ PHASE D GATE ──────────────────────────────────────┐
│ Git diff scanned: {yes/no}                          │
│ Checkpoints read: {N}/{total_streams}               │
│ Evaluator spawned: {yes/no} — verdict: {PASS/FAIL}  │
│ Graded verdict: C={N} R={N} I={N} Q={N} avg={N}    │
│ Manifest updated with convergence: {yes/no}         │
│ Gate status: PASS / FAIL — {reason if fail}         │
└─────────────────────────────────────────────────────┘
```

Emit JSONL:
```json
{"event":"converge","run_id":"<id>","gaps_closed":{N},"gaps_remaining":{N},"verdict":"PASS|FAIL|CONDITIONAL","grades":{"c":{N},"r":{N},"i":{N},"q":{N}},"ts":"..."}
```

**A run with no Phase D JSONL event = unverified. Dashboard shows ⚠️ UNVERIFIED.**

## Dashboard Mode (`/adhd` without arguments)

```markdown
## Komission Domain Health Dashboard
> Generated: YYYY-MM-DD HH:MM

| Domain | Active Runs | Checkpoints | Avg Progress | Gaps | Priority |
|--------|------------|-------------|-------------|------|----------|

### Active ADHD Runs
| Run ID | Domain | Tier | Streams | Status | Phase D | Age |
|--------|--------|------|---------|--------|---------|-----|
| ... | ... | ... | ... | active | ⚠️ UNVERIFIED | 3d |
| ... | ... | ... | ... | completed | ✅ PASS (7.3) | 1d |
| ... | ... | ... | ... | active | — | 8d ⚠️ STALE |

### Recommended Focus (Rule 11 compliant)
1. <domain> (highest gap count)
2. <domain> (dependency of above)

### Stale Runs (>7 days, no recent checkpoint)
| Run ID | Age | Last Activity | Action |
|--------|-----|---------------|--------|
```

## Graceful Degradation

**`ADHD_STATELESS=1`** — When state harness is unavailable or broken:
- Falls back to current copy-paste model (Phase C outputs text packets only)
- No JSON state files created
- Convergence uses time-based staleness instead of SHA-based
- All features work, just without automation

Activate: Set environment variable or pass `--stateless` flag.

## ADHD-Specific Red Flags

| ADHD Trap | Recognition | Correction |
|---|---|---|
| "한 터미널에서 다 하자" | 2+ gaps, not distributing | Tier 2 is DEFAULT → /tkm → distribute to N sessions |
| "나중에 합치면 되지" | No /checkpoint at session end | /checkpoint is MANDATORY before session close |
| "이것도 빨리 고치자" | Drifting to another domain's gap | Rule 11 warning + stay on current domain |
| "대충 되겠지" | Skipping Phase A/A.5 | RECON + DEEP-DIVE mandatory — no routing without deep evidence |
| "TK 한번 더 돌리자" | Same topic repeated debate | 1 debate per topic → execute, don't re-debate |
| "이거 Tier 0이지" | Underestimating complexity | **If uncertain → Tier 2, not Tier 1.** ADHD exists to distribute. |
| "Gap 1개네" | Counting by category not items | Count INDIVIDUAL items: "7 endpoints" = 7 gaps, not 1 |
| "의존성 안 봐도 되겠지" | Skipping Phase A.5 deep-dive | Phase A.5 is MANDATORY — upstream/downstream/cross-layer trace required |
| "TKM 안 써도 되지" | Tier 2 without /tkm invocation | Tier 2 MUST invoke /tkm for work package generation |

## When NOT to Use ADHD

- **Single-file bug fix** → just fix it
- **Already have a spec from /interview** → use `/execute`
- **Real-time multi-person collaboration** → use `/team create`
- **First time exploring a domain** → use Explore agent directly
- **No skeleton exists** → ADHD assumes scaffolding is already in place

## Stability Guards

- Phase A Explore agents timeout: 2 minutes → output `⚠ PHASE A INCOMPLETE — [agent N timed out, M findings gathered]` and proceed. User sees the marker.
- TKM invocation timeout: 5 minutes → output `⚠ TKM INCOMPLETE — DHR produced without work packages` and proceed with DHR only.
- **Incomplete Phase Marking**: If ANY phase could not be fully completed (timeout, missing data, tool failure), output `⚠ PHASE [X] INCOMPLETE — [reason]` inline. This marker is visible to the user and to `/adhd verify` convergence scanning.
- Max write-stream count advisory: 4 (warn at >4, hard warn at >6)
- `/adhd verify` re-enters Phase B at most 2 times
- Max 1 active ADHD run per domain (prevent overlapping runs)

### Sub-Skill Crash Protocol (stop_failure)

> 31개 run 분석: 23 stop_failure events (33% of all events), 전부 TKC.
> Sub-skill crash 시 대응 프로토콜이 없으면 stream이 영원히 stale.

When a sub-skill (/tkc, /tk, /ralph) crashes during stream execution:

| Failure | Action |
|---------|--------|
| /tkc crash (1st time) | Retry once. If fails again → downgrade to direct implementation (skip debate). |
| /tk crash (Codex MCP) | Fall back to /tkc. Log: `{"event":"fallback","from":"tk","to":"tkc",...}` |
| /ralph crash | Check state file. If Phase 1+ complete → resume from last cycle. If Phase 0 → restart. |
| Multiple crashes (3+) in same run | **STOP the stream.** Mark stream status = `failed`. Report in notices.md. |

### Run Lifecycle

> 31 run directories, most status="active" since March 22. No cleanup mechanism.

**Stale Run Detection (Dashboard mode):**
- Run age > 7 days with no checkpoint updates → mark `⚠️ STALE` in dashboard
- Run age > 14 days → mark `⚠️ EXPIRED — consider archiving or re-running`
- Recommend: `mv .claude/state/adhd/runs/<stale-run> .claude/state/adhd/archived/`

**Run cannot be "completed" without:**
1. `convergence` field in manifest (from Phase D)
2. At least 1 `converge` event in JSONL
3. `current_phase` = "D" in manifest

Runs without these → status remains "active" or "abandoned" (never "completed").

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|---|---|---|
| `/adhd` on domain with no commits | No git data = no diagnosis | Explore the domain first |
| Ignoring Rule 11 | Defeats focus discipline | Respect 2-domain budget |
| Running `/adhd verify` before sessions complete | Premature convergence | Wait for all `/checkpoint` calls |
| Using ADHD for production incidents | Too slow for incidents | `/team create hotfix` |
| Skipping `/checkpoint` in child sessions | Breaks convergence tracking | ALWAYS `/checkpoint` at session end |
| ADHD implementing code directly | Violates mothership principle | Route to sub-skill, never implement |
| **Counting gaps by category** | **Understates true gap count, suppresses Tier 2** | **Count individual items: "7 missing endpoints" = 7 gaps** |
| **Skipping Phase A.5** | **Routes without understanding blast radius** | **Phase A.5 is MANDATORY — no routing without dependency trace** |
| **Tier 2 without /tkm** | **Produces vague terminal packets instead of conflict-free work packages** | **Tier 2 MUST invoke /tkm — it handles file ownership + conflict audit** |
| **Defaulting to Tier 0/1** | **Defeats ADHD's purpose — distributing work** | **Tier 2 is DEFAULT. Tier 0/1 require explicit 4-condition justification** |

## Output Format

```
## /adhd: <domain> [topic]

### Phase A — Domain Health Report
{DHR with Skeleton Map, Gap Matrix (individual counts!), Priority Queue, Rule 11 Budget}

### Phase A.5 — Dependency Deep-Dive
{Dependency Annotation Table: upstream, downstream, cross-layer, blast radius per gap}
{Updated gap count + severity after deep-dive}

### Phase B — Route Decision
{Tier selected + justification}
{If Tier 0/1: explicit 4-condition downgrade justification}
{If Tier 2 (default): /tkm invocation plan}

### Phase C — Dispatch (Tier 2-3)
{/tkm invocation + work package output}
{State harness setup}
{N terminal dispatch packets (from /tkm work packages)}
{Rule 11 + topology checks}
```

For `/adhd verify`:
```
## /adhd verify: <domain>

### Re-scan (PULL from git)
{git diff + checkpoint scan results}

### Convergence Report
{Gaps Closed / Remaining / New + Stream Status table}

### Evaluator Verdict
{blind-evaluator PASS/FAIL per stream + integration}

### Graded Verdict
{Completeness/Correctness/Integration/Quality scores + weighted avg}

### Phase D Gate
{Structured gate checklist}

### Verdict
{COMPLETE / CONDITIONAL / FAIL}

### Verification Mesh
{verify-implementation + verify-ui-consistency results}
```

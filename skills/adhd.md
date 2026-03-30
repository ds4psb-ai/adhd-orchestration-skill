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
        → Phase D    (CONVERGE: blind-evaluator adversarial loop + graded verdict — invoked separately)
                     ↺ FAIL → re-dispatch (Phase C) with evaluator feedback
                     ↺ PASS round 1 → mandatory round 2 (single-pass misses ~30%)
                     ↺ PASS round 2 → COMPLETE
```

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

Write `manifest.json`:
```json
{
  "run_id": "run_<date>_<domain>",
  "domain": "<domain>",
  "tier": 2,
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "base_sha": "<git HEAD>",
  "streams_count": 3,
  "status": "active",
  "dhr_path": ".claude/state/adhd/runs/<run-id>/dhr.json"
}
```

Write `dhr.json` (structured DHR for machine consumption).

TKM writes `streams/stream-N.json` with ownership, contracts, acceptance criteria.

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

### Phase D — CONVERGE (`/adhd verify`)

**PULL-based** — does NOT rely on sessions reporting their own completion. Scans git state directly.

#### Step 1: Re-scan (PULL from git)

```bash
# What changed since run started?
git log --oneline <base_sha>..HEAD -- <all owned_files across streams>
git diff --stat <base_sha>..HEAD -- <all owned_files>
```

Read checkpoint JSON sidecars for each stream (if available).
Read `notices.md` for any inter-session signals.

#### Step 2: Generate new DHR

Run Phase A again for the same domain. Compare against original DHR.

#### Step 3: Convergence Report

```markdown
## Convergence Report: <domain>

### Gaps Closed (✅)
| Gap | Closed By | Commit | Evidence |
|-----|-----------|--------|----------|

### Gaps Remaining (❌)
| Gap | Reason | Next Action |
|-----|--------|-------------|

### New Gaps Discovered (⚠️)
| Gap | Source | Priority |
|-----|--------|----------|

### Stream Status (from git scan + checkpoint JSON)
| Stream | Files Changed | Commits | Checkpoint Progress | Status |
|--------|--------------|---------|---------------------|--------|
```

#### Step 4: Blind Evaluator Loop (Ralph-style — MANDATORY)

> "Separating the agent doing the work from the agent judging it proves to be a strong lever."
> "I ran 5-15 iterations per generation, each pushing in a more distinctive direction."
> — Anthropic Engineering, 2026-03-24
>
> **Repetition breeds excellence.** Each evaluation round surfaces issues the prior round missed.
> 10 rounds of eval produced "distinctive designs" — this is the core philosophy.

**ADHD Phase D now runs Ralph's blind-evaluator loop at the convergence level.**
This is NOT implementation-level eval (that's Ralph per-stream). This is **cross-stream integration eval**.

**Step 4a: Spawn Cross-Stream Blind Evaluators (PARALLEL)**

```
Agent tool (spawn BOTH in one message):

  subagent_type: blind-evaluator-be
  prompt: "Cross-stream backend convergence eval for ADHD run <run-id>.
           Read manifest at .claude/state/adhd/runs/<run-id>/manifest.json.
           For EACH backend stream: grep target symbols, run pytest --testmon -x -q,
           verify acceptance criteria from work package.
           Check cross-stream API contracts: do imports match exports?
           Return PASS or FAIL per stream + cross-stream integration verdict."

  subagent_type: blind-evaluator-fe
  prompt: "Cross-stream frontend convergence eval for ADHD run <run-id>.
           Read manifest at .claude/state/adhd/runs/<run-id>/manifest.json.
           For EACH frontend stream: grep target symbols, run bun run build,
           check i18n keys in ko.json + en.json, verify acceptance criteria.
           Check cross-stream component contracts: do shared types match?
           Return PASS or FAIL per stream + cross-stream integration verdict."
```

**Step 4b: Eval Loop (MINIMUM 2 rounds, NO MAXIMUM)**

```
Round 1: Spawn evaluators → collect PASS/FAIL per stream
  IF all PASS → Round 2 (mandatory — single-pass misses ~30%)
  IF any FAIL → fix findings → re-verify → re-evaluate (new evaluator pair)

Round 2: Spawn NEW evaluators (fresh context, no anchoring to Round 1)
  IF all PASS → proceed to Step 4c (Graded Verdict)
  IF any FAIL → fix → re-verify → Round 3

Round 3+: Continue until ALL PASS or iteration_budget exhausted.
  Each round: new evaluators, new context, new findings.
  "10 rounds produced distinctive designs" — more rounds = higher quality.
```

**Step 4c: Graded Verdict (AFTER eval loop PASS)**

> Adapted from Anthropic evaluator: "I wrote four grading criteria... each criterion
> had a hard threshold, and if any one fell below it, the sprint failed."

Grade convergence against 4 criteria:

| Criterion | Weight | Question | Grade /10 |
|---|---|---|---|
| Completeness | 30% | All gaps closed? Stubbed features? Output contracts honored? | |
| Correctness | 25% | Implementation actually works? Tests pass? Evidence provided? | |
| Integration | 25% | Cross-stream connections work? Import/export contracts match? | |
| Quality | 20% | Production-ready? Hardening debt? Rule 14 compliance? | |

**Thresholds:**
- Weighted average ≥ 7.0 = **PASS** → COMPLETE
- Any single criterion < 5.0 = **FAIL** regardless of average
- Weighted average 5.0-6.9 = **CONDITIONAL** → iteration decision needed

**Step 4d: Iteration Decision** (from P7 Iteration Loop):
| Condition | Action |
|---|---|
| All ≥ 7.0 AND eval loop PASS x2 | COMPLETE |
| 1-2 criteria < 7.0, scores trending up | REFINE (fix weak areas, same approach) |
| 2+ criteria < 5.0 or scores trending down | PIVOT (re-enter Phase B with revised DHR) |
| iteration_budget exhausted | "Convergence requires manual judgment" + full report |

**Re-dispatch protocol:**
When REFINE or PIVOT → decrement iteration_budget → re-enter Phase C with:
- Updated DHR (Phase D re-scan results)
- Specific QA feedback per failing criterion
- Blind evaluator findings from failed rounds
- "Fix failed areas first, then re-test" (generator rule from Anthropic harness)

#### Step 5: Verify Mesh

Run verification based on touched files:
- Backend files → `verify-implementation` (pytest, schema, hardening)
- Frontend files → `verify-implementation` + `verify-ui-consistency`
- All → regression gate: `after_failures ≤ before_failures`

#### Step 6: Observability

Append to `~/.claude/adhd-runs.jsonl`:
```json
{"event": "converge", "run_id": "<id>", "gaps_closed": 5, "gaps_remaining": 2, "gaps_new": 1, "convergence_pct": 71, "timestamp": "..."}
```

## Dashboard Mode (`/adhd` without arguments)

```markdown
## Komission Domain Health Dashboard
> Generated: YYYY-MM-DD HH:MM

| Domain | Active Runs | Checkpoints | Avg Progress | Gaps | Priority |
|--------|------------|-------------|-------------|------|----------|

### Active ADHD Runs
| Run ID | Domain | Tier | Streams | Status | Base SHA | Age |
|--------|--------|------|---------|--------|----------|-----|

### Recommended Focus (Rule 11 compliant)
1. <domain> (highest gap count)
2. <domain> (dependency of above)
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

### Re-scan DHR (PULL-based)
{Updated Domain Health Report from git scan}

### Convergence Report
{Gaps Closed / Remaining / New}

### Stream Status
{Per-stream progress from git + checkpoint JSON}

### Verdict
{COMPLETE / RE-ENTER / DEFER}

### Verification Mesh
{verify-implementation + verify-ui-consistency results}
```

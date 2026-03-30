---
name: ralph
description: "Persistent execution harness — Generator + Blind Evaluator loop with external state"
argument-hint: "TASK_DESCRIPTION"
---

# Ralph — Persistent Execution Harness

> "Separating the agent doing the work from the agent judging it proves to be a strong lever."
> "Out of the box, Claude is a poor QA agent." — Anthropic Engineering, 2026-03-24

You are the **Generator**. A separate **blind-evaluator** agent judges your work.
You do not exit until the evaluator says PASS.

**State lives in a task-scoped state file, not in your memory.** Read it first. Update it every cycle.

### State File Resolution (Parallel-Safe)
Ralph uses **task-scoped state files** — each Ralph session gets its own file.
This prevents conflicts even when multiple agents run on the same branch.

**Directory:** `.claude/state/ralph/`

**New task → create new file:**
```
STATE_DIR=".claude/state/ralph"
mkdir -p "$STATE_DIR"
# Derive slug from task description (first 40 chars, lowercase, hyphens)
TASK_SLUG=$(echo "TASK_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' /:' '-' | cut -c1-40 | sed 's/-*$//')
STATE_FILE="${STATE_DIR}/${TASK_SLUG}.md"
```

**Resume existing task → find matching file:**
```bash
ls -t .claude/state/ralph/   # list by modification time
# Find file whose ## Task section matches your current task
```

**NEVER use root `state file` directly.** That file is legacy.
If it exists and matches your task, migrate it into `.claude/state/ralph/` on first access.

**Examples:**
- Task "Fix healthcheck failure" → `.claude/state/ralph/fix-healthcheck-failure.md`
- Task "Boards preview items" → `.claude/state/ralph/boards-preview-items.md`
- Two agents on same branch, different tasks → different files → zero conflict

---

## When NOT to Use Ralph

- Planning only — no implementation to verify
- Trivial one-shot fix with no real verification burden
- A lighter direct fix is clearly enough

---

## YOU WILL WANT TO SKIP STEPS. YOU MUST NOT.

| Thought | Reality |
|---------|---------|
| "Tests pass, so I'm done" | Tests verify compilation, not completeness |
| "This is already correct" | Prove it with grep evidence |
| "The blind audit is overkill" | It EXISTS because you think this |
| "Build passes, ship it" | Build ≠ all consumers safe |
| "I can evaluate my own work" | No. You cannot. Anthropic proved this. |
| "One eval round is enough" | Single-pass misses ~30% of issues. Minimum 2 rounds. |
| "I only changed one file" | One file can have 10 downstream consumers. Trace them. |
| "The upstream is unrelated" | Every symbol has a producer. Find it. |
| "I'll skip the patch plan" | No plan → scattered edits → missed sites. |

## Non-Negotiable Failure Modes

This harness exists to stop these patterns. If you notice any, stop and correct:

1. **Self-approval** — declaring success without an explicit evaluation step
2. **Scope reduction** — silently dropping hard requirements
3. **Evidence fabrication** — claiming checks passed without reading the output
4. **Dependency blindness** — patching one site and missing upstream/downstream effects
5. **Verification theater** — running commands but not using the results
6. **Loop skipping** — failing to re-run evaluation after meaningful changes

---

## Loop Protocol

```
Phase 0  Read state file → fresh-start → grep symbols → trace upstream/downstream → patch plan
Phase 1  Execute (smallest coherent change per patch plan)
Phase 2  Verify (tests + build + re-grep)  ← MINIMUM 2 ROUNDS
Phase 3  Blind Evaluator (MANDATORY)       ← MINIMUM 2 ROUNDS
         FAIL → fix → Phase 2
         PASS (1st) → Phase 1 (address ADVISORY items) → Phase 2 → Phase 3 again
         PASS (2nd) → Phase 4
Phase 4  Completion Gate → update state file → commit → push
```

### Minimum Iteration Rule (MUST)
- **Verify: ≥2 rounds.** First verify catches obvious issues. Second verify catches regressions from fixes.
- **Blind Evaluator: ≥2 rounds.** First evaluator finds gaps. Second evaluator confirms gaps are closed.
- Evaluator ADVISORY items from round 1 → treat as Phase 1 work before round 2.
- This rule exists because single-pass verification misses ~30% of issues (observed pattern).

**Every interim output ends with:**
`Completion promise: I will continue until the work is complete or I hit a real blocker with evidence.`

---

## Phase 0 — Ground + Trace

### 0A. Initialize State File (MUST FRESH-START)
1. Derive `STATE_FILE` path from your task description (see State File Resolution above).
2. If the file already exists AND its `## Task` matches → **resume** (read and continue).
3. If the file doesn't exist OR task doesn't match → **create fresh**.
4. If root `state file` exists and matches → migrate it into `.claude/state/ralph/`.

Write fresh state file:
- task description
- target symbols (from task)
- target areas (directories)
- verification commands (pytest, bun build, etc.)
- completion gates (grep counts, test pass, evaluator PASS x2)
- **success criteria** — how success will be measured
- **stopping rule** — what "done when" means

### 0A.5 Check for Upstream Handoff (OPTIONAL — does NOT skip Phase 0)

If `.claude/state/handoff.json` exists:
1. Read it — extract `debate_topic`, `final_decision`, `target_files`, `acceptance_criteria`, `evidence_summary`
2. Pre-populate state file with these as **HINTS**:
   - task description ← `debate_topic` + `final_decision`
   - target areas ← `target_files` (directories)
   - completion gates ← `acceptance_criteria`
   - evidence context ← `evidence_summary`
3. Delete `handoff.json` after reading (consumed — one-shot handoff)
4. **Phase 0B-0F still MANDATORY** — handoff is acceleration, not bypass

If `.claude/state/handoff.json` does NOT exist:
- Proceed normally (standalone `/ralph` invocation)

### ADHD Integration (if running as part of ADHD dispatch)

If environment has ADHD context (`run_id`, `stream_id` visible in terminal packet):
1. Record in state file: `adhd_run_id`, `adhd_stream_id`
2. On completion (Phase 4), append to `.claude/state/adhd/runs/<run-id>/notices.md`:
   ```
   [STREAM <stream_id> COMPLETE] — <task summary>
   Files changed: <list>
   Evaluator rounds: <count>
   Final verdict: PASS
   ```
3. This enables ADHD Phase D to scan stream completion without polling

If no ADHD context → skip this section (standalone mode).

### 0B. Inspect Repo State
```bash
git status --short
git log --oneline -5
```
Dirty state or unexpected branches → resolve before proceeding.

### 0C. Symbol Trace (MANDATORY)
For EVERY symbol you will change:
```bash
rg -n "symbol_name" backend/ frontend/
```
- List ALL sites: producers + consumers
- Record count: `review_reason: 5 sites (1 producer, 4 consumers)`
- Write to state file under `target_symbols`

**Exit contract:** If you cannot list all sites, you are not ready to edit.

### 0D. Upstream/Downstream Dependency Trace (MANDATORY)
Symbol grep alone is not enough. For each target symbol, trace the **dependency chain**:

1. **Upstream** — What calls/configures/feeds this symbol? Follow the chain to the root.
   - Config files that set values consumed by the symbol
   - Services that produce data the symbol reads
   - CI/CD pipelines, deploy scripts, healthchecks that reference it
2. **Downstream** — What consumes/depends on this symbol's output?
   - Endpoints, tests, scripts that call or import it
   - Documentation that references the current behavior
   - External systems (Railway, Vercel, CI) that depend on it

Record in state file: `upstream: [list]`, `downstream: [list]` per symbol.

**Exit contract:** If you cannot list at least one upstream and one downstream per symbol, investigate deeper before proceeding.

### 0E. Patch Plan (MANDATORY)
Before touching any code, document a **concrete patch plan** in state file:

| # | File | Change | Rationale |
|---|------|--------|-----------|

This forces you to think through ALL sites before editing the first one.
The plan is the contract — Phase 1 executes exactly this plan, no more, no less.

### 0F. Read files before touching them.

---

## Phase 1 — Generator Work

### Cross-Stream Safety (if ADHD stream context exists)

When running as part of an ADHD multi-stream dispatch:
- **Your owned files** (from work package Target Files table): full read/write
- **Other stream files**: READ-ONLY — do NOT modify
- If you discover a bug in another stream's file:
  1. Append to `.claude/state/adhd/runs/<run-id>/notices.md`:
     `[DISCOVERY] Stream <yours> found issue in <file> (owned by Stream <N>): <description>`
  2. Do NOT fix it — let the owning stream handle it

If not running under ADHD → no restrictions (standalone mode).

### Generator Rules

1. Change ALL sites from Phase 0C — not just the first one
2. Backend = code + tests together
3. Frontend = component + i18n together
4. After editing, re-grep every changed symbol immediately:
```bash
rg -n "symbol_name" backend/ frontend/
# Count must match Phase 0B. Unpatched sites → patch NOW.
```

---

## Phase 2 — Verify

### Layer 1: Tests + Build
```bash
cd backend && source venv/bin/activate && pytest --testmon -x -q
cd frontend && bun run build
```
**Read the output. Copy the summary line. Do not say "passes" unless you saw it.**

### Layer 2: Compare with Prior Iteration
After every meaningful change:
- re-run the relevant verification commands
- compare results with the prior iteration
- record what improved, regressed, or stayed unchanged

### Layer 3: Inspect Artifacts, Not Just Scores
Do not rely on pass/fail alone. Check actual:
- diffs, test output, build output
- generated files, user-visible behavior

### Layer 4: Re-grep
For each changed symbol → confirm zero unpatched sites.

### Layer 5: Contracts
- i18n → keys in both `ko.json` AND `en.json`
- Types changed → all consumers handle new type
- VDG → `normalize_vdg_schema()` only
- No `Any` in new code

### Update state file
Write: iteration number, phase=verifying, test results, grep counts, open gaps.

---

## Phase 3 — Blind Evaluator (MANDATORY — NEVER SKIP)

Spawn **two evaluators in parallel** to avoid context window truncation:

### Cross-Stack Tasks (backend + frontend changed)
Spawn both `blind-evaluator-be` and `blind-evaluator-fe` simultaneously:

```
Agent tool invocation (parallel — send BOTH in one message):

  subagent_type: blind-evaluator-be
  prompt: "Evaluate backend changes for Ralph state at STATE_FILE_PATH.
           Grep target symbols in backend/ only. Run pytest --testmon -x -q.
           Check backend completion gates. Return PASS or FAIL with evidence."

  subagent_type: blind-evaluator-fe
  prompt: "Evaluate frontend changes for Ralph state at STATE_FILE_PATH.
           Grep target symbols in frontend/src/ only. Run bun run build.
           Check i18n keys in ko.json + en.json. Return PASS or FAIL with evidence."
```

**Both PASS → proceed to Phase 4.**
**Either FAIL → fix findings → back to Phase 2 → spawn NEW evaluator pair.**

### Single-Layer Tasks (backend only OR frontend only)
Spawn only the relevant evaluator:
- Backend only → `blind-evaluator-be`
- Frontend only → `blind-evaluator-fe`

Replace `STATE_FILE_PATH` with the actual path (e.g., `.claude/state/ralph/fix-healthcheck.md`).

Do NOT debate findings. If evaluator flagged it, CHECK IT with code evidence.
**Do NOT reuse an old PASS after the code materially changed.** New code = new evaluation.

---

## Phase 4 — Completion Gate

ALL must be TRUE with FRESH evidence:

- [ ] All task requirements met (no scope reduction)
- [ ] Tests pass (paste summary)
- [ ] Build passes (paste summary)
- [ ] Blind evaluator(s): PASS (BE + FE or relevant single evaluator)
- [ ] Re-grep: zero unpatched sites
- [ ] i18n complete (if UI changed)
- [ ] VDG via normalizer (if VDG touched)
- [ ] state file updated: phase=complete

**Any gate fails → back to Phase 1.**

### Final Update
Write to state file: `phase: complete`, `status: done`, final cycle log entry.

### Commit + Push (DEFAULT)
After all gates pass:
1. Stage only files changed by this Ralph cycle (NOT unrelated dirty files)
2. Commit with descriptive message explaining "why"
3. Push to current branch

**Skip commit/push ONLY if:** user explicitly said not to, or changes are draft/experimental.
This exists because completed work that isn't committed gets lost or conflicts with parallel work.

---

## Escalation
- Same failure 3+ iterations → blocker, ask user
- VDG/DB schema changes → exhaustive trace first
- Auth/security → user approval required
- Evaluator FAIL 3+ consecutive → report pattern

## Forbidden
- Self-approval without evaluator PASS
- "이미 올바름" without grep evidence
- Skipping Phase 0C symbol trace
- Skipping Phase 3 blind evaluator
- Relying on conversation memory instead of state file
- Omitting completion promise from interim outputs

---

Task: $ARGUMENTS

---
name: tkm
description: "Tiki-Taka Meta-prompt Factory (TKM) — Parallel Work Package Generator. Decomposes complex multi-subsystem problems into N self-contained, conflict-free work packages for parallel execution."
hooks:
  SubagentStop:
    - matcher: "Explore"
      hooks:
        - type: command
          command: ".claude/hooks/explore-witness.sh"
  StopFailure:
    - matcher: ""
      hooks:
        - type: command
          command: "echo '{\"event\":\"stop_failure\",\"skill\":\"tkm\",\"ts\":\"'$(date -u +%FT%TZ)'\"}' >> ~/.claude/adhd-runs.jsonl"
---

# Tiki-Taka Meta-prompt Factory (TKM) — Parallel Work Package Generator

Generate 1-N **self-contained meta-prompt documents** for parallel execution in separate terminal sessions. Each document is designed to be consumed by `/tk`, `/tkc`, or `/tktk` — never executed directly.

**Core principle:** /tkm INVESTIGATES and PARTITIONS. It does NOT implement, fix, or execute. Output = documents + JSON contracts.

**Why /tkm exists:** When a problem spans multiple subsystems, a single developer session becomes a bottleneck. /tkm decomposes the problem into N conflict-free work packages that N independent sessions can execute in parallel — with zero file conflicts and explicit API contracts between streams.

**MCP calls: 0** | **Subagent calls: 1** (Partition Auditor) | **Output: N markdown files + stream JSON contracts**

## Sovereignty

TKM is a **standalone skill** — it does NOT require ADHD context.

| Mode | Invocation | Context Source |
|------|-----------|----------------|
| **Standalone** | `/tkm "problem description"` | Self-investigation (Phase 1) |
| **ADHD-Routed** | `/tkm --from-run <run-id>` | Loads DHR + problem inventory from ADHD run manifest |

Both modes produce identical output format. ADHD-routed mode skips Phase 1 investigation (evidence already gathered).

## Usage

```
/tkm <problem description>           # standalone mode
/tkm                                 # uses current session context
/tkm --docs 3 <description>          # force specific document count
/tkm --from-run <run-id>             # ADHD-routed mode (loads existing DHR)
/tkm --json                          # also output stream contracts as JSON
```

## Architecture

```
Phase 1  (Deep Investigation + Problem Inventory)
  → Phase 2  (Skeleton: partition into N streams + file ownership + dependency graph)
    → Phase 3  (SUBAGENT: Partition Auditor — file conflict + semantic dependency verification)
      → Phase 4  (Document Expansion + Cross-Stream Contracts + Write Files)
```

## Incomplete Phase Convention

If ANY phase could not be fully completed (timeout, tool failure, missing data), output `⚠ PHASE [X] INCOMPLETE — [reason]` inline. This marker is visible to the user and to `/adhd verify` convergence scanning.

## Protocol

### Phase 1 — Deep Investigation + Problem Inventory (MANDATORY)
> **Exit contract**: ≥2 agents, ≥3 findings each, Problem Inventory Table + File Dependency Map. INCOMPLETE if timeout.

**No partitioning is permitted until Phase 1 is complete.**

Combines evidence collection and problem enumeration into a single phase.

#### Step A: Investigation

Launch ≥2 Explore agents in parallel. Each agent MUST produce ≥3 concrete findings (cite file:line, commit hash, or data point).

- **Agent 1: Direct** — Read ≥2 relevant source files, trace call paths, check schemas for the problem area.
- **Agent 2: Upstream/Downstream** — What FEEDS the problem area? What CONSUMES its output? Trace the full pipeline.
- **Agent 3: Historical** — MUST run unless topic has zero git history (cite why if skipping). `git log --oneline -20` for relevant files. Look for repeated fixes, threshold churn, regression patterns.

#### Step B: Problem Enumeration

After investigation, compile the **Problem Inventory Table**:

```markdown
## Problem Inventory

| # | Problem | Severity | File(s) | Status | Notes |
|---|---------|----------|---------|--------|-------|
| 1 | [concrete description] | CRITICAL/HIGH/MED/LOW | path/to/file.py | patch needed / investigation needed / resolved / by-design | [context] |
```

**Rules:**
- Every problem gets a row — no silent omissions
- Severity must be justified (not gut feel)
- "Status: resolved" or "by-design" items stay in the table but are excluded from partitioning
- **Actively exclude false positives** — verify each issue exists before listing

#### Step C: File Dependency Map

For all files involved in unresolved problems, build:

```markdown
## File Dependency Map

| File | Imports From | Exported To | Public API Surface |
|------|-------------|-------------|-------------------|
| service_a.py | config.py, models.py | router_x.py, task_y.py | func_1(), func_2() |
```

This map is the input for Phase 2 partitioning and Phase 3 conflict audit.

### Phase 2 — Skeleton: Partition into N Streams
> **Exit contract**: N-stream partition with zero file conflicts + method recommendations per stream.

Decide how many documents to generate and what each covers.

#### Step A: Partition Strategy

Consider these dimensions (in priority order):

1. **File ownership** — Each stream owns distinct files. The primary partition criterion.
2. **Semantic cohesion** — Issues that share root causes or data flows belong together.
3. **Dependency direction** — If Stream A's output feeds Stream B's input, they are separate streams with an explicit contract.
4. **Severity balance** — Don't put all HIGH issues in one stream and all LOW in another.

**Partition constraints:**
- Default: 2-3 documents (user can override with `--docs N`)
- Each document should have 2-6 issues (too few = overhead not justified, too many = loses focus)
- **ZERO file overlap between streams** — if two issues require editing the same file, they MUST be in the same stream
- **Shared files** (config, models, types): if read-only by all streams → OK. If written by any stream → assign to that stream exclusively.

#### Step B: Conflict-Free Verification (pre-audit)

Before subagent audit, do a quick self-check:

```
Stream 1 files: {A, B, C}
Stream 2 files: {D, E, F}
Stream 3 files: {G, H, I}

Intersection check:
  1∩2 = {} ✓
  1∩3 = {} ✓
  2∩3 = {} ✓
```

If any intersection is non-empty, reassign the conflicting file to ONE stream.

#### Step C: Method Recommendation

For each document, recommend the execution method:

| Condition | Recommended Method | Reason |
|-----------|-------------------|--------|
| ≤2 issues, ≤3 files, no architecture decisions | `/tkc` | Fast self-debate (~1-3 min) |
| ≥3 issues OR architecture/design decisions | `/tk` | Cross-model diversity needed |
| Unknown root cause + SoTA comparison needed | `/tktk` | Deep 3-round research |
| Trivial/mechanical changes only | Direct execution (no debate) | Debate overhead not justified |

#### Step D: Skeleton Output

```markdown
## Partition Skeleton

### Document 1: [Title] — [Domain]
- Issues: #2, #5, #8
- Files: [list]
- Method: /tk
- Estimated: 2-3 rounds

### Document 2: [Title] — [Domain]
- Issues: #3, #7, #11
- Files: [list]
- Method: /tkc
- Estimated: 1-2 rounds

### Cross-Stream Dependencies:
- Doc 1 → Doc 2: function_x() signature (Doc 1 may modify, Doc 2 imports)
- Doc 2 → Doc 3: table.column (Doc 2 adds, Doc 3 reads)
```

### Phase 3 — Partition Auditor (SUBAGENT)
> **Exit contract**: Subagent PASS/FAIL per audit category. INCOMPLETE if timeout >3min.

Spawn a fresh-context subagent to audit the partition for conflicts and gaps.

**Agent configuration:**
- `subagent_type`: `general-purpose`
- Full tool access (Read, Grep, Glob needed for import tracing)

**Subagent prompt structure:**

```
You are a **Merge Conflict Prevention Specialist**. Your job: verify that N work streams can execute in parallel without file conflicts or semantic dependency violations.

## PARTITION TO AUDIT
{Phase 2 Skeleton output — stream definitions, file lists, dependency map}

## YOUR VERIFICATION CHECKLIST

### 1. File Overlap (MUST: zero tolerance)
For each pair of streams, verify ZERO shared files.
Use Glob/Grep to check for files referenced but not listed.

### 2. Import Graph Conflicts (MUST)
For each stream's files, trace imports:
- `grep -r "from X import"` for each file X owned by another stream
- If Stream A's file imports from Stream B's file, the API contract must be explicit
- Flag any import where the IMPORTED function is likely to change (it is in the issue list)

### 3. Shared State (SHOULD)
Check for shared mutable state:
- Database tables written by multiple streams
- Redis keys written by multiple streams
- Global config values modified by multiple streams
- Shared type definitions that may change

### 4. Missing Issues (SHOULD)
Cross-reference the Problem Inventory against the partition:
- Every unresolved issue must appear in exactly one stream
- No issue should be split across streams
- No issue should be orphaned (present in inventory but absent from all streams)

### 5. Self-Containedness (SHOULD)
For each stream's document, verify:
- Context section has enough info to understand the problem WITHOUT reading other documents
- File list is complete (no implicit "also edit X")
- Acceptance criteria are independently verifiable

## OUTPUT FORMAT
```markdown
## Audit Results

### File Overlap: PASS/FAIL
[details]

### Import Conflicts: PASS/FAIL
[details — list each cross-stream import with risk level]

### Shared State: PASS/WARN/FAIL
[details]

### Issue Coverage: PASS/FAIL
[orphaned or duplicated issues]

### Self-Containedness: PASS/WARN
[gaps found]

### Recommended Fixes
1. [fix]
2. [fix]
```
```

**Post-audit:** Apply recommended fixes. If FAIL on File Overlap or Import Conflicts → revise partition before proceeding.

### Phase 4 — Document Expansion + Write Files
> **Exit contract**: N self-contained markdown docs written + cross-stream summary with conflict matrix.

Write N markdown files. Each document must be **self-contained** — a developer in a fresh terminal with no prior context can execute it.

#### Document Template

```markdown
# [Stream Title]

> **Owner**: Developer [X] (independent /tk[c] session)
> **Priority**: **[CRITICAL|HIGH|MED]** — [one-line justification]
> **Scope**: [affected subsystems in 10-20 words]
> **Estimated**: [N] /tk[c] rounds
> **Method**: /tk[c|tk] ([reason for recommendation])

---

## Context

### Background
[Problem area overview — enough for a developer with NO prior context to understand]

### What Triggered This
[Specific incident, finding, or session that surfaced these issues]

### Root Cause Chain (if applicable)
```
[visual trace: Service A → Service B → ❌ gap → symptom]
```

---

## Target Files (This Stream Only)

| File | Lines | Role | Cross-Stream Conflict |
|------|-------|------|----------------------|
| `path/to/file.py` | ~N | [role description] | None |

**Conflict guarantee**: These files are NOT modified by any other stream.

---

## Issue [N]: [Title]

### Phenomenon
[Concrete, reproducible description]

### Code Location
**File**: `path/to/file.py:line_range`
```python
# relevant code snippet (5-15 lines)
```

### Root Cause / Investigation Points
1. [Question or hypothesis to investigate during /tk debate]
2. [Alternative explanation to consider]

### Patch Design (direction, not implementation)
[Pseudocode or decision points — /tk session decides the final approach]

---

## API Contract

### This stream IMPORTS (read-only dependencies):
```python
# Functions/data from OTHER streams — signatures must not change
from module_a import func_x  # (ParamType) → ReturnType — owned by Stream [N]
```
**Rule**: If Stream [N] changes these signatures, notify this stream's operator.

### This stream EXPORTS (other streams depend on):
```python
# Functions/data that OTHER streams consume
def func_y(param: Type) -> ReturnType:  # consumed by Stream [M]
```
**Rule**: Signature changes require notification to Stream [M] operator.

### Shared Data (if any):
```
table.column — Type — written by this stream, read by Stream [N]
```

---

## Merge Strategy

- **Merge order**: [This stream can merge independently / Must merge after Stream X]
- **Integration check**: [What to verify after merge — e.g., "run pytest for module Y"]
- **Rollback**: [How to revert this stream's changes without affecting others]

---

## [Method] Topic

```
/tk[c] [Domain] [Issue Summary]:
(1) [Issue 1 — 2-3 line description with investigation angle].
(2) [Issue 2 — description].
(3) [Issue 3 — description].
[Key files]: [file list].
[Constraint]: Do not modify other stream files — [list of off-limits files].
[Context]: [1-2 sentences of essential background].
```

**Copy the above block into a fresh terminal session.**

---

## Acceptance Criteria

- [ ] [Verifiable condition 1]
- [ ] [Verifiable condition 2]
- [ ] `pytest --testmon` passes (backend changes)
- [ ] `bun run build` passes (frontend changes)
- [ ] No files outside Target Files table were modified
```

#### File Naming & Location

- **Location**: `docs/{domain}/` (auto-determined from problem area)
  - VDG issues → `docs/vdg/`
  - Frontend issues → `docs/ui/`
  - Infrastructure → `docs/ops/`
  - Cross-cutting → `docs/` root
- **Naming**: `{prefix}-{stream-number}-{slug}.md`
  - Example: `canary-patch-5-dispatch-safety.md`, `hotfix-1-auth-race.md`
  - User can specify prefix; default derived from problem description

#### Cross-Stream Summary

After writing all N documents, output a summary:

```markdown
## Cross-Stream Summary

### Documents Generated
| # | File | Issues | Priority | Method | Files Modified |
|---|------|--------|----------|--------|---------------|
| 1 | docs/vdg/patch-5-dispatch.md | #2, #5, #8 | HIGH | /tk | 5 files |
| 2 | docs/vdg/patch-6-schema.md | #3, #7 | HIGH | /tkc | 4 files |

### Execution Order
[Can all run in parallel? Or is there a dependency ordering?]

### File Conflict Matrix
| | Stream 1 | Stream 2 | Stream 3 |
|---|----------|----------|----------|
| Stream 1 | — | [contract type] | None |
| Stream 2 | [contract type] | — | [contract type] |

### Post-Merge Integration
[What to verify after ALL streams are complete]
```

## Anti-Pattern Guards (MUST)

### /tkm Does NOT:
1. **Write code** — Output is documents, not implementation
2. **Execute patches** — Documents describe WHAT to investigate and patch, not HOW (that is /tk's job)
3. **Run tests** — Documents include test criteria, not test execution
4. **Make architecture decisions** — Documents frame the decision for /tk debate
5. **Produce a single monolithic document** — If the problem is complex enough for /tkm, it needs N>1 documents

### Quality Gates:
1. **Every issue accounted for** — Problem Inventory ↔ Document Issues must be 1:1
2. **Zero file overlap** — Phase 3 subagent must PASS
3. **Self-contained** — Each document readable without others
4. **Method justified** — /tk vs /tkc recommendation has explicit reason
5. **Acceptance criteria testable** — No vague "improve X" criteria

### When NOT to use /tkm:
- Single-file bug fix → just fix it
- 1-2 issues in the same subsystem → use /tk or /tkc directly
- Already have a spec from /interview → use /execute
- Real-time collaboration needed → use `/team create`

## Stability Guards

- **No MCP dependency**: Entire protocol runs locally. No hang risk.
- **Subagent timeout**: If Partition Auditor >3 minutes, output `⚠ PHASE 3 INCOMPLETE — audit timed out, using self-verified partition` and proceed.
- **Phase 1 timeout**: If Explore agents >2 min, output `⚠ PHASE 1 INCOMPLETE — [N findings gathered]` and proceed.
- **Min/Max documents**: Minimum 1 (degenerate case), Maximum 5 (beyond this, use `/team create` instead).
- **Large file handling**: If a file >800 lines must be shared between streams, flag it and suggest refactoring as a prerequisite issue in one stream.

## Output Format

```
## TKM: {problem description}

### Phase 1 — Investigation + Problem Inventory
{Problem Inventory Table + File Dependency Map}

### Phase 2 — Partition Skeleton
{N-stream partition with file ownership + method recommendations}

### Phase 3 — Partition Audit
{Subagent audit results — PASS/FAIL per category}

### Phase 4 — Documents Generated
{Summary table + file paths}
{Cross-Stream Summary with conflict matrix}

### Files Written
- `docs/{domain}/{name-1}.md`
- `docs/{domain}/{name-2}.md`
- `docs/{domain}/{name-3}.md`
```

## JSON Contract Output

When `--json` flag is used OR when invoked via `--from-run`, TKM additionally writes stream contract files:

```
.claude/state/adhd/runs/<run-id>/streams/stream-N.json
```

**Stream JSON Schema:**
```json
{
  "run_id": "run_<date>_<domain>",
  "stream_id": "s<N>",
  "title": "<stream title>",
  "domain": "<domain>",
  "owned_files": ["path/to/file.py"],
  "read_dependencies": ["path/to/shared.py"],
  "write_contracts": [
    {
      "function": "func_name()",
      "signature": "(param: Type) -> ReturnType",
      "consumed_by": "s<M>"
    }
  ],
  "method": "direct|tkc|tk|tktk",
  "acceptance_criteria": ["pytest passes", "no files outside owned list modified"],
  "verification_required": ["backend-pytest", "verify-vdg-schema"],
  "base_sha": "<git HEAD at partition time>",
  "status": "pending"
}
```

In standalone mode without `--json`, stream contracts are embedded in the markdown work packages only.

## Arguments

If called with arguments, use them as the problem description.
If called without arguments, use the current session context (recent discussion, active issues, git status).
`--docs N` forces specific document count (overrides auto-detection).
`--from-run <run-id>` loads existing DHR from ADHD run (skips Phase 1).
`--json` writes stream contract JSON files alongside markdown documents.

<!-- Origin: https://github.com/ds4psb-ai/adhd-orchestration-skill | License: MIT + Attribution | (c) 2026 ds4psb-ai -->

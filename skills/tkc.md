---
name: tkc
description: "Claude 단독 Generator↔Evaluator: context-isolated subagent evaluation with 6-layer debiasing. Anthropic harness pattern의 single-model 구현."
hooks:
  Stop:
    - matcher: ""
      hooks:
        - type: command
          command: ".claude/hooks/skill-witness.sh"
  SubagentStop:
    - matcher: "Explore"
      hooks:
        - type: command
          command: ".claude/hooks/explore-witness.sh"
  StopFailure:
    - matcher: ""
      hooks:
        - type: command
          command: "echo '{\"event\":\"stop_failure\",\"skill\":\"tkc\",\"ts\":\"'$(date -u +%FT%TZ)'\"}' >> ~/.claude/adhd-runs.jsonl"
---

# Tiki-Taka Claude Self-Debate (TKC) — Context Isolation Protocol

Run a structured self-debate using a **fresh-context subagent** as blind challenger. Achieves cognitive diversity through **structural isolation** (not different models) — the challenger cannot see the proposer's reasoning chain.

**Why subagent > same-session persona switch:** Same-session role-play is anchored to the full context window. A subagent starts with a clean slate — physically different context = genuinely independent evaluation. Combined with persona inversion and criteria rotation, this is the highest-fidelity single-model debate possible.

**When to use /tkc vs /tk:**
- `/tk` — Codex MCP available, want cross-model cognitive diversity (different training data)
- `/tkc` — Codex MCP unavailable/slow, want fast structured debate (~1-3 min vs 10-18 min)

## Usage

```
/tkc <topic or question>
/tkc              # debates the current task/context
```

## Prerequisites

- No external MCP required (MCP calls: 0)
- Uses Agent tool for subagent challenger (1 subagent call)

## Architecture

```
Phase 0    (Claude: deep research — Explore agents + web search)
  → Phase 0.5  (Claude: SoTA web research — replaces Codex probe)
    → Phase 1    (Claude: bold proposal with commitment markers)
      → Phase 1.5  (Context Packet: proposal + raw evidence ONLY, no reasoning chain)
        → Phase 2    (SUBAGENT: blind challenger — fresh context, different persona/criteria)
          → Phase 2.5  (Claude: verify + expand challenger claims)
            → Phase 3    (Claude: defense + Position Lock + synthesis + self-bias audit)
```

**MCP calls: 0** | **Subagent calls: 1** | **Research phases: 3** (0, 0.5, 2.5)

## Harness Role Mapping

> Source: Anthropic "Harness Design for Long-Running Application Development" (2026-03-24)

| Anthropic Harness | TKC Phase | Implementation |
|---|---|---|
| Planner | (upstream: /tkm or user) | Problem spec before debate |
| Generator | Phase 1 — Bold Proposal | Claude produces solution with evidence |
| Evaluator | Phase 2 — Blind Challenger | Subagent evaluates independently (clean context) |
| Feedback loop | Phase 2.5 → Phase 3 | Verify claims → Defend or Revise |
| Grading criteria | Phase 2 prompt + Phase 3C | Persona criteria + bias audit |
| Context reset | Subagent spawn | Key innovation: physically separate context |

Blog insight: "Tuning a standalone evaluator to be skeptical turns out to be far
more tractable than making a generator critical of its own work."
→ TKC implements this via context-isolated subagent with mandatory disagreement quota.

Blog insight: "Out of the box, Claude is a poor QA agent. It took several rounds
of tuning before the evaluator was grading in a way that I found reasonable."
→ TKC mitigates this via Anti-Sycophancy Protocol + 6-layer debiasing stack.

## Debiasing Stack

| Layer | Technique | Effect |
|-------|-----------|--------|
| 1 | Context isolation (subagent) | No anchoring to prior reasoning chain |
| 2 | Persona assignment | Different evaluation perspective |
| 3 | Criteria inversion | Same evidence, different lens |
| 4 | Mandatory disagreement quota | Prevents sycophantic agreement |
| 5 | Blind evidence (no interpretation) | Forces independent analysis |
| 6 | Self-bias audit (Phase 3C) | Post-hoc detection of residual bias |

## Incomplete Phase Convention

If ANY phase could not be fully completed (timeout, tool failure, missing data), output `⚠ PHASE [X] INCOMPLETE — [reason]` inline. This marker is visible to the user and enables post-hoc quality assessment.

## Protocol

### Phase 0 — Evidence Collection (MANDATORY)
> Exit contract: ≥2 agents launched, ≥3 findings each, Evidence Base 7 fields populated.

**Steps:**
1. **Launch ≥2 Explore agents in parallel**, each MUST produce ≥3 concrete findings
   (cite file:line, commit hash, or data point).
   - Agent 1: **Direct investigation** — read ≥2 relevant source files, trace call paths
   - Agent 2: **Upstream investigation** — trace ROOT of pipeline/system
   - Agent 3: **Historical investigation** — git log/blame (skip only if zero git history)

2. **Root Cause Probe** — "Is the proposed change more likely to introduce negatives
   than positives? What happens if we trace the problem to its true origin?"

3. **Web Search Gate** — Execute if ANY condition met:
   - Library/framework latest version features involved
   - APIs/policies that may have changed after 2025-05
   - Recency keywords ("latest", "2026", "current")
   - Technical architecture or system design decision
   - Keep searches concise: 1-3 queries, cite in debate

4. **Compile Evidence Base**:
   - Data examined, Key metrics, Root cause trace
   - Git history pattern, Web search findings
   - Gaps remaining, Confidence (HIGH/MED/LOW per finding)

**TKC-specific additions to Web Search Gate:**
- "Internal code patterns that may have industry-standard alternatives or known anti-patterns"
- "A design decision of any kind is being made (naming, structure, flow, error handling)"

### Phase 0.5 — SoTA Self-Research (replaces Codex probe)
> After Phase 0, research state-of-the-art across 4 dimensions using WebSearch/tavily (no Codex MCP):
> 1. **SoTA alternatives** — better approaches (2025-2026), anti-patterns, production solutions
> 2. **Recency check** — deprecated APIs, breaking changes, new best practices
> 3. **Production evidence** — theoretical vs proven at scale
> 4. **Cutoff awareness** — flag anything outdated (Claude cutoff 2025-05)

**TKC-specific: Mandatory Execution Enforcement (MUST)**

Phase 0.5 is MANDATORY by default. Skip ONLY if ALL 5 conditions are met:
1. Purely internal naming/formatting/style (no external pattern applies)
2. No library, framework, protocol, or algorithm involved
3. No architectural or design decision being made
4. Zero interaction with external systems (APIs, DBs, queues, auth)
5. Can articulate what searches you WOULD run and why each returns zero results

**Anti-Skip Rationalizations (NOT valid reasons to skip):**
| Rationalization | Why it's wrong |
|---|---|
| "Internal codebase work" | Industry patterns/anti-patterns apply to ALL code |
| "Hardening task" | Hardening practices evolve |
| "Not a technology decision" | Architecture decisions need SoTA comparison |
| "All evidence is internal" | Internal evidence needs external validation |
| "Simple refactoring" | Refactoring patterns have documented pitfalls |
| "Just fixing a bug" | Bug classes have known solutions |
| "No external dependency" | Design patterns are external knowledge |

### Phase 1 — Bold Proposal with Commitment Markers
> **Exit contract**: Root-cause-backed proposal + ≥2 I COMMIT markers with confidence levels.

Present a bold proposal grounded in Phase 0 evidence + Phase 0.5 web findings:

1. **Pre-Proposal Investigation** (90-second cap):
   - For each SoTA alternative found → check if codebase has supporting components
   - For each anti-pattern flagged → verify whether current code exhibits it
   - Launch 1-2 Explore agents if web findings opened new vectors

2. **Proposal** with:
   - Reference specific data from Phase 0
   - Incorporate relevant SoTA findings from Phase 0.5
   - Root Cause assessment: explain WHY this problem exists
   - State explicitly:
     - What value the ambitious version unlocks
     - What would be lost if scope is reduced
     - What upstream causes your research uncovered
     - What you are MOST excited about in this proposal
   - Flag known biases: note where reasoning might favor elegance over pragmatism

3. **Commitment Markers** — For each core claim:
   ```
   I COMMIT: [claim]. Confidence: HIGH/MED/LOW. Falsifiable by: [condition]
   ```
   These markers serve as anchors for the Phase 3 bias audit.

### Phase 1.5 — Context Packet Preparation
> **Exit contract**: Context packet with proposal + raw evidence only (no reasoning chain).

**This is /tkc's core innovation.** Prepare the Context Packet for the blind challenger.

**INCLUDED** (challenger receives):
- Phase 1 proposal text (conclusions only)
- Raw evidence (data, metrics, code snippets)
- File paths list
- Assigned persona + evaluation criteria

**EXCLUDED** (challenger does NOT receive):
- Claude's reasoning chain
- Phase 0 evidence interpretation/analysis
- Root cause analysis process
- Web search result interpretation
- Prior conversation context

**Persona Selection** — Choose the persona that creates maximum cognitive tension with the proposal type:

| Proposal Type | Challenger Persona | Inversion Criteria |
|---------------|-------------------|-------------------|
| Architecture/Design | **Production SRE** ("I'm the one paged at 3AM for this") | Operational cost, failure modes, MTTR |
| Performance/Optimization | **Minimalist Architect** ("What's the simplest version?") | Complexity cost, maintenance burden |
| New Feature | **Skeptical PM** ("Do users actually want this?") | User value, opportunity cost |
| Bug Fix | **Root Cause Detective** ("This is a symptom, not the cause") | Upstream causes, systemic patterns |
| Refactoring | **Pragmatic Senior Dev** ("It works. Why touch it?") | Risk-reward ratio, rollback plan |
| Security | **Adversarial Red Teamer** ("How do I break this?") | Attack surface, threat model gaps |
| Default | **Devil's Advocate Researcher** ("Let me find counter-evidence") | Counter-evidence, alternative explanations |

### Phase 2 — Blind Challenger (SUBAGENT)
> **Exit contract**: Subagent 8-point critique + disagreement ledger + score. INCOMPLETE if timeout >5min.

Spawn a fresh-context subagent using the **Agent tool**.

**Agent configuration:**
- `subagent_type`: `general-purpose` (full tool access: Read, Grep, Glob, WebSearch)
- NO `isolation: worktree` — needs same codebase access
- Prompt constructed from Context Packet (Phase 1.5)

**Subagent prompt structure:**

```
You are a {PERSONA_NAME}. {PERSONA_DESCRIPTION}.

## YOUR EVALUATION CRITERIA (different from the proposer's)
{INVERTED_CRITERIA}

## ANTI-SYCOPHANCY PROTOCOL
Your value comes ONLY from GENUINE disagreement. Agreement is CHEAP and WORTHLESS.
You MUST:
1. Identify ≥3 substantive flaws (not cosmetic)
2. Propose ≥1 fundamentally different approach
3. Rate your genuine disagreement 1-10 at the end
   - If <5: you haven't looked hard enough. Try again.
   - If 10: you disagree on everything. Check for contrarian bias.

## CONTEXT PACKET
{Proposal text + raw evidence ONLY — no reasoning chain}

## YOUR TASK
(0) SoTA CHALLENGE: Is there a fundamentally better approach?
(1) REALITY CHECK: Phantom references? Missing APIs?
(2) ROOT CAUSE: Deeper upstream cause missed?
(3) INTERPRETATION: Alternative explanations for the same evidence?
(4) IMPLEMENTATION GAP: Where does this break in practice?
(5) PRESERVE & STRENGTHEN: Make valuable parts MORE ambitious
(6) BETTER EXECUTION: Architecture/phasing alternatives
(7) WHAT'S MISSING: What should be ADDED?

## GRADING CRITERIA (evaluate the proposal against these, from Anthropic evaluator pattern)
Grade each 1-10 before writing your critique:

| Criterion | Weight | Question |
|---|---|---|
| Root Cause Accuracy | 30% | Does proposal address actual cause, not symptoms? |
| Implementation Feasibility | 25% | Can this work with existing code/infra? |
| Blast Radius Control | 25% | What breaks if implementation is wrong? |
| Value Ambition | 20% | Does this unlock real value beyond minimal fix? |

Overall weighted score: __/10
If < 6.0: flag "PROPOSAL NEEDS FUNDAMENTAL REVISION" at top of critique.

## MANDATORY INDEPENDENT RESEARCH
You MUST do your own investigation (read code, search codebase) before critiquing.
Do NOT rely solely on the provided evidence.

## DISAGREEMENT LEDGER
For each point: KEEP / STRENGTHEN / MODIFY / CUT (proof required) / PHASE
Rate: GENUINE INSIGHT vs PERFORMATIVE DISAGREEMENT (self-audit)
Final disagreement score: __/10
```

**Post-subagent:** If challenger's disagreement score <5/10, the critique is likely too weak. Note this in Phase 3 bias audit but proceed (do NOT re-spawn).

### Phase 2.5 — Investigation (Verify + Expand Challenger Claims)
> **Exit contract**: Each challenger claim verified/expanded with code evidence. INCOMPLETE if >3min.

After receiving the challenger's critique, investigate before defending.

**Four vectors** (same as /tk Phase 1.5 MEGA):

1. **Verify** — For each verifiable challenger claim:
   - Claims a field/table/API doesn't exist → Check code or schema
   - Claims behavior differs from stated → Read implementation
   - Points out a data pattern → Run the query
   - Suggests a metric is wrong → Re-measure

2. **Expand** — For each NEW angle the challenger introduced:
   - Mentions a related subsystem → Investigate that subsystem
   - Questions the root cause → Trace DEEPER upstream
   - Suggests alternative architecture → Check if components exist in codebase

3. **Connect** — For each indirect connection discovered:
   - Follow dependency chains (what calls this? what does this call?)
   - Check for related bugs/patterns in git history
   - Query DB for actual data that validates or invalidates

4. **Pre-Synthesize** — Prepare for final defense:
   - Identify open questions still unresolved
   - Check integration concerns
   - Run final DB/code verification

**Hard cap: 3 minutes.** If exceeded, output `⚠ PHASE 2.5 INCOMPLETE — [N claims verified, M remaining]` and proceed with gathered evidence.

### Phase 3 — Defense + Position Lock + Synthesis + Bias Audit
> **Exit contract**: Category A/B/C filtering + Position Lock + Scope Report + Bias Audit + witness block.

#### Section A — Defense

Respond to EVERY challenger point with AGGRESSIVE filtering:

- **Category A (Accept)**: Concrete technical flaw with proof (API doesn't exist, field missing from schema, ToS violation with specific clause)
- **Category B (REJECT unless independently confirmed)**: Scope reduction framed as pragmatism ("simpler would work", "too complex"). REJECT by default.
- **Category C (REJECT)**: Generic risk aversion ("what if X fails", "might be too ambitious"). Reject outright.

**Phase 2.5 Integration**: For each investigated point:
- "Challenger flagged [X] — I verified: [result]. [Accept/Reject with evidence]."
- "Challenger introduced [Y] — I expanded investigation: [NEW findings]."
- "Connected investigation revealed [Z] — neither perspective had seen this."

**DO NOT CAPITULATE.** Maximum strength defense.

#### Position Lock

> "After defense, my position is: [explicit statement]. Is this weaker than my Phase 1 position? [yes/no + justification]. If yes, I must restore scope before proceeding."

If position is weaker than Phase 1 without Category A evidence, STOP and restore.

#### Section B — Synthesis

Present the **Scope Preservation Report**:
```
## Scope Preservation Report
- Original proposal components: [list]
- KEPT: [list]
- STRENGTHENED: [list — what got MORE ambitious through debate]
- MODIFIED: [list]
- PHASED: [list — destination preserved]
- CUT: [list — Category A evidence only]

Scope preserved: [percentage]
Debate delta: What changed because of self-debate?
Evidence delta: What new facts emerged from Phases 0/0.5/2.5?
```

**RED FLAG**: If scope preserved <70%, either the original proposal was genuinely flawed (cite Category A evidence), or you capitulated — go back and restore Category B/C cuts.

#### Section C — Self-Bias Audit (TKC-specific)

**Same-model debate requires explicit bias detection since there is no external judge.**

```
## Bias Audit
1. ANCHORING CHECK: How many Category B/C rejections are "defending what I already decided"?
   - Each rejection: EVIDENCE-BASED (specific grounds) or ANCHORING (defending prior position)
   - Anchoring ratio: __/%  (>40% → revisit rejections)

2. SYCOPHANCY CHECK: Among agreements with challenger, how many are genuine vs model echo?
   - Each agreement: GENUINE CONVERGENCE or MODEL ECHO
   - Echo ratio: __/%  (>50% → challenger critique was too weak)

3. NOVELTY CHECK: Did the debate produce genuinely new insights?
   - List novel insights (if none → debate value questionable)

4. SCOPE DELTA: What changed through debate?
   - Components ADDED through debate: __
   - Components STRENGTHENED: __
   - Components CUT with Category A evidence: __
   - Net ambition change: INCREASED / MAINTAINED / DECREASED

5. COMMITMENT AUDIT: Review Phase 1 commitment markers.
   - Each "I COMMIT" claim: HELD / MODIFIED (with reason) / ABANDONED (Category A only)
   - Abandoned without Category A → anchoring failure, restore
```

**If anchoring ratio >40% OR echo ratio >50%:** Flag to user and recommend revisiting specific decisions.

### Final Decision

Present the final synthesized position. Since there is no external verdict:
- State final position explicitly
- Highlight what the debate changed (the delta)
- Flag any bias audit concerns
- If bias audit raised red flags, acknowledge limitations of single-model debate

## Anti-Deflation Guards

### Debate Integrity Obligations
1. **Default is KEEP, not CUT.** Burden of proof is on cutting.
2. **Defend your position.** Fight with specific technical evidence.
3. **Category B/C cuts REJECTED by default.** Only Category A (concrete flaw with proof) changes design.
4. **Phase ≠ Cut.** Phasing preserves the destination. Hidden cuts → reject.
5. **Final synthesis ≥ initial proposal ambition.** If less, explain with Category A evidence.
6. **Research-first.** Every claim backed by Phase 0 evidence.

### Obligation 7 (TKC-specific)
7. **Commitment markers are binding.** Abandoning a Phase 1 "I COMMIT" claim without
   Category A evidence is a bias signal detected in Phase 3C audit.

### Red Flags

**Core red flags (all debate skills):**
- Scope <70% of initial proposal → Likely capitulating. Restore B/C cuts.
- All challenger points accepted → Stopped thinking critically.
- Zero components STRENGTHENED → Debate only subtracted (deflation).
- Phase 0 skipped or shallow → Debate built on sand.

**TKC-specific:**
- Anchoring ratio >40% → Defending by inertia, not evidence. Revisit rejections.
- Echo ratio >50% → Challenger too sympathetic (same-model weakness). Flag to user.
- No novel insights → Debate didn't produce value. Acknowledge.
- Challenger disagreement score <5/10 → Critique too weak. Note in Phase 3C.

## Stability Guards

- **No MCP dependency**: Entire protocol runs locally. No hang risk.
- **Subagent timeout**: If challenger subagent takes >5 minutes, output `⚠ PHASE 2 INCOMPLETE — challenger timed out` and proceed with self-critique fallback.
- **Phase 0 timeout**: If Explore agents >2 min, output `⚠ PHASE 0 INCOMPLETE — [N findings gathered]` and proceed.
- **Phase 2.5 timeout**: Hard cap 3 minutes. If exceeded, output `⚠ PHASE 2.5 INCOMPLETE — [reason]` and proceed.
- **Session limit**: Max 3 self-debates per conversation (context management).
- **Malformed subagent response**: If challenger returns empty or broken output, perform self-critique using the 8-point framework as fallback.

## Output Format

Present each phase clearly:

```
## Self-Debate: {topic}

### Phase 0 — Evidence Collection
{Evidence Base: data, metrics, root cause trace, git history, web findings, gaps, confidence}

### Phase 0.5 — SoTA Research
{Web research findings on alternatives — marked as [Claude web research]}

### Phase 1 — Proposal + Commitment Markers
{Root-cause-backed proposal with value statement + I COMMIT markers}

### Phase 2 — Blind Challenger [{PERSONA_NAME}]
{Subagent critique with 8-point framework + disagreement ledger + score}

### Phase 2.5 — Investigation
{Verify + Expand + Connect + Pre-Synthesize — full findings}

### Phase 3 — Defense + Synthesis + Bias Audit
**Section A**: {Category A/B/C filtering + Phase 2.5 evidence}
**Position Lock**: {position statement + Phase 1 comparison}
**Section B**: {Scope Preservation Report + synthesis}
**Section C**: {Bias Audit — anchoring/sycophancy/novelty/scope delta/commitment audit}

### Decision
{Final position + debate delta + bias audit summary}

### Witness Block (MUST — append at end of debate output)
{"witness":{"skill":"tkc","phase":"final","components":{"C1":"KEEP","C2":"STRENGTHEN"},"incomplete":[],"scope_pct_informational":85}}
```

## Arguments

If called with arguments, use them as the debate topic.
If called without arguments, debate the current task, problem, or most recent discussion topic in context.

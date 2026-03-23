---
name: tkc
description: "Tiki-Taka Claude Self-Debate: Context-isolated subagent debate with persona inversion and bias audit. Use when user says /tkc, self-debate, or when Codex MCP is unavailable but structured debate is needed."
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

## Debiasing Stack

| Layer | Technique | Effect |
|-------|-----------|--------|
| 1 | Context isolation (subagent) | No anchoring to prior reasoning chain |
| 2 | Persona assignment | Different evaluation perspective |
| 3 | Criteria inversion | Same evidence, different lens |
| 4 | Mandatory disagreement quota | Prevents sycophantic agreement |
| 5 | Blind evidence (no interpretation) | Forces independent analysis |
| 6 | Self-bias audit (Phase 3C) | Post-hoc detection of residual bias |

## Protocol

### Phase 0 — Evidence Collection (MANDATORY)

**RULE: No proposal is permitted until Phase 0 is complete.** Even for short questions, gather evidence first.

**Steps:**

1. **Launch ≥2 Explore agents in parallel**, each MUST produce ≥3 concrete findings (cite file:line, commit hash, or data point).
   - Agent 1: **Direct investigation** — read ≥2 relevant source files, trace call paths, check schemas.
   - Agent 2: **Upstream investigation** — trace the ROOT of the pipeline/system. If the question is about X, investigate what FEEDS X and what X FEEDS INTO.
   - Agent 3: **Historical investigation** — MUST run unless topic has zero git history (cite why if skipping). git log/blame for relevant files. Look for patterns: repeated fixes, threshold churn, tuning spirals.

2. **Root Cause Probe** — Before forming your position, ask yourself:
   > "Is the proposed change more likely to introduce negatives than positives? What happens if we trace the problem to its true origin instead of patching the symptom?"

3. **Web Search Gate** — Execute web search if ANY of these conditions are met:
   - The question involves a specific library/framework's **latest version** features.
   - APIs, policies, or best practices that may have changed after 2025-05 (Claude's training cutoff) are relevant.
   - The user explicitly uses recency keywords ("latest", "2026", "current", "recently", "new").
   - A technical decision depends on information that could have changed post-cutoff.
   - The question involves a **technical architecture or system design** decision.
   - The question involves **internal code patterns** that may have industry-standard alternatives or known anti-patterns.
   - A **design decision** of any kind is being made (naming, structure, flow, error handling).
   - Keep searches concise: 1-3 queries, extract key facts only, cite in the debate.

4. **Compile the Evidence Base**:
   ```
   ## Evidence Base
   - **Data examined**: [Actual data — DB queries, code traces, API responses, file contents]
   - **Key metrics**: [Quantifiable findings — counts, scores, distances, percentages]
   - **Root cause trace**: [Upstream origin of the problem — not just the symptom]
   - **Git history pattern**: [If applicable — repeated fixes, threshold churn, tuning spirals]
   - **Web search findings**: [If applicable — recent info with sources]
   - **Gaps remaining**: [What is still unknown]
   - **Confidence**: HIGH/MED/LOW per finding
   ```

### Phase 0.5 — SoTA Self-Research (replaces Codex probe)

Claude performs its own state-of-the-art research using WebSearch + tavily.

**Research Dimensions** (same 4 as /tk Phase 0.5):

1. **STATE-OF-THE-ART ALTERNATIVES** — Search for better approaches to this class of problem (2025-2026). Include anti-patterns, failure case studies, production solutions.
2. **RECENCY CHECK** — What changed in the last 12 months? Deprecated APIs, breaking changes, new best practices.
3. **PRODUCTION EVIDENCE** — Distinguish "theoretical advantage" from "proven at production scale."
4. **CUTOFF AWARENESS** — Flag anything in own evidence that may be outdated (cutoff 2025-05).

**Execution Rule: MUST EXECUTE (opt-out, not opt-in)**

Phase 0.5 web research is MANDATORY by default. Skip ONLY if ALL of the following are true:
1. The topic is purely about this project's internal naming/formatting/style (no external pattern applies)
2. No library, framework, protocol, or algorithm is involved
3. No architectural or design decision is being made
4. The change has zero interaction with external systems (APIs, DBs, message queues, auth)
5. You can articulate what specific searches you WOULD run and why each would return zero useful results

If even ONE condition fails → MUST execute web research.

**If skipping, you MUST state:**
> Phase 0.5 SKIP JUSTIFICATION: [explain which searches you considered and why ALL 5 conditions are met]

**Anti-Skip Rationalizations (these are NOT valid reasons to skip):**
| Rationalization | Why it's wrong |
|---|---|
| "Internal codebase work" | Industry patterns/anti-patterns apply to ALL code |
| "Hardening task" | Hardening practices evolve — check latest approaches |
| "Not a technology decision" | Architecture decisions need SoTA comparison |
| "All evidence is internal" | Internal evidence needs external validation |
| "Simple refactoring" | Refactoring patterns have well-documented pitfalls |
| "Just fixing a bug" | Bug classes have known solutions — check if yours is optimal |
| "No external dependency" | Design patterns are external knowledge |

**Process:**
- Use WebSearch and/or tavily-search for verification
- Include version numbers and dates
- Integrate findings into Evidence Base before proceeding to Phase 1

**For internal codebase tasks, search for:**
- "[problem class] best practices 2025 2026" (e.g., "state machine hardening best practices")
- "[pattern name] anti-patterns production" (e.g., "retry logic anti-patterns production")
- "[technique] alternatives comparison" (e.g., "cosine similarity alternatives comparison")

### Phase 1 — Bold Proposal with Commitment Markers

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

## Anti-Deflation Guards (MUST)

### Claude's Obligations
1. **Default is KEEP, not CUT.** Burden of proof is on cutting, not on keeping.
2. **Defend your position.** If you believe in your proposal, fight for it.
3. **Category B/C cuts are REJECTED by default.** Only Category A changes the design.
4. **Phase ≠ Cut.** Phasing preserves the destination. Hidden cuts → reject.
5. **Ambition ratchet.** Final synthesis should be at least as ambitious as Phase 1. If less ambitious, explain each reduction with Category A evidence.
6. **Research-first.** Every claim must be backed by Phase 0 evidence.
7. **Commitment markers are binding.** Abandoning a commitment without Category A evidence is a bias signal.

### Red Flags (self-check)
- Scope <70% of Phase 1 → Likely capitulating. Restore B/C cuts.
- All challenger points accepted → Stopped thinking critically.
- Zero components STRENGTHENED → Debate only subtracted. That's deflation.
- Phase 0 was skipped or shallow → Debate built on sand. STOP and research.
- Position Lock violated → Section B weakened beyond Section A. Revert.
- Anchoring ratio >40% → Defending by inertia, not evidence.
- Echo ratio >50% → Challenger was too sympathetic (same-model weakness).
- No novel insights → Debate didn't produce value. Acknowledge.

## Stability Guards

- **No MCP dependency**: Entire protocol runs locally. No hang risk.
- **Subagent timeout**: If challenger subagent takes >5 minutes, output `⚠ PHASE 2 INCOMPLETE — challenger timed out` and proceed with self-critique fallback.
- **Phase 0 timeout**: If Explore agents >2 min, output `⚠ PHASE 0 INCOMPLETE — [N findings gathered]` and proceed.
- **Phase 2.5 timeout**: Hard cap 3 minutes. If exceeded, output `⚠ PHASE 2.5 INCOMPLETE — [reason]` and proceed.
- **Incomplete Phase Marking**: If ANY phase could not be fully completed (timeout, tool failure, missing data), output `⚠ PHASE [X] INCOMPLETE — [reason]` inline. This marker is visible to the user and enables post-hoc quality assessment.
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
```

## Arguments

If called with arguments, use them as the debate topic.
If called without arguments, debate the current task, problem, or most recent discussion topic in context.

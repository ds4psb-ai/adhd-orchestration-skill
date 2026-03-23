---
name: tktk
description: "Tiki-Taka Deep Research: 3-round Claude↔Codex debate with mandatory inter-round investigation. Use when deep root-cause analysis and state-of-the-art comparison are needed."
---

# Tiki-Taka Deep Research Protocol (3 Rounds)

Enhanced Tiki-Taka: every round is backed by expanding investigation. Not just debate — **research-debate-research-debate-research-synthesize.**

The difference: `/tk` researches at Phase 0 and Phase 1.5. `/tktk` researches at **every junction** — Claude expands investigation into DB, codebase, git history, and all directly/indirectly related topics after every Codex response, and Codex leverages web research for state-of-the-art alternatives.

## Usage

```
/tktk <topic or question>
/tktk              # debates the current task/context
```

## Prerequisites

- `codex-cli` MCP must be loaded (`mcp__codex-cli__codex`, `mcp__codex-cli__codex-reply`)
- If MCP is unavailable, inform the user and abort
- **MUST NOT pass `model` parameter** to any Codex MCP call. Codex CLI uses its own `~/.codex/config.toml` to select the model.

## Model Complementarity

Both models can read code and search the web. The debate's value comes from exploiting their **asymmetric strengths**:

| | Claude Opus 4.6 (Lead) | GPT-5.4 xhigh via Codex CLI (Challenger) |
|---|---|---|
| **Core edge** | Orchestrated deep investigation — Agent Teams, parallel Explore agents | Fresh perspective + superior web verification (BrowseComp 82.7%) |
| **Debate role** | Propose, defend, synthesize — grounded in multi-agent codebase evidence | Challenge, verify, broaden — grounded in web research + different training data |
| **Unique value** | Can trace call paths, git-blame, and query schemas simultaneously | Catches blind spots from different training, stronger on novel patterns (SWE-Bench Pro 57.7%) |
| **Blind spot** | Training cutoff 2025-05 — can miss recent changes in libs/APIs | Single-agent — can read files but can't orchestrate parallel deep dives |

**Principle:** A turn where either model does NOT leverage its core edge is a wasted turn.
- Claude turn without investigation (Explore agents, code traces, DB queries) = wasted
- GPT turn without web verification (Tavily, Playwright, browsing) = wasted

**tktk addition:** 3-round protocol means GPT gets 3 critique opportunities — each should leverage web research progressively deeper, not repeat the same searches.

## MCP Resilience

### Pre-flight — Health Check

Before the first Codex call (Phase 0.5), test MCP connectivity:

**Call** `mcp__codex-cli__codex` with:
- `prompt`: `Health check. Respond with exactly one word: READY`

- **Success** → proceed. Discard this thread (do NOT reuse the threadId).
- **Failure/hang >2 min** → abort debate. Inform user: "Codex MCP is unresponsive. Try again later or check `codex-cli` status."
- This call does NOT count toward the debate MCP budget.

### Prompt Quality (Thread Context, No Duplication)

**RULE: Thread context carries forward. Don't repeat what Codex already has.**

Codex retains full thread context across `codex-reply` calls. Resending identical evidence wastes tokens and increases latency dramatically (observed: 30min+ when evidence is duplicated).

- Phase 0.5: Send **structured evidence summary** (key findings as bullet list, not verbose explanations) — this is the foundation
- R1: Reference "evidence from Phase 0.5" — add only the NEW proposal. Do NOT resend the evidence base.
- R2/R3: Reference prior context — add only defense/synthesis delta. Do NOT resend prior rounds.
- R2/R3 defense delta format (DO NOT resend full synthesis):
  1. Category A accepted: [list of prior points + 1-line fix per point]
  2. Category C rejected: [list + 1-line evidence]
  3. Key changes from prior round: [bullet list of what's NEW]
  4. Scope Preservation Report (table only, no detailed sub-components)
  Codex has full prior context. Only send what CHANGED.

**Key principle:** Each Codex call should contain only NEW information. Prior context is preserved in the thread.

## Core Principle: Research-Debate Interleave

```
Phase 0 (Claude research)
    ↓
Phase 0.5 (Codex web research probe)
    ↓
Round 1 (Claude proposal → Codex critique)
    ↓
Phase 1.5 (Claude EXPANDED research — verify + expand)  ← NOT just verify, EXPAND
    ↓
Round 2 (Claude deepening → Codex re-critique)
    ↓
Phase 2.5 (Claude FINAL research — synthesize with evidence)  ← NEW in tktk
    ↓
Round 3 (Claude synthesis → Codex verdict)
```

**RULE**: Every arrow (↓) is a research gate. No round proceeds without fresh investigation.

## Protocol

### Phase 0 — Evidence Collection (MANDATORY)

**RULE: No Codex MCP call is permitted until Phase 0 is complete.**

**Steps:**

1. **Launch ≥2 Explore agents in parallel**, each MUST produce ≥3 concrete findings (cite file:line, commit hash, or data point).
   - Agent 1: Direct investigation — read ≥2 relevant source files, trace call paths, check schemas.
   - Agent 2: Upstream investigation — trace the ROOT of the pipeline/system being discussed. If the question is about X, investigate what FEEDS X and what X FEEDS INTO.
   - Agent 3: Historical investigation — MUST run unless topic has zero git history (cite why if skipping). git log/blame for relevant files. Look for patterns: repeated fixes, threshold churn, tuning spirals.

2. **Root Cause Probe** — Before forming your position, ask yourself:
   > "Is the proposed change more likely to introduce negatives than positives? What happens if we trace the problem to its true origin instead of patching the symptom?"

   This is NOT pessimism — it's the discipline that catches the 51st downstream patch before it's written.

3. **Web Search** — Execute web search if ANY of these conditions are met:
   - The question involves a technical architecture or system design decision
   - A specific library/framework's features are relevant
   - APIs, policies, or best practices that may have changed post-training-cutoff
   - The user uses recency keywords ("latest", "current", "recently", "new")
   - A technical decision depends on information that could have changed
   - Keep searches concise: 1-3 queries, extract key facts, cite in the debate

4. **Compile Evidence Base**:
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

### Phase 0.5 — Codex State-of-the-Art Probe

Before the debate begins, ask Codex to web-research whether better approaches exist.

**CHECKPOINT** — Before calling Codex, output the current debate state to the user:
> **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

**Call** `mcp__codex-cli__codex` with:
- `prompt`:
  ```
  Before we debate a specific proposal, I need your research capabilities.

  Topic: {topic summary}
  Current approach: {brief description}

  ## Key Evidence (Claude's Phase 0 findings)
  {Structured bullet-list summary of evidence — key metrics, root cause, gaps. NOT verbose prose.}

  ## RESEARCH FOCUS (web search)

  1. **STATE-OF-THE-ART + ANTI-PATTERNS**
     Search for better approaches to this class of problem (2025-2026).
     Include: anti-patterns, failure case studies, and how production systems actually solve this.
     For each finding: name, version, production adoption evidence, how it differs from current approach.
     If current approach IS state-of-the-art, confirm with evidence.

  2. **RECENCY CHECK**
     Deprecated APIs, breaking changes, major releases, new best practices.
     Flag anything from Claude's evidence that may be outdated (cutoff 2025-05).

  ## REQUIREMENTS
  - Use web search (Tavily) for verification — don't rely on training data alone
  - Include version numbers and dates
  - Distinguish "theoretical advantage" from "proven at production scale"
  - This is a research task, not a debate. Report findings objectively.
  ```
- Save the returned `threadId` for all subsequent rounds

**Integrate** Codex's web findings into your Evidence Base before proceeding to Round 1.

### Round 1 — Opening

1. **Claude** conducts a 90-second **Pre-Proposal Investigation** triggered by Phase 0.5 findings, then presents a bold proposal.

   **Pre-Proposal Investigation** (before writing the proposal):
   - For each SoTA alternative GPT found → check if codebase has supporting components or compatible architecture
   - For each anti-pattern GPT flagged → verify whether current code exhibits it
   - For each newer technique → investigate if existing architecture can accommodate it
   - Launch 1-2 Explore agents if web findings opened new investigation vectors
   - Time cap: 90 seconds (targeted, not broad)

   **Proposal** grounded in Phase 0 evidence + Phase 0.5 web findings + pre-proposal investigation:
   - Reference specific data from Phase 0
   - Incorporate relevant state-of-the-art findings from Phase 0.5
   - Root Cause assessment: explain WHY this problem exists, not just WHAT to fix
   - State explicitly:
     - What value the ambitious version unlocks
     - What would be lost if scope is reduced
     - What upstream causes your research uncovered
     - What you are MOST excited about in this proposal
   - Flag known biases: note where your reasoning might favor elegance over pragmatism.

2. **CHECKPOINT** — Before calling Codex, output the current debate state to the user:
   > **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

   **Call** `mcp__codex-cli__codex-reply` with:
   - `threadId`: saved threadId from Phase 0.5
   - `prompt`:
     ```
     Claude↔GPT debate. Your different training catches different things.

     Claude has done deep codebase research AND incorporated your Phase 0.5 web findings. Challenge INTERPRETATION, not absence of data.

     PROTOCOL: 3-round debate. After this, Claude investigates your points, responds in Round 2, then you re-critique, then Claude synthesizes in Round 3 for your final verdict. Front-load your best insights NOW — each subsequent round should go DEEPER, not repeat.

     RESEARCH: Verify technical claims via web search (Tavily) or codebase reads before stating them.
     Evidence hierarchy: Browsed/code-verified = Category A (Claude must address). Intuition-only = Category C (Claude will reject).

     Given this proposal (refer to our Phase 0.5 evidence for full context):

     {Claude's proposal with root cause analysis}

     Provide:
     (0) SoTA CHALLENGE: Fundamentally better approach? Describe concretely or confirm direction is sound.
     (1) REALITY CHECK: Phantom references? Missing fields/APIs? Acknowledge what Claude already verified.
     (2) ROOT CAUSE: Deeper upstream cause Claude missed?
     (3) INTERPRETATION: Alternative explanations for the same evidence?
     (4) IMPLEMENTATION GAP: Where breaks in practice? Propose FIX, not scope cut.
     (5) PRESERVE & STRENGTHEN: Make valuable aspects MORE ambitious.
     (6) BETTER EXECUTION: Architecture/phasing/guardrails that preserve destination.
     (7) WHAT'S MISSING: What should be ADDED?
     (8) LEDGER per component: KEEP / STRENGTHEN / MODIFY / CUT (proof of impossibility required) / PHASE (destination preserved)

     Be direct. Catch what Claude missed AND make the plan bolder.
     ```

3. **Present** Codex's response to the user

### Phase 1.5 — Expanded Investigation (CRITICAL — this is what makes /tktk different)

After Codex R1, do NOT just verify claims. **EXPAND your investigation** based on everything Codex raised.

**Three expansion vectors:**

1. **Verify** — For each verifiable Codex claim:
   - Questions whether a field/table/API exists → Check code or schema
   - Claims behavior differs from stated → Read implementation
   - Points out a data pattern → Run the query
   - Suggests a metric is wrong → Re-measure

2. **Expand** — For each NEW angle Codex introduced:
   - If Codex mentions a related subsystem → Investigate that subsystem
   - If Codex questions the root cause → Trace DEEPER upstream
   - If Codex suggests an alternative architecture → Check if components for it already exist in the codebase
   - If Codex references a concept → Check DB schema, git history, config for related fields

3. **Connect** — For each indirect connection you discover:
   - Follow dependency chains (what calls this? what does this call?)
   - Check for related bugs/patterns in git history
   - Query DB for actual data that would validate or invalidate the combined Claude+Codex hypothesis
   - Look for patterns: is this the Nth downstream patch? Are there tuning spirals?

**Process:**
1. List every verifiable claim AND new angle from Codex
2. Launch 2-3 Explore agents covering verify + expand + connect vectors
3. Run DB queries if relevant data exists
4. Compile results as Phase 1.5 Evidence Update

### Round 2 — Deepening

1. **Claude** conducts a 60-second **Pre-Defense Investigation**, then responds with FULL Phase 1.5 findings.

   **Pre-Defense Investigation** (before filtering):
   - Phase 1.5 findings marked "inconclusive" → one more targeted check
   - Codex R1 points not fully verified → one final investigation
   - Any MODIFY/CUT component → re-read actual implementation to confirm defense is grounded in current code
   - Time cap: 60 seconds (surgical, not broad)

   Apply AGGRESSIVE filtering:
   - **Category A (Accept)**: Concrete technical flaw with proof
   - **Category B (REJECT by default)**: Scope reduction as pragmatism
   - **Category C (REJECT)**: Generic risk aversion

   **Phase 1.5 Integration**: For each point investigated:
   - "Codex flagged [X] — I verified: [result]. [Accept/Reject with evidence]."
   - "Codex introduced [Y] — I expanded investigation: [NEW findings]."
   - "Connected investigation revealed [Z] — neither of us had seen this."

   **DO NOT CAPITULATE.** Defend with evidence.

2. **CHECKPOINT** — Before calling Codex, output the current debate state to the user:
   > **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

   **Call** `mcp__codex-cli__codex-reply` with:
   - `threadId`: saved threadId
   - `prompt`:
     ```
     Claude defended with expanded Phase 1.5 evidence (verify + expand + connect).
     RESEARCH: Verify claims via web/code. Browsed/code-verified = Category A. Intuition = Category C.

     {Claude's counterargument with Phase 1.5 findings}

     Push harder in BOTH directions:
     (1) STILL WRONG: What's still technically broken? Propose fixes, not cuts.
     (2) EVIDENCE REVIEW: Each claim — confirmed → fix, refuted → acknowledge, ambiguous → what settles it.
     (3) NEW EVIDENCE REACTION: React to Phase 1.5 discoveries neither side expected.
     (4) CONSERVATIVE BIAS SELF-CHECK: Each R1 scope reduction → concrete evidence (keep) or reflex (retract + fix).
     (5) WEB RESEARCH UPDATE: Search for anything new relevant to expanded findings.
     (6) AMBITION GAPS: Where is Claude TOO CONSERVATIVE?
     (7) UPDATED LEDGER: Every CUT must have proof of impossibility.
     (8) CONFIDENCE: Rate each point HIGH/MED/LOW.
     ```

3. **Present** Codex's re-critique to the user

### Phase 2.5 — Pre-Synthesis Research (tktk exclusive)

**60-second surgical investigation** before final synthesis:

1. **Unresolved disputes** — Points where Claude and Codex reached different conclusions in R1+R2 → one more code/data check
2. **Integration verification** — Components both sides agreed on from different angles → verify they are actually compatible
3. **Edge case data** — Boundary conditions mentioned in the debate → verify with actual data
4. **Evidence freshness** — If R2 Codex presented new web research results → cross-check against codebase
5. **Final DB/code verification** for the synthesis

Time cap: 60 seconds. Launch 1-2 Explore agents if needed.

**Compile Phase 2.5 Evidence** — this becomes the final evidence base for Round 3

### Round 3 — Convergence

1. **Claude** conducts a 60-second **Pre-Synthesis Surgical Check**, then synthesizes:

   **Pre-Synthesis Check** (before writing synthesis):
   - Phase 2.5 findings marked "inconclusive" → one final targeted check
   - Any MODIFY/CUT component → re-read actual implementation to confirm synthesis is grounded
   - R2 Codex points that Phase 2.5 didn't fully resolve → one last investigation
   - Time cap: 60 seconds (surgical, not broad)

   **Synthesis** incorporating ALL evidence (Phase 0 + 0.5 + 1.5 + 2.5 + surgical check):

   **Mandatory Scope Preservation Report:**
   ```
   ## Scope Preservation Report
   - Original proposal components: [list]
   - KEPT: [list]
   - STRENGTHENED: [list — what got MORE ambitious through debate]
   - MODIFIED: [list]
   - PHASED: [list — destination preserved]
   - CUT: [list — Category A evidence only]

   Scope preserved: [percentage]
   Debate delta: What changed because of cross-model debate?
   Evidence delta: What new facts emerged from Phases 0/0.5/1.5/2.5?
   Research value: Which research phase produced the highest-impact discoveries?
   ```

   **RED FLAGS:**
   - Scope <70% → Likely capitulation. Restore Category B/C cuts.
   - Zero STRENGTHENED → Debate only subtracted. That's deflation.
   - Phase 2.5 evidence ignored → You're debating from positions, not data.

2. **CHECKPOINT** — Before calling Codex, output the current debate state to the user:
   > **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

   **Call** `mcp__codex-cli__codex-reply` with:
   - `threadId`: saved threadId
   - `prompt`:
     ```
     FINAL round. No more exchanges after this. Claude conducted a surgical check, then synthesized with full evidence.

     {Claude's synthesis with full Scope Preservation Report}

     Final verdict:
     (1) AGREE or DISAGREE — state explicitly.
     (2) REMAINING RISKS: Technical risks only. "It's ambitious" is not a risk.
     (3) FINAL LEDGER with all components.
     (4) CONSERVATIVE BIAS AUTOPSY: Each R1+R2 scope reduction → GENUINE INSIGHT (keep) or CONSERVATIVE REFLEX (retract + fix). >50% reflex → acknowledge bias.
     (5) SCOPE DELTA: % ambition preserved, each CUT → impossibility or reflex, SELF-GRADE 1-10 conservative bias.
     (6) DEBATE VALUE: Genuine cross-model insight vs. generic risk aversion?
     (7) RESEARCH VALUE: Did inter-round research (0.5/1.5/2.5) change outcome? How?
     (8) WEB RESEARCH VALUE: Did SoTA findings influence direction? How?
     ```

3. **Present** Codex's verdict to the user

### Final Decision

- **If AGREE**: Adopt synthesized position. Summarize.
- **If DISAGREE**: Claude makes final call, stating overrides and why.

## Anti-Deflation Guards (MUST)

### Claude's Obligations
1. **Default is KEEP, not CUT.** Burden of proof is on cutting.
2. **Defend your position.** Fight for it with evidence.
3. **Category B/C cuts REJECTED by default.**
4. **Phase ≠ Cut.** Phasing must preserve destination.
5. **Ambition ratchet.** Final synthesis ≥ R1 ambition.
6. **Research-first.** Every claim backed by evidence.
7. **Inter-round research is MANDATORY.** No shortcutting Phases 1.5 or 2.5.

### Red Flags
- Codex won R1 AND R2 → Likely capitulating. Re-examine before R3.
- Scope <70% → Likely capitulating. Restore cuts.
- All Codex points accepted → Stopped thinking critically.
- Zero STRENGTHENED → Deflation.
- Phase 1.5 or 2.5 skipped → Debate built on sand.
- Web research ignored → Missing state-of-the-art context.

## Stability Guards

- **MCP hang detection**: Codex MCP calls have no built-in timeout. High-quality responses routinely take **10-18 minutes** — this is normal for GPT-5.4 xhigh reasoning. Only if a call exceeds **20 minutes** should the user consider it potentially hung.
  - Claude cannot detect a hang — the user must press **Escape (Ctrl+C)** to interrupt.
  - All work is preserved via checkpoints output before each MCP call.
  - After interrupt, apply the Phase-specific fallback below and continue the debate.
- **DO NOT rush Codex.** Long response time often correlates with higher quality output. Patience is rewarded.
- **Phase-specific fallbacks:**
  - **Phase 0.5 fails** → Claude performs its own web search (WebSearch tool) covering the 4 Research Dimensions. Mark as "[Claude web search — Codex probe unavailable]". Proceed to R1 with 3 remaining MCP calls.
  - **R1 Codex critique fails** → Claude performs self-critique using the 8-point framework, explicitly playing devil's advocate. Mark as "[Self-critique — Codex unavailable]". Proceed to Phase 1.5, then R2 with 2 remaining MCP calls.
  - **R2 Codex re-critique fails** → Claude proceeds to Phase 2.5 research and R3 solo. 1 remaining MCP call for R3 verdict.
  - **R3 Codex verdict fails** → Claude makes final decision solo. Present Scope Preservation Report + state: "Codex was unavailable for final verdict — this is Claude's unilateral synthesis based on all prior evidence."
  - **Multiple failures** → If 2+ MCP calls fail, switch to solo mode. Complete the debate structure (evidence → proposal → self-critique → defense → synthesis) without Codex. Mark output as "[Solo debate — Codex MCP unavailable]".
- **Early exit**: If Codex agrees fully in R1, skip to R3 — but STILL do Phase 1.5 research
- **Malformed response**: Ignore that round, continue
- **Session limit**: Max 2 debates per conversation (deeper than /tk, uses more context)
- **Phase timeout**: If Explore agents >2 min, output `⚠ PHASE [X] INCOMPLETE — [N findings gathered, M agents timed out]` and proceed.
- **Incomplete Phase Marking**: If ANY phase could not be fully completed (timeout, MCP failure, missing data), output `⚠ PHASE [X] INCOMPLETE — [reason]` inline. This marker is visible to the user and enables post-hoc quality assessment.

## Output Format

```
## Deep Debate: {topic}

### Phase 0 — Evidence Collection
{Evidence Base: data, metrics, root cause trace, git history, web findings, gaps, confidence}

### Phase 0.5 — State-of-the-Art Probe
{Codex web research findings on alternatives}

### Round 1 — Opening
**Claude**: {root-cause-backed proposal}
**Codex**: {critique with state-of-the-art challenge + ledger}

### Phase 1.5 — Expanded Investigation
{Verify + Expand + Connect — full findings}

### Round 2 — Deepening
**Claude**: {evidence-backed counterargument with new discoveries}
**Codex**: {re-critique with web research update + evidence review}

### Phase 2.5 — Pre-Synthesis Research
{Final evidence pass — open questions resolved, integration verified}

### Round 3 — Convergence
**Claude**: {Scope Preservation Report + evidence-grounded synthesis}
**Codex**: {verdict + scope delta + self-grade + research value assessment}

### Decision
{final decision with reasoning}
```

## Arguments

If called with arguments, use them as the debate topic.
If called without arguments, debate the current task or most recent discussion topic.

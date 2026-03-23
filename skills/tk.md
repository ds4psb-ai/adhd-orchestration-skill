---
name: tk
description: "Tiki-Taka v2: 2-round Claude↔Codex debate with SoTA probe, root cause tracing, and Position Lock. Use when user says /tk, tiki-taka, debate, or asks for Codex opinion."
---

# Tiki-Taka Debate v2 (2 Rounds) — Research-First Protocol

Run a structured 2-round debate between Claude (lead) and Codex (challenger) using the Codex CLI MCP. **Every debate MUST begin with deep research.** No debate should start from surface-level analysis.

**Why 2 rounds > 3 rounds:** Each round is a capitulation surface. Benchmark data (4/4 debates: compound capitulation at R2→R3) proves R3 removal improves scope preservation. 2 rounds force "one-shot" intensity from both sides.

## Usage

```
/tk <topic or question>
/tk              # debates the current task/context
```

## Prerequisites

- `codex-cli` MCP must be loaded (`mcp__codex-cli__codex`, `mcp__codex-cli__codex-reply`)
- If MCP is unavailable, inform the user and abort
- **MUST NOT pass `model` parameter** to any Codex MCP call. Codex CLI uses its own `~/.codex/config.toml` to select the model. Passing `model` breaks ChatGPT account auth.

## Architecture

```
Phase 0   (Claude deep research: 2-3 Explore + root cause + git history + web search)
  → Phase 0.5 (Codex SoTA web research)                    [mcp__codex-cli__codex — call #1]
    → Round 1 (Claude proposal → Codex 8-point critique)    [mcp__codex-cli__codex-reply — call #2]
      → Phase 1.5 MEGA (verify + expand + connect + pre-synthesis)
        → Round 2 FINAL (Claude defense+synthesis → Codex re-critique+verdict)  [mcp__codex-cli__codex-reply — call #3]
```

**MCP calls: 3** | **Debate rounds: 2** | **Research phases: 3** (0, 0.5, 1.5 MEGA)

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
- R2: Reference prior context — add only defense/synthesis delta. Do NOT resend prior rounds.
- R2 defense delta format (DO NOT resend full synthesis):
  1. Category A accepted: [list of R1 points + 1-line fix per point]
  2. Category C rejected: [list + 1-line evidence]
  3. Key changes from R1: [bullet list of what's NEW — e.g., "fire-and-forget → transactional outbox"]
  4. Position Lock statement (1-2 lines)
  5. Scope Preservation Report (table only, no detailed sub-components)
  Codex has full R1 context. Only send what CHANGED.

**Key principle:** Each Codex call should contain only NEW information. Prior context is preserved in the thread.

## Protocol

### Phase 0 — Evidence Collection (MANDATORY, before any Codex call)

**RULE: No Codex MCP call is permitted until Phase 0 is complete.** Even for short questions, you MUST gather evidence first.

**Steps:**

1. **Launch 2-3 Explore agents in parallel** to investigate the topic area deeply.
   - Agent 1: **Direct investigation** — read relevant source files, trace call paths, check schemas.
   - Agent 2: **Upstream investigation** — trace the ROOT of the pipeline/system. If the question is about X, investigate what FEEDS X and what X FEEDS INTO.
   - Agent 3 (if applicable): **Historical investigation** — git log/blame for relevant files. Look for patterns: repeated fixes, threshold churn, tuning spirals.

2. **Root Cause Probe** — Before forming your position, ask yourself:
   > "Is the proposed change more likely to introduce negatives than positives? What happens if we trace the problem to its true origin instead of patching the symptom?"

   This is NOT pessimism — it's the discipline that catches the 51st downstream patch before it's written.

3. **Web Search Gate** — Execute web search if ANY of these conditions are met:
   - The question involves a specific library/framework's **latest version** features.
   - APIs, policies, or best practices that may have changed after 2025-05 (Claude's training cutoff) are relevant.
   - The user explicitly uses recency keywords ("latest", "2026", "current", "recently", "new").
   - A technical decision depends on information that could have changed post-cutoff.
   - The question involves a **technical architecture or system design** decision.
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

**FORBIDDEN:** Calling `mcp__codex-cli__codex` without a completed Evidence Base. If you catch yourself about to skip Phase 0, STOP and investigate first.

### Phase 0.5 — Codex State-of-the-Art Probe

Before the debate begins, ask Codex to web-research whether better approaches exist.

**CHECKPOINT** — Before calling Codex, output the current debate state to the user:
> **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

**Call** `mcp__codex-cli__codex` with:
- `prompt`:
  ```
  I need your web research capabilities before we debate.

  Topic: {topic summary}
  Current approach: {brief description}

  ## Key Evidence (Claude's Phase 0 findings)
  {Structured bullet-list summary of evidence — key metrics, root cause, gaps. NOT verbose prose.}

  ## RESEARCH FOCUS (web search)

  1. **STATE-OF-THE-ART ALTERNATIVES**
     Search for better approaches to this class of problem (2025-2026).
     Include: anti-patterns, failure case studies, and how production systems actually solve this.
     For each finding: name, version, production adoption evidence, how it differs from current approach.
     If current approach IS state-of-the-art, confirm with evidence.

  2. **RECENCY CHECK**
     What changed in the last 12 months that affects this decision?
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
   - `thread_id`: saved threadId from Phase 0.5
   - `prompt`:
     ```
     Claude↔GPT debate. Your different training catches different things.

     Claude has done deep codebase research AND incorporated your Phase 0.5 web findings. Challenge INTERPRETATION, not absence of data.

     PROTOCOL: 2-round debate. After this, Claude investigates your points and responds ONE FINAL TIME. You then give ONE FINAL verdict. There is no Round 3. Front-load your best insights NOW — this is your only critique round.

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

     Be direct. Catch what Claude missed AND make the plan bolder. This is your ONE SHOT.
     ```

3. **Present** Codex's response to the user

### Phase 1.5 MEGA — Expanded Investigation + Pre-Synthesis

After Codex R1, do NOT just verify claims. **EXPAND investigation AND prepare for final synthesis** — this phase absorbs both Phase 1.5 and Phase 2.5 from the old protocol.

**Hard cap: 3 minutes.** If Explore agents exceed this, proceed with gathered evidence and note gaps.

**Four expansion vectors:**

1. **Verify** — For each verifiable Codex claim:
   - Questions whether a field/table/API exists → Check code or schema
   - Claims behavior differs from stated → Read implementation
   - Points out a data pattern → Run the query
   - Suggests a metric is wrong → Re-measure

2. **Expand** — For each NEW angle Codex introduced:
   - If Codex mentions a related subsystem → Investigate that subsystem
   - If Codex questions the root cause → Trace DEEPER upstream
   - If Codex suggests an alternative architecture → Check if components already exist in codebase
   - If Codex references a concept → Check DB schema, git history, config for related fields

3. **Connect** — For each indirect connection you discover:
   - Follow dependency chains (what calls this? what does this call?)
   - Check for related bugs/patterns in git history
   - Query DB for actual data that validates or invalidates combined hypothesis
   - Look for patterns: is this the Nth downstream patch? Are there tuning spirals?

4. **Pre-Synthesize** — Prepare for final round (absorbed from old Phase 2.5):
   - Identify open questions from R1 that are still unresolved
   - Check integration concerns: if Claude and Codex agreed on components from different angles, verify compatibility
   - Check edge cases: actual data for boundary conditions mentioned in debate
   - Run final DB/code verification for synthesis

**Process:**
1. List every verifiable claim AND new angle from Codex
2. Launch 2-3 Explore agents covering all four vectors
3. Run DB queries if relevant data exists
4. Compile results as Phase 1.5 MEGA Evidence Update

### Round 2 FINAL — Defense + Position Lock + Synthesis → Verdict

This is the FINAL exchange. No Round 3.

#### Claude's Response (SECTION A → POSITION LOCK → SECTION B)

**SECTION A — DEFENSE** (complete before moving to Section B)

**Pre-Defense Investigation** (60-second surgical check before filtering):
- Phase 1.5 MEGA findings marked "inconclusive" → one more targeted check
- Codex R1 points not fully verified → one final investigation
- Any MODIFY/CUT component → re-read actual implementation to confirm defense is grounded in current code
- Time cap: 60 seconds (surgical, not broad)

Respond to EVERY Codex R1 point with AGGRESSIVE filtering:
- **Category A (Accept)**: Concrete technical flaw with proof (API doesn't exist, ToS violation with specific clause, field genuinely missing from schema)
- **Category B (REJECT unless independently confirmed)**: Scope reduction framed as pragmatism ("simpler would work", "too complex", "Phase 1 should be smaller"). REJECT by default. Only accept if YOU find independent evidence.
- **Category C (REJECT)**: Generic risk aversion ("what if X fails", "might be too ambitious"). Reject outright.

**Phase 1.5 MEGA Integration**: For each point investigated:
- "Codex flagged [X] — I verified: [result]. [Accept/Reject with evidence]."
- "Codex introduced [Y] — I expanded investigation: [NEW findings]."
- "Connected investigation revealed [Z] — neither of us had seen this."

**DO NOT CAPITULATE.** This is your ONE AND ONLY defense opportunity. Maximum strength.

**POSITION LOCK** — Checkpoint between defense and synthesis:

> "After defense, my position is: [explicit statement]. Is this weaker than my R1 position? [yes/no + justification]. If yes, I must restore scope before proceeding to synthesis."

If the position is weaker than R1 without Category A evidence, STOP and restore before continuing.

**SECTION B — SYNTHESIS** (built on locked position, no retroactive weakening)

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
Debate delta: What changed because of cross-model debate?
Evidence delta: What new facts emerged from Phases 0/0.5/1.5 MEGA?
```

**RED FLAG**: If scope preserved <70%, either (a) the original proposal was genuinely flawed (cite Category A evidence), or (b) you capitulated — go back and restore Category B/C cuts.

Your synthesis should be AT LEAST as ambitious as your original proposal, improved by Codex's technical findings.

#### Codex's Final Verdict

**CHECKPOINT** — Before calling Codex, output the current debate state to the user:
> **Debate checkpoint saved.** If the next MCP call hangs (>20 min), press Escape/Ctrl+C. All work above is preserved.

**Call** `mcp__codex-cli__codex-reply` with:
- `thread_id`: saved threadId
- `prompt`:
  ```
  FINAL round. No more exchanges after this. Claude defended, locked position, and synthesized.

  {Claude's full response: Section A defense + Position Lock + Section B synthesis}

  ## PART 1 — RE-CRITIQUE (complete and lock before Part 2)
  (1) STILL WRONG: What's still technically broken? Propose fixes, not cuts.
  (2) EVIDENCE REVIEW: Each R1 claim — confirmed → fix, refuted → acknowledge, ambiguous → what settles it.
  (3) NEW EVIDENCE REACTION: Phase 1.5 MEGA discoveries neither side anticipated.
  (4) CONSERVATIVE BIAS AUTOPSY: Each R1 scope reduction → GENUINE INSIGHT (keep) or CONSERVATIVE REFLEX (retract + scope-preserving fix). >50% reflex → acknowledge bias.
  (5) AMBITION GAPS: Where is Claude STILL too conservative?

  ## PART 2 — FINAL VERDICT (Part 1 is locked — no retroactive changes)
  (1) AGREE or DISAGREE — state explicitly.
  (2) REMAINING RISKS: Technical risks only. "It's ambitious" is not a risk.
  (3) FINAL LEDGER with all components.
  (4) SCOPE DELTA: % ambition preserved, each CUT → impossibility or reflex, SELF-GRADE 1-10 conservative bias.
  (5) DEBATE VALUE: Genuine cross-model insight vs. generic risk aversion?
  (6) RESEARCH VALUE: Did Phase 0/0.5/1.5 MEGA evidence change outcome? How?
  ```

**Present** Codex's verdict to the user.

### Final Decision

- **If AGREE**: Adopt the synthesized position. Summarize the agreed approach.
- **If DISAGREE**: Claude makes the final call, explicitly stating where it overrides Codex and why.

## Anti-Deflation Guards (MUST)

### Claude's Obligations
1. **Default is KEEP, not CUT.** Burden of proof is on cutting, not on keeping.
2. **Defend your position.** If you believe in your proposal, fight for it. "Codex made a good point" is NOT sufficient reason to cut scope — state the specific technical evidence.
3. **Category B/C cuts are REJECTED by default.** Only Category A (concrete technical flaw with proof) changes the design.
4. **Phase ≠ Cut.** Phasing preserves the destination. If Codex says "do this later" but the "later" never has a path, it's a hidden cut — reject it.
5. **Ambition ratchet.** Your final synthesis should be at least as ambitious as your R1 proposal. If it's less ambitious, explain each reduction with Category A evidence.
6. **Research-first.** Every claim must be backed by Phase 0 evidence. Unsupported claims are weak claims — do the work before the debate.
7. **One-Shot Defense.** Round 2 is your ONLY defense opportunity. No holding back for a non-existent Round 3. Maximum intensity in Section A.

### Red Flags (self-check)
- Codex won R1 → You are likely about to capitulate in your ONE defense. Re-examine before responding.
- Scope <70% of R1 → You are likely capitulating. Restore Category B/C cuts.
- All Codex points accepted as "heterogeneous insight" → You stopped thinking critically.
- Zero components STRENGTHENED → The debate only subtracted, never added. That's deflation.
- Phase 0 was skipped or shallow → The entire debate is built on sand. STOP and research.
- **Position Lock violated** → Section B weakened position beyond what Section A established. Revert.
- **Conservative Bias Autopsy >50% REFLEX** → Codex's critique was mostly bias, not insight. Weight accordingly.

## Stability Guards

- **MCP hang detection**: Codex MCP calls have no built-in timeout. High-quality responses routinely take **10-18 minutes** — this is normal for GPT-5.4 xhigh reasoning. Only if a call exceeds **20 minutes** should the user consider it potentially hung.
  - Claude cannot detect a hang — the user must press **Escape (Ctrl+C)** to interrupt.
  - All work is preserved via checkpoints output before each MCP call.
  - After interrupt, apply the Phase-specific fallback below and continue the debate.
- **DO NOT rush Codex.** Long response time often correlates with higher quality output. Patience is rewarded.
- **Phase-specific fallbacks:**
  - **Phase 0.5 fails** → Claude performs its own web search (WebSearch tool) covering the 4 Research Dimensions. Mark as "[Claude web search — Codex probe unavailable]". Proceed to R1 with 2 remaining MCP calls.
  - **R1 Codex critique fails** → Claude performs self-critique using the 8-point framework, explicitly playing devil's advocate. Mark as "[Self-critique — Codex unavailable]". Proceed to Phase 1.5 MEGA, then R2 with 1 remaining MCP call.
  - **R2 Codex verdict fails** → Claude makes final decision solo. Present Scope Preservation Report + state: "Codex was unavailable for final verdict — this is Claude's unilateral synthesis based on all prior evidence."
  - **Multiple failures** → If 2+ MCP calls fail, switch to solo mode. Complete the debate structure (evidence → proposal → self-critique → defense → synthesis) without Codex. Mark output as "[Solo debate — Codex MCP unavailable]".
- **Early exit**: If Codex agrees in Round 1, end early — but STILL do Phase 1.5 MEGA research before final synthesis
- **Malformed response**: If Codex returns empty or broken output, ignore that round and continue
- **Session limit**: Max 3 debates per conversation (context management)
- **Phase 0 timeout**: If Explore agents take too long (>2 min), proceed with whatever evidence was gathered. Note the incomplete research in Evidence Base.
- **Phase 1.5 MEGA timeout**: Hard cap 3 minutes. Proceed with gathered evidence.

## Output Format

Present each phase clearly:

```
## Debate: {topic}

### Phase 0 — Evidence Collection
{Evidence Base: data, metrics, root cause trace, git history, web findings, gaps, confidence}

### Phase 0.5 — State-of-the-Art Probe
{Codex web research findings on alternatives}

### Round 1 — Opening
**Claude**: {root-cause-backed proposal with value statement}
**Codex**: {8-point critique with SoTA challenge + root cause challenge + ledger}

### Phase 1.5 MEGA — Expanded Investigation + Pre-Synthesis
{Verify + Expand + Connect + Pre-Synthesize — full findings}

### Round 2 FINAL — Defense + Synthesis → Verdict
**Claude Section A**: {Category A/B/C filtering + Phase 1.5 MEGA evidence}
**Claude Position Lock**: {position statement + R1 comparison}
**Claude Section B**: {Scope Preservation Report + synthesis}
**Codex Part 1**: {re-critique + evidence review + Conservative Bias Autopsy}
**Codex Part 2**: {verdict — AGREE/DISAGREE + final ledger + scope delta + self-grade + research value}

### Decision
{final decision with reasoning}
```

## Arguments

If called with arguments, use them as the debate topic.
If called without arguments, debate the current task, problem, or most recent discussion topic in context.

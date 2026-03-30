---
description: Save session checkpoint to memory for cross-session continuity
---

Save a checkpoint of the current session state. Analyze the conversation so far and create a checkpoint file with machine-readable JSON sidecar.

## Instructions

1. Analyze the current conversation to extract:
   - **Objective**: What was the user trying to accomplish?
   - **Progress**: Approximate completion percentage
   - **Completed**: What has been done so far (with commit hashes if available)
   - **In Progress**: What is currently being worked on
   - **Remaining**: What still needs to be done, with enough code-level detail to resume cold
   - **Failed Approaches**: What was tried and didn't work, and why
   - **Key Decisions**: Important decisions made during the session (debate conclusions, architecture choices, API selections — anything a fresh session CANNOT derive from code alone)
   - **Resume Point**: Exact next step to take when resuming (numbered steps, not prose)

2. Capture git state for SHA-based staleness:
   ```bash
   git rev-parse HEAD              # current SHA
   git diff --stat HEAD -- <key_files>  # uncommitted changes summary
   ```

3. Create a checkpoint file at:
   `/Users/ted/.claude-komission/projects/-Users-ted-komission/memory/checkpoints/YYYY-MM-DD-<topic>.md`

   Use today's date and a short kebab-case topic derived from the objective.

4. Markdown Format:
```markdown
# Checkpoint: <topic>
> Saved: YYYY-MM-DD HH:MM

## Objective
<one-line summary>

## Progress: XX%

## Completed
- <item with commit hash and exact file changes>

## In Progress
- <item with current state>

## Remaining
- <item with code-level detail: file paths, line numbers, code snippets if helpful>

## Failed Approaches
- <approach>: <why it failed>

## Key Decisions
<Debate conclusions, API provider selections, architecture choices — anything NOT derivable from reading the code. Include rationale. Use tables for structured comparisons.>

## Resume Point
<Numbered steps. First step should be immediately actionable without further research.>
1. ...
2. ...

## Key Files
- `path/to/file:line` — <why relevant>
```

5. **JSON Sidecar** — Create a machine-readable companion file at:
   `/Users/ted/.claude-komission/projects/-Users-ted-komission/memory/checkpoints/YYYY-MM-DD-<topic>.json`

   JSON Schema:
   ```json
   {
     "topic": "<kebab-case-topic>",
     "objective": "<one-line>",
     "progress_pct": 75,
     "base_sha": "<git HEAD at checkpoint time>",
     "domain": "<primary domain: vdg|frontend|backend|mobile|infra|...>",
     "key_files": [
       {"path": "path/to/file.py", "sha": "<file-level SHA or HEAD>", "role": "<why relevant>"}
     ],
     "completed": ["<item 1>", "<item 2>"],
     "remaining": ["<item 1>", "<item 2>"],
     "blockers": ["<blocker if any>"],
     "resume_steps": ["<step 1>", "<step 2>"],
     "adhd_run_id": "<run-id if part of ADHD run, null otherwise>",
     "stream_id": "<stream-id if part of ADHD stream, null otherwise>",
     "verification_status": {
       "tests_pass": true,
       "build_pass": true,
       "last_verify": "<timestamp or null>"
     },
     "saved_at": "YYYY-MM-DDTHH:MM:SSZ"
   }
   ```

   **SHA-Based Staleness**: Future sessions can check staleness by comparing:
   - `base_sha` vs current HEAD → any commits since checkpoint?
   - `key_files[].sha` vs current file SHA → key files changed?
   - If either differs → checkpoint is **stale** (code changed since save)

6. **ADHD Run Integration**: If the current session is part of an ADHD run:
   - Set `adhd_run_id` and `stream_id` in the JSON sidecar
   - Update the stream state file at `.claude/state/adhd/runs/<run-id>/checkpoints/<stream-id>.json`
   - Include acceptance criteria status from the stream

7. **Resume Comment**: After saving, output a short copy-paste block the user can paste into the next session to resume instantly:
```
Continue <topic> Phase X.

Checkpoint: Read memory/checkpoints/YYYY-MM-DD-<topic>.md and start.

<1-2 line summary of what's done and what's next>
```

8. Update `MEMORY.md` checkpoint index with a one-line entry.

9. Confirm to the user that the checkpoint was saved and show both file paths (markdown + JSON).

## Observability

Append a one-line entry to `~/.claude/adhd-runs.jsonl` if this checkpoint is part of an ADHD run:
```json
{"event": "checkpoint", "run_id": "<id>", "stream_id": "<id>", "topic": "<topic>", "progress_pct": 75, "base_sha": "<sha>", "timestamp": "YYYY-MM-DDTHH:MM:SSZ"}
```

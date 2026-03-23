---
name: verify-implementation
description: Use when integrated verification is required after code changes with adaptive, diff-aware coverage
---

# Verify Implementation

## Purpose
- Enforce integrated verification based on change scope just before implementation is complete.
- Operate a hybrid of a fixed checklist + dynamic registry (self-extending).
- Leave evidence of "failed before fix / passed after fix" through Before/After revalidation.

## Execution Plan
1. Pre-Scan:
Synchronize the registry to latest using `manage-skills`.
`python3 .claude/skills/manage-skills/scripts/skill_registry_sync.py --base HEAD~1 --head HEAD --write`
2. Check Selection:
Select checks from the dynamic registry that match changed files.
3. Verification Run:
Execute the selected check commands sequentially.
`python3 .claude/skills/verify-implementation/scripts/run_registry_checks.py --base HEAD~1 --head HEAD --report-path .claude/reports/verify-implementation-latest.md --json`
4. Before/After Revalidation:
Re-run critical failure scenarios to confirm regression prevention.
5. Evidence Report:
Leave execution evidence in the output format below.

## Decision Rules
1. Always execute checks with `status=active`.
2. For `status=proposed` checks, decide on promotion after at least one manual verification.
3. A check without `evidence` is considered a verification gap.
4. Do not delete newly auto-generated checks; enhance their commands and retain them.

## Pseudocode
```text
registry = load_dynamic_registry()
targets = select_checks(changed_files, status in [active, proposed])

before = run(targets)
apply_fixes_if_needed()
after = run(targets)

assert after.failures <= before.failures
publish_report(before, after, targets)
```

## Output Format
```markdown
## Verification Evidence
- changed_files: <N>
- executed_checks: <N>
- before_failures: <N>
- after_failures: <N>

### Executed Checks
| check_id | command | result | evidence |
| --- | --- | --- | --- |
| backend-pytest | ... | pass | pytest summary |

### Regression Gate
- monotonic_coverage: pass|fail
- unresolved_checks: [check_id, ...]
```

## Exceptions
- For infra/ops-only changes (`infra/**`), auto-generated checks are temporarily allowed as `proposed`.
- For lint/format-only changes, tests can be skipped, but build/type checks must be retained.
- If a failure is caused by an external API outage, document the failure cause and record a re-run plan.

## Dynamic Coverage Registry

Populate this registry with your project's checks. The `skill_registry_sync.py` script auto-extends it when new files are changed.

<!-- REGISTRY:START -->
| check_id | trigger_patterns | verification_command | evidence | status | last_updated |
| --- | --- | --- | --- | --- | --- |
| backend-pytest | backend/** | cd backend && python3 -m pytest tests/ -v --tb=short | baseline | active | 2026-01-01 |
| frontend-build | frontend/** | cd frontend && npm run build | baseline | active | 2026-01-01 |
| frontend-typecheck | frontend/src/** | cd frontend && npm run typecheck | baseline | active | 2026-01-01 |
<!-- REGISTRY:END -->

<!-- Origin: https://github.com/ds4psb-ai/adhd-orchestration-skill | License: MIT + Attribution | (c) 2026 ds4psb-ai -->

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

<!-- REGISTRY:START -->
| check_id | trigger_patterns | verification_command | evidence | status | last_updated |
| --- | --- | --- | --- | --- | --- |
| backend-pytest | backend/** | cd backend && source venv/bin/activate && python3 -m pytest tests/ -v --tb=short | baseline;matched:backend/Dockerfile;matched:backend/app/main.py;matched:backend/app/routers/auth.py;matched:backend/app/routers/coaching.py;matched:backend/app/routers/crew/challenges.py;matched:backend/app/routers/crew/main.py;matched:backend/app/routers/for_you.py;matched:backend/app/routers/outlier_promotion.py;matched:backend/app/routers/zodiac.py;matched:backend/app/schemas/crawled_video.py;matched:backend/app/schemas/lineage.py;matched:backend/app/schemas/storyteller.py;matched:backend/app/schemas/unified_pass_response_schema.py;matched:backend/app/schemas/vdg_unified_pass.py;matched:backend/app/schemas/vdg_v4.py;matched:backend/app/services/lineage_projection_service.py;matched:backend/app/services/lineage_view_service.py;matched:backend/app/services/public_constellation_insights.py;matched:backend/app/services/storyteller_service.py;matched:backend/app/services/tiktok_metadata.py;matched:backend/app/services/vdg_pipeline/converter.py;matched:backend/app/services/vdg_stuck_recovery.py;matched:backend/tests/test_stuck_recovery_dispatch.py | active | 2026-03-23 |
| frontend-build | frontend/** | cd frontend && bun run build | baseline;matched:frontend/src/app/actions/crew/campaigns.ts;matched:frontend/src/components/zodiac/zodiacDetailUtils.ts;matched:frontend/src/hooks/useCoachingWebSocket.ts;matched:frontend/src/hooks/useCrewLive.ts;matched:frontend/src/hooks/useCrewSSE.ts;matched:frontend/src/lib/api/types/zodiac.ts;matched:frontend/src/lib/server-auth.ts;matched:frontend/src/components/UnifiedOutlierCard.tsx;matched:frontend/src/components/outlier/XEmbedCard.tsx;matched:frontend/src/components/patterns/sections/VideosSection.tsx;matched:frontend/src/components/public-funnel/PublicForYouFunnelPage.tsx;matched:frontend/src/hooks/useTwitterWidgets.ts;matched:frontend/src/app/crew/page.tsx;matched:frontend/scripts/check-class-contract.js;matched:frontend/src/components/outlier/TikTokPlayer.tsx | active | 2026-03-23 |
| frontend-typecheck | frontend/src/**<br>frontend/messages/** | cd frontend && bun run typecheck | baseline | active | 2026-02-13 |
| i18n-sync | frontend/messages/** | cd frontend && jq -e . messages/ko.json >/dev/null && jq -e . messages/en.json >/dev/null | baseline | active | 2026-02-13 |
| api-contract-sync | backend/app/routers/**<br>backend/app/schemas/**<br>frontend/src/lib/api.ts | grep -rn -e 'router\.' -e 'BaseModel' -e 'interface' -e 'type' backend/app frontend/src/lib/api.ts | baseline | active | 2026-03-23 |
| vdg-schema-ssot | backend/app/** | grep -rn 'vdg_data\.get(' backend/app | baseline | active | 2026-03-23 |
| migration-safety | backend/alembic/**<br>backend/app/models/** | cd backend && source venv/bin/activate && python3 -m pytest tests/ -k migration -v --tb=short | baseline | active | 2026-02-13 |
| docs-consistency | docs/**<br>.claude/docs/** | grep -rn -e 'TODO' -e 'FIXME' docs .claude/docs | baseline | active | 2026-03-23 |
| auto-claude-commands-verify-md | .claude/commands/** | grep -n -e 'skill_registry_sync.py' -e 'run_registry_checks.py' .claude/commands/review.md .claude/commands/test.md .claude/commands/verify.md | matched:.claude/commands/verify.md;matched:.claude/commands/review.md;matched:.claude/commands/test.md | active | 2026-03-23 |
| auto-claude-skills-manage-skills-skill-md | .claude/skills/** | python3 .claude/skills/manage-skills/scripts/skill_registry_sync.py --help >/dev/null && python3 .claude/skills/verify-implementation/scripts/run_registry_checks.py --help >/dev/null | matched:.claude/skills/manage-skills/SKILL.md;matched:.claude/skills/verify-implementation/SKILL.md;matched:.claude/skills/manage-skills/scripts/skill_registry_sync.py;matched:.claude/skills/verify-implementation/scripts/run_registry_checks.py | active | 2026-02-13 |
| auto-tests-test-skill-registry-sync-py | tests/test_skill_registry_sync.py | source backend/venv/bin/activate && python -m pytest tests/test_skill_registry_sync.py -v --tb=short | matched:tests/test_skill_registry_sync.py | active | 2026-02-13 |
| auto-tests-test-run-registry-checks-py | tests/test_run_registry_checks.py | source backend/venv/bin/activate && python -m pytest tests/test_run_registry_checks.py -v --tb=short | matched:tests/test_run_registry_checks.py | active | 2026-02-13 |
| verify-hardening-patterns | backend/app/services/**<br>backend/app/routers/** | grep -rn 'async def ' backend/app/services/ backend/app/routers/ --include='*.py' | baseline | active | 2026-03-23 |
| auto-github-workflows-ci-yml | .github/workflows/** | manual verification required | matched:.github/workflows/ci.yml | proposed | 2026-03-16 |
| auto-mobile-env-example | mobile/.env.example | cd mobile && bun run test | matched:mobile/.env.example | proposed | 2026-03-16 |
| auto-mobile-app-layout-tsx | mobile/app/** | cd mobile && bun run test | matched:mobile/app/_layout.tsx;matched:mobile/app/camera.tsx;matched:mobile/app/index.tsx;matched:mobile/app/shoot.tsx | active | 2026-03-16 |
| auto-mobile-bun-lock | mobile/bun.lock | cd mobile && bun run test | matched:mobile/bun.lock | proposed | 2026-03-16 |
| auto-mobile-package-json | mobile/package.json | cd mobile && bun run test | matched:mobile/package.json | proposed | 2026-03-16 |
| auto-mobile-src-components-errorboundary-tsx | mobile/src/** | cd mobile && bun run test | matched:mobile/src/components/ErrorBoundary.tsx;matched:mobile/src/lib/apiClient.ts;matched:mobile/src/lib/auth.ts | active | 2026-03-16 |
| verify-visual-regression | frontend/src/pages/**/*.tsx | cd frontend && npx playwright test e2e/visual/ --reporter=list | baseline | active | 2026-03-22 |
| verify-a11y | frontend/src/components/**/*.tsx | cd frontend && npx playwright test e2e/a11y.spec.ts --reporter=list | baseline | proposed | 2026-03-23 |
<!-- REGISTRY:END -->

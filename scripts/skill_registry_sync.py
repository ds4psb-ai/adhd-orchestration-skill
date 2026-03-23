#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from fnmatch import fnmatch
from pathlib import Path


REGISTRY_START = "<!-- REGISTRY:START -->"
REGISTRY_END = "<!-- REGISTRY:END -->"
DEFAULT_SKILL_FILE = Path(".claude/skills/verify-implementation/SKILL.md")


@dataclass
class RegistryRow:
    check_id: str
    trigger_patterns: str
    verification_command: str
    evidence: str
    status: str
    last_updated: str


def _extract_registry_block(skill_doc: str) -> tuple[str, str, str]:
    start = skill_doc.find(REGISTRY_START)
    end = skill_doc.find(REGISTRY_END)
    if start < 0 or end < 0 or end < start:
        raise ValueError("Registry markers are missing from skill document.")
    prefix = skill_doc[: start + len(REGISTRY_START)]
    block = skill_doc[start + len(REGISTRY_START) : end]
    suffix = skill_doc[end:]
    return prefix, block, suffix


def _split_cells(markdown_row: str) -> list[str]:
    return [cell.strip() for cell in markdown_row.strip().strip("|").split("|")]


def _parse_registry_rows(block: str) -> list[RegistryRow]:
    rows = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(rows) < 2:
        return []

    headers = _split_cells(rows[0])
    expected = {
        "check_id",
        "trigger_patterns",
        "verification_command",
        "evidence",
        "status",
        "last_updated",
    }
    if set(headers) != expected:
        raise ValueError("Registry table headers are invalid or incomplete.")

    parsed: list[RegistryRow] = []
    for line in rows[2:]:
        cells = _split_cells(line)
        if len(cells) != len(headers):
            continue
        item = dict(zip(headers, cells))
        parsed.append(
            RegistryRow(
                check_id=item["check_id"],
                trigger_patterns=item["trigger_patterns"],
                verification_command=item["verification_command"],
                evidence=item["evidence"],
                status=item["status"],
                last_updated=item["last_updated"],
            )
        )
    return parsed


def _render_registry_rows(rows: list[RegistryRow]) -> str:
    table = [
        "| check_id | trigger_patterns | verification_command | evidence | status | last_updated |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        table.append(
            "| "
            + " | ".join(
                [
                    row.check_id,
                    row.trigger_patterns,
                    row.verification_command,
                    row.evidence,
                    row.status,
                    row.last_updated,
                ]
            )
            + " |"
        )
    return "\n" + "\n".join(table) + "\n"


def _split_patterns(raw_patterns: str) -> list[str]:
    return [pattern.strip() for pattern in re.split(r"<br>|,", raw_patterns) if pattern.strip()]


def _row_matches_path(row: RegistryRow, changed_file: str) -> bool:
    return any(fnmatch(changed_file, pattern) for pattern in _split_patterns(row.trigger_patterns))


def _slugify_path(path: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", path).strip("-").lower()
    return normalized or "path"


def _infer_trigger_pattern(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    if len(parts) == 2 and "." in parts[1]:
        return f"{parts[0]}/{parts[1]}"
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}/**"
    if parts:
        return f"{parts[0]}/**"
    return "**"


def _infer_verification_command(path: str) -> str:
    if path.startswith("backend/"):
        return "cd backend && source venv/bin/activate && python3 -m pytest tests/ -v --tb=short"
    if path.startswith("frontend/"):
        return "cd frontend && bun run build && bun run typecheck"
    if path.startswith("mobile/"):
        return "cd mobile && bun run test"
    if path.startswith("docs/"):
        return "rg -n \"TODO|FIXME\" docs/"
    return "manual verification required"


def _next_auto_check_id(path: str, rows: list[RegistryRow]) -> str:
    base = f"auto-{_slugify_path(path)}"
    existing = {row.check_id for row in rows}
    if base not in existing:
        return base

    index = 2
    while f"{base}-{index}" in existing:
        index += 1
    return f"{base}-{index}"


def _merge_evidence(existing: str, new_item: str) -> str:
    cleaned = [item.strip() for item in existing.split(";") if item.strip()]
    if new_item not in cleaned:
        cleaned.append(new_item)
    return ";".join(cleaned)


def sync_registry(skill_doc: str, changed_files: list[str], date_str: str | None = None) -> tuple[str, dict]:
    effective_date = date_str or date.today().isoformat()
    unique_files = sorted({path.strip() for path in changed_files if path.strip()})
    if not unique_files:
        return skill_doc, {"changed_files": 0, "matched_count": 0, "created_count": 0}

    prefix, block, suffix = _extract_registry_block(skill_doc)
    rows = _parse_registry_rows(block)
    if not rows:
        raise ValueError("Registry table must include at least one data row.")

    matched_count = 0
    created_count = 0

    for changed_file in unique_files:
        matched_row = next((row for row in rows if _row_matches_path(row, changed_file)), None)
        if matched_row:
            matched_count += 1
            matched_row.evidence = _merge_evidence(matched_row.evidence, f"matched:{changed_file}")
            if matched_row.verification_command.strip().lower() == "manual verification required":
                matched_row.status = "proposed"
            else:
                matched_row.status = "active"
            matched_row.last_updated = effective_date
            continue

        created_count += 1
        rows.append(
            RegistryRow(
                check_id=_next_auto_check_id(changed_file, rows),
                trigger_patterns=_infer_trigger_pattern(changed_file),
                verification_command=_infer_verification_command(changed_file),
                evidence=f"matched:{changed_file}",
                status="proposed",
                last_updated=effective_date,
            )
        )

    updated = prefix + _render_registry_rows(rows) + suffix
    report = {
        "changed_files": len(unique_files),
        "matched_count": matched_count,
        "created_count": created_count,
    }
    return updated, report


def _git_changed_files(base: str, head: str) -> list[str]:
    command = ["git", "diff", "--name-only", f"{base}..{head}"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Synchronize verify-implementation coverage registry using git diff.",
    )
    parser.add_argument(
        "--skill-file",
        default=str(DEFAULT_SKILL_FILE),
        help="Path to the verify skill file containing registry markers.",
    )
    parser.add_argument("--base", default="HEAD~1", help="Git base revision for diff.")
    parser.add_argument("--head", default="HEAD", help="Git head revision for diff.")
    parser.add_argument(
        "--changed-file",
        dest="changed_files",
        action="append",
        default=None,
        help="Explicit changed file path. Repeat for multiple files.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the updated registry back to --skill-file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable sync report as JSON.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    skill_path = Path(args.skill_file)
    skill_doc = skill_path.read_text(encoding="utf-8")

    changed_files = args.changed_files
    if changed_files is None:
        changed_files = _git_changed_files(args.base, args.head)

    updated, report = sync_registry(skill_doc, changed_files)
    has_changes = updated != skill_doc

    if args.write and has_changes:
        skill_path.write_text(updated, encoding="utf-8")

    if args.json:
        print(json.dumps(report, ensure_ascii=False))
    else:
        print(f"changed_files={report['changed_files']}")
        print(f"matched_count={report['matched_count']}")
        print(f"created_count={report['created_count']}")
        print(f"updated={str(has_changes).lower()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

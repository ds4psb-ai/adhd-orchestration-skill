#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path


REGISTRY_START = "<!-- REGISTRY:START -->"
REGISTRY_END = "<!-- REGISTRY:END -->"
DEFAULT_SKILL_FILE = Path(".claude/skills/verify-implementation/SKILL.md")
DEFAULT_REPORT_PATH = Path(".claude/reports/verify-implementation-latest.md")


@dataclass
class RegistryRow:
    check_id: str
    trigger_patterns: str
    verification_command: str
    evidence: str
    status: str
    last_updated: str


def _extract_registry_block(skill_doc: str) -> str:
    start = skill_doc.find(REGISTRY_START)
    end = skill_doc.find(REGISTRY_END)
    if start < 0 or end < 0 or end < start:
        raise ValueError("Registry markers are missing from verify skill document.")
    return skill_doc[start + len(REGISTRY_START) : end]


def _split_cells(markdown_row: str) -> list[str]:
    return [cell.strip() for cell in markdown_row.strip().strip("|").split("|")]


def parse_registry(skill_doc: str) -> list[RegistryRow]:
    block = _extract_registry_block(skill_doc)
    rows = [line.strip() for line in block.splitlines() if line.strip().startswith("|")]
    if len(rows) < 2:
        return []

    headers = _split_cells(rows[0])
    required = [
        "check_id",
        "trigger_patterns",
        "verification_command",
        "evidence",
        "status",
        "last_updated",
    ]
    if sorted(headers) != sorted(required):
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


def _split_patterns(raw_patterns: str) -> list[str]:
    return [pattern.strip() for pattern in re.split(r"<br>|,", raw_patterns) if pattern.strip()]


def _matches_any_path(row: RegistryRow, changed_files: list[str]) -> bool:
    patterns = _split_patterns(row.trigger_patterns)
    for changed_file in changed_files:
        if any(fnmatch(changed_file, pattern) for pattern in patterns):
            return True
    return False


def select_checks(
    rows: list[RegistryRow],
    changed_files: list[str],
    include_all_active: bool = False,
) -> list[RegistryRow]:
    effective_changed = [path for path in changed_files if path]
    selected: list[RegistryRow] = []
    selected_ids: set[str] = set()

    def add_row(row: RegistryRow) -> None:
        if row.check_id in selected_ids:
            return
        selected.append(row)
        selected_ids.add(row.check_id)

    if effective_changed:
        for row in rows:
            if row.status not in {"active", "proposed"}:
                continue
            if _matches_any_path(row, effective_changed):
                add_row(row)
        if include_all_active:
            for row in rows:
                if row.status == "active":
                    add_row(row)
        return selected

    for row in rows:
        if row.status == "active":
            add_row(row)
    return selected


def execute_check(row: RegistryRow, shell: str = "/bin/zsh") -> dict:
    command = row.verification_command.strip()
    if command.lower() == "manual verification required":
        return {
            "check_id": row.check_id,
            "command": command,
            "result": "manual",
            "exit_code": 0,
            "output": "manual verification required",
            "status": row.status,
        }

    result = subprocess.run(
        [shell, "-lc", command],
        capture_output=True,
        text=True,
        check=False,
    )
    combined_output = "\n".join(part for part in [result.stdout.strip(), result.stderr.strip()] if part).strip()
    return {
        "check_id": row.check_id,
        "command": command,
        "result": "pass" if result.returncode == 0 else "fail",
        "exit_code": result.returncode,
        "output": combined_output,
        "status": row.status,
    }


def _render_markdown_report(changed_files: list[str], results: list[dict]) -> str:
    pass_count = sum(1 for item in results if item["result"] == "pass")
    fail_count = sum(1 for item in results if item["result"] == "fail")
    manual_count = sum(1 for item in results if item["result"] == "manual")
    lines = [
        "# Verification Evidence",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- changed_files: {len(changed_files)}",
        f"- executed_checks: {len(results)}",
        f"- pass_count: {pass_count}",
        f"- fail_count: {fail_count}",
        f"- manual_count: {manual_count}",
        "",
        "## Executed Checks",
        "",
        "| check_id | status | result | exit_code |",
        "| --- | --- | --- | --- |",
    ]
    for item in results:
        lines.append(
            f"| {item['check_id']} | {item['status']} | {item['result']} | {item['exit_code']} |"
        )
    lines.append("")
    lines.append("## Changed Files")
    lines.append("")
    if changed_files:
        for path in changed_files:
            lines.append(f"- `{path}`")
    else:
        lines.append("- (none)")
    lines.append("")
    lines.append("## Output Snippets")
    lines.append("")
    for item in results:
        snippet = item["output"] or "(no output)"
        lines.append(f"### {item['check_id']}")
        lines.append("```text")
        lines.append(snippet)
        lines.append("```")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def _git_changed_files(base: str, head: str) -> list[str]:
    command = ["git", "diff", "--name-only", f"{base}..{head}"]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run verify-implementation checks selected from the dynamic registry.",
    )
    parser.add_argument("--skill-file", default=str(DEFAULT_SKILL_FILE), help="Path to verify skill file.")
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
        "--include-all-active",
        action="store_true",
        help="Include all active checks in addition to changed-file matches.",
    )
    parser.add_argument(
        "--report-path",
        default=str(DEFAULT_REPORT_PATH),
        help="Markdown report output path.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON summary.")
    parser.add_argument(
        "--fail-on-manual",
        action="store_true",
        help="Return non-zero if manual checks are selected.",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    skill_doc = Path(args.skill_file).read_text(encoding="utf-8")
    rows = parse_registry(skill_doc)

    changed_files = args.changed_files
    if changed_files is None:
        changed_files = _git_changed_files(args.base, args.head)

    selected = select_checks(rows, changed_files, include_all_active=args.include_all_active)
    results = [execute_check(row) for row in selected]
    report_text = _render_markdown_report(changed_files, results)

    report_path = Path(args.report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")

    pass_count = sum(1 for item in results if item["result"] == "pass")
    fail_count = sum(1 for item in results if item["result"] == "fail")
    manual_count = sum(1 for item in results if item["result"] == "manual")

    summary = {
        "changed_files": len(changed_files),
        "executed_checks": len(results),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "manual_count": manual_count,
        "report_path": str(report_path),
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(f"changed_files={summary['changed_files']}")
        print(f"executed_checks={summary['executed_checks']}")
        print(f"pass_count={summary['pass_count']}")
        print(f"fail_count={summary['fail_count']}")
        print(f"manual_count={summary['manual_count']}")
        print(f"report_path={summary['report_path']}")

    if fail_count > 0:
        return 1
    if args.fail_on_manual and manual_count > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

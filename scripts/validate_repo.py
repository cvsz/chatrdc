#!/usr/bin/env python3
"""Validate ztemplate structure and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

# Directories whose contents are generated, cached, or third-party and must not
# be treated as repository-owned Markdown. Skipping them avoids false-positive
# broken-link reports in local environments (for example, a present .venv) and
# keeps validation focused on repository-owned documentation.
SKIPPED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".cache",
    "build",
    "dist",
    "coverage",
    "node_modules",
    ".next",
    ".nuxt",
    ".out",
    "tmp",
    ".tmp",
}


def _is_skipped_dir(path: Path, root: Path = ROOT) -> bool:
    try:
        relative = path.relative_to(root.resolve())
    except ValueError:
        return True
    return any(part in SKIPPED_DIRS for part in relative.parts)


REQUIRED_PATHS = (
    "README.md",
    "ABOUT.md",
    "AGENTS.md",
    "CLAUDE.md",
    "OPENCODE.md",
    "ZEAZ-INTRODUCTION.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "IMPLEMENTATION-CHECKLIST.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    "docs/ai/README.md",
    "docs/ai/guides",
    "docs/ai/playbooks",
    "docs/ai/prompts",
    "skills/zeaz-skill-finder/SKILL.md",
    "components.d/zeaz-engineering.yml",
    "plugins.d/zeaz-skills.yml",
    "ecc-install.json",
    "scripts/github_admin.py",
    "docs/ai/guides/github-repository-admin.md",
)

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "#", "data:")


def validate_required_paths(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")
    return errors


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target)


def validate_markdown_links(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for md in sorted(root.rglob("*.md")):
        if _is_skipped_dir(md, root):
            continue
        text = md.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith(SKIP_PREFIXES):
                continue
            target = normalize_link_target(raw)
            if not target:
                continue
            link_base = (
                root
                if md.relative_to(root).as_posix() == "templates/project-readme.md"
                else md.parent
            )
            resolved = (link_base / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{md.relative_to(root)}: link escapes repository: {raw}")
                continue
            if not resolved.exists():
                errors.append(f"{md.relative_to(root)}: broken local link: {raw}")
    return errors


def main() -> int:
    errors = validate_required_paths() + validate_markdown_links()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Repository structure and local Markdown links are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

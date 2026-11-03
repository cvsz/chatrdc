"""Tests for scripts/validate_repo.py repository baseline validation."""

from __future__ import annotations

import tempfile
from pathlib import Path

from scripts.validate_repo import validate_markdown_links


def _write(root: Path, relative: str, content: str) -> Path:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def test_repo_owned_broken_link_is_reported():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write(root, "README.md", "# repo\nsee [missing](./does-not-exist.md)\n")
        errors = validate_markdown_links(root)
        assert any("broken local link: ./does-not-exist.md" in error for error in errors)


def test_repo_owned_valid_link_is_not_reported():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write(root, "README.md", "# repo\nsee [sibling](./sibling.md)\n")
        _write(root, "sibling.md", "# sibling\n")
        errors = validate_markdown_links(root)
        assert not errors


def test_generated_directory_broken_links_are_skipped():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write(root, "README.md", "# repo\nok\n")
        _write(
            root,
            ".venv/lib/python3.14/site-packages/pkg/README.md",
            "# pkg\nsee [missing](./nope.md)\n",
        )
        _write(root, "build/output.md", "# build\nsee [missing](./nope.md)\n")
        errors = validate_markdown_links(root)
        assert not any("nope.md" in error for error in errors)


def test_absolute_and_external_links_are_not_flagged():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        _write(
            root,
            "README.md",
            "# repo\nsee [external](https://example.com) and [anchor](#section)\n",
        )
        errors = validate_markdown_links(root)
        assert not errors

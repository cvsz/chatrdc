from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_workflow_security import scan_workflows


class WorkflowSecurityTests(unittest.TestCase):
    def scan(self, workflow: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "test.yml").write_text(workflow, encoding="utf-8")
            return scan_workflows(root)

    def test_read_only_pull_request_checkout_is_allowed(self) -> None:
        findings = self.scan(
            """name: CI
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
        with:
          persist-credentials: false
"""
        )
        self.assertEqual(findings, [])

    def test_pull_request_secrets_are_rejected(self) -> None:
        findings = self.scan(
            """name: Unsafe
on:
  pull_request:
permissions:
  contents: read
jobs:
  test:
    steps:
      - run: echo ${{ secrets.PRIVATE_TOKEN }}
"""
        )
        self.assertTrue(any("must not reference secrets" in item for item in findings))

    def test_pull_request_write_permissions_are_rejected(self) -> None:
        findings = self.scan(
            """name: Unsafe
on:
  pull_request:
permissions:
  contents: write
jobs:
  test:
    steps:
      - run: echo test
"""
        )
        self.assertTrue(any("unsafe write permission" in item for item in findings))

    def test_job_level_pull_request_write_permissions_are_rejected(self) -> None:
        findings = self.scan(
            """name: Unsafe
on:
  pull_request:
jobs:
  test:
    permissions:
      pull-requests: write
    steps:
      - run: echo test
"""
        )
        self.assertTrue(any("must not request write permissions" in item for item in findings))

    def test_codeql_security_events_permission_is_allowed_only_for_codeql(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workflows = root / ".github" / "workflows"
            workflows.mkdir(parents=True)
            (workflows / "codeql.yml").write_text(
                """name: CodeQL
on:
  pull_request:
permissions:
  contents: read
  security-events: write
jobs:
  analyze:
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
        with:
          persist-credentials: false
""",
                encoding="utf-8",
            )
            self.assertEqual(scan_workflows(root), [])

    def test_pull_request_target_is_rejected(self) -> None:
        findings = self.scan(
            """name: Unsafe
on:
  pull_request_target:
jobs:
  test:
    steps:
      - run: echo test
"""
        )
        self.assertTrue(any("pull_request_target is forbidden" in item for item in findings))

    def test_secret_and_untrusted_ref_combination_is_rejected(self) -> None:
        findings = self.scan(
            """name: Unsafe
on:
  workflow_dispatch:
jobs:
  review:
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
        with:
          ref: ${{ github.event.inputs.sha }}
      - run: ./scripts/from-the-pr.sh
        env:
          GH_TOKEN: ${{ secrets.REVIEWER_PAT }}
"""
        )
        self.assertTrue(any("combines secrets with a PR-controlled" in item for item in findings))

    def test_secretless_operator_selected_pr_ref_is_allowed(self) -> None:
        findings = self.scan(
            """name: Read-only scan
on:
  workflow_dispatch:
jobs:
  inspect:
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@0123456789012345678901234567890123456789
        with:
          ref: ${{ github.event.inputs.pr_number && format('refs/pull/{0}/merge', github.event.inputs.pr_number) }}
          persist-credentials: false
      - run: git status --short
"""
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()

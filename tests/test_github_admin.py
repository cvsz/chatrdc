from scripts.github_admin import REQUIRED_CHECKS, protection_payload


def test_required_checks_cover_linux_and_windows_python_ci():
    assert "repository-baseline" in REQUIRED_CHECKS
    assert "python" in REQUIRED_CHECKS
    assert "windows-python" in REQUIRED_CHECKS
    assert "dependency-review" in REQUIRED_CHECKS
    assert "Analyze Python and GitHub Actions" in REQUIRED_CHECKS


def test_branch_protection_requires_independent_review_and_strict_checks():
    payload = protection_payload()

    assert payload["required_status_checks"]["strict"] is True
    assert set(payload["required_status_checks"]["contexts"]) == set(REQUIRED_CHECKS)
    reviews = payload["required_pull_request_reviews"]
    assert reviews["required_approving_review_count"] == 1
    assert reviews["dismiss_stale_reviews"] is True
    assert reviews["require_code_owner_reviews"] is True
    assert reviews["require_last_push_approval"] is True
    assert payload["enforce_admins"] is True
    assert payload["allow_force_pushes"] is False
    assert payload["allow_deletions"] is False

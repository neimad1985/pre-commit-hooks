from pathlib import Path
from textwrap import dedent

import pytest

from conftest import HookRunner, run_git


def reference_template(hooks_repository: Path, hook_ids: list[str]) -> str:
    hooks = "".join(f"          - id: {hook_id}\n" for hook_id in hook_ids)
    return f"repos:\n  - repo: {hooks_repository}\n    rev: {{rev}}\n    hooks:\n{hooks}"


def publish(hooks_repository: Path, hook_ids: list[str], tag: str) -> None:
    (hooks_repository / "reference" / "pre-commit-config.yaml").write_text(reference_template(hooks_repository, hook_ids))
    run_git(hooks_repository, "add", "reference")
    run_git(hooks_repository, "commit", "--message", tag)
    run_git(hooks_repository, "tag", tag)


@pytest.fixture
def hooks_repository(tmp_path: Path) -> Path:
    """Faux dépôt de hooks local qui remplace GitHub : v1.0.0, puis v1.1.0 avec un hook de plus."""
    hooks_repository = tmp_path / "hooks"
    (hooks_repository / "reference").mkdir(parents=True)
    run_git(hooks_repository, "init")
    run_git(hooks_repository, "config", "--local", "user.name", "test")
    run_git(hooks_repository, "config", "--local", "user.email", "test@example.com")
    publish(hooks_repository, ["sync-pre-commit-config"], "v1.0.0")
    publish(hooks_repository, ["sync-pre-commit-config", "check-gitignore"], "v1.1.0")
    return hooks_repository


def rendered_reference(hooks_repository: Path, hook_ids: list[str], tag: str) -> str:
    return reference_template(hooks_repository, hook_ids).replace("{rev}", tag)


def test_sync_pre_commit_config_fails_and_moves_an_outdated_project_to_the_latest_tag(
    repository: Path, hooks_repository: Path, run_hook: HookRunner
) -> None:
    config = repository / ".pre-commit-config.yaml"
    config.write_text(rendered_reference(hooks_repository, ["sync-pre-commit-config"], "v1.0.0"))

    result = run_hook("sync-pre-commit-config")

    assert result.returncode == 1
    assert config.read_text() == rendered_reference(
        hooks_repository, ["sync-pre-commit-config", "check-gitignore"], "v1.1.0"
    )


def test_sync_pre_commit_config_passes_in_an_up_to_date_project(
    repository: Path, hooks_repository: Path, run_hook: HookRunner
) -> None:
    config = repository / ".pre-commit-config.yaml"
    content = rendered_reference(hooks_repository, ["sync-pre-commit-config", "check-gitignore"], "v1.1.0")
    config.write_text(content)

    result = run_hook("sync-pre-commit-config")

    assert result.returncode == 0
    assert config.read_text() == content

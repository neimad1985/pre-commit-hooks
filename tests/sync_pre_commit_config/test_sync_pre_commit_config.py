from pathlib import Path
from textwrap import dedent

import pytest
import yaml

from tests.conftest import HookRunner

REPOSITORY_URL = "https://example.com/hooks"
OTHER_BLOCK = {"repo": "https://example.com/other-hooks", "rev": "v1.0.0", "hooks": [{"id": "other-hook"}]}


@pytest.fixture
def hooks_repository(repository: Path) -> Path:
    """Fait du dépôt de test un dépôt de hooks, ce qui met sync-pre-commit-config en mode bootstrap."""
    (repository / ".pre-commit-hooks.yaml").write_text(
        dedent("""\
        - id: sync-pre-commit-config
          name: sync pre-commit config
          entry: sync-pre-commit-config
          language: python
          always_run: true
          pass_filenames: false
    """)
    )
    (repository / "reference").mkdir()
    (repository / "reference" / "pre-commit-config.yaml").write_text(
        dedent(f"""\
        repos:
          - repo: {REPOSITORY_URL}
            rev: {{rev}}
            hooks:
              - id: sync-pre-commit-config
          - repo: {OTHER_BLOCK["repo"]}
            rev: {OTHER_BLOCK["rev"]}
            hooks:
              - id: other-hook
    """)
    )
    return repository


def test_sync_pre_commit_config_fails_and_writes_a_local_block_while_keeping_other_repositories(
    hooks_repository: Path, run_hook: HookRunner
) -> None:
    result = run_hook("sync-pre-commit-config")

    assert result.returncode == 1
    config = yaml.safe_load((hooks_repository / ".pre-commit-config.yaml").read_text())
    assert config["repos"] == [
        {
            "repo": "local",
            "hooks": [
                {
                    "id": "sync-pre-commit-config",
                    "name": "sync pre-commit config",
                    "entry": "uv run sync-pre-commit-config",
                    "language": "system",
                    "always_run": True,
                    "pass_filenames": False,
                }
            ],
        },
        OTHER_BLOCK,
    ]


@pytest.mark.usefixtures("hooks_repository")
def test_sync_pre_commit_config_passes_with_an_up_to_date_config(run_hook: HookRunner) -> None:
    run_hook("sync-pre-commit-config")

    result = run_hook("sync-pre-commit-config")

    assert result.returncode == 0

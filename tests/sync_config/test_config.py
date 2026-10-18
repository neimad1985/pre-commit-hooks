from pathlib import Path
from textwrap import dedent

from pre_commit_hooks.sync_config.config import is_up_to_date


def test_is_up_to_date_accepts_a_config_identical_to_the_expected_content(tmp_path: Path) -> None:
    config = tmp_path / ".pre-commit-config.yaml"
    config.write_text("repos: []")

    assert is_up_to_date(config, "repos: []")


def test_is_up_to_date_rejects_a_config_that_differs_from_the_expected_content(tmp_path: Path) -> None:
    config = tmp_path / ".pre-commit-config.yaml"
    config.write_text("repos: []")

    assert not is_up_to_date(
        config,
        dedent("""\
            repos:
              - repo: local
        """),
    )


def test_is_up_to_date_rejects_a_missing_config(tmp_path: Path) -> None:
    assert not is_up_to_date(tmp_path / ".pre-commit-config.yaml", "repos: []")

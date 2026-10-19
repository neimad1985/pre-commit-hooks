from importlib.resources import files
from pathlib import Path

from conftest import HookRunner

REFERENCE = files("pre_commit_hooks.sync_ruff_config").joinpath("ruff.toml").read_text()


def test_sync_ruff_config_ignores_a_project_without_pyproject(repository: Path, run_hook: HookRunner) -> None:
    result = run_hook("sync-ruff-config")

    assert result.returncode == 0
    assert not (repository / "ruff.toml").exists()


def test_sync_ruff_config_fails_and_creates_ruff_toml_in_a_python_project(
    repository: Path, run_hook: HookRunner
) -> None:
    (repository / "pyproject.toml").write_text("[project]")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 1
    assert (repository / "ruff.toml").read_text() == REFERENCE


def test_sync_ruff_config_fails_and_rewrites_a_different_ruff_toml(repository: Path, run_hook: HookRunner) -> None:
    (repository / "pyproject.toml").write_text("[project]")
    (repository / "ruff.toml").write_text("line-length = 80")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 1
    assert (repository / "ruff.toml").read_text() == REFERENCE


def test_sync_ruff_config_passes_with_a_ruff_toml_identical_to_the_reference(
    repository: Path, run_hook: HookRunner
) -> None:
    (repository / "pyproject.toml").write_text("[project]")
    (repository / "ruff.toml").write_text(REFERENCE)

    result = run_hook("sync-ruff-config")

    assert result.returncode == 0

from importlib.resources import files
from pathlib import Path

from tests.conftest import HookRunner, run_git

REFERENCE = files("pre_commit_hooks.sync_ruff_config").joinpath("ruff.toml").read_text()


def track_python_file(repository: Path, relative_path: str) -> None:
    python_file = repository / relative_path
    python_file.parent.mkdir(parents=True, exist_ok=True)
    python_file.write_text("")
    run_git(repository, "add", relative_path)


def test_sync_ruff_config_ignores_a_repository_without_python_file(repository: Path, run_hook: HookRunner) -> None:
    (repository / "README.md").write_text("")
    run_git(repository, "add", "README.md")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 0
    assert not (repository / "ruff.toml").exists()


def test_sync_ruff_config_ignores_an_untracked_python_file(repository: Path, run_hook: HookRunner) -> None:
    (repository / "script.py").write_text("")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 0
    assert not (repository / "ruff.toml").exists()


def test_sync_ruff_config_fails_and_creates_ruff_toml_at_the_root_for_a_python_file_in_a_subfolder(
    repository: Path, run_hook: HookRunner
) -> None:
    track_python_file(repository, "project/src/module.py")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 1
    assert (repository / "ruff.toml").read_text() == REFERENCE
    assert not (repository / "project" / "ruff.toml").exists()


def test_sync_ruff_config_fails_and_rewrites_a_different_ruff_toml(repository: Path, run_hook: HookRunner) -> None:
    track_python_file(repository, "script.py")
    (repository / "ruff.toml").write_text("line-length = 80")

    result = run_hook("sync-ruff-config")

    assert result.returncode == 1
    assert (repository / "ruff.toml").read_text() == REFERENCE


def test_sync_ruff_config_passes_with_a_ruff_toml_identical_to_the_reference(
    repository: Path, run_hook: HookRunner
) -> None:
    track_python_file(repository, "script.py")
    (repository / "ruff.toml").write_text(REFERENCE)

    result = run_hook("sync-ruff-config")

    assert result.returncode == 0

import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

type HookRunner = Callable[..., subprocess.CompletedProcess[str]]


def run_git(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments], check=True, capture_output=True, text=True
    ).stdout


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    repository = tmp_path / "repository"
    repository.mkdir()
    run_git(repository, "init")
    run_git(repository, "config", "--local", "user.name", "test")
    run_git(repository, "config", "--local", "user.email", "test@example.com")
    return repository


@pytest.fixture
def run_hook(repository: Path) -> HookRunner:
    """Lance l'exécutable d'un hook installé dans le venv, depuis le dépôt de test."""

    def run(hook: str, environment: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(Path(sys.executable).parent / hook)],
            cwd=repository,
            capture_output=True,
            text=True,
            env=os.environ | (environment or {}),
        )

    return run

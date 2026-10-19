import subprocess
from pathlib import Path

from pre_commit_hooks.check_transcrypt.initialization import is_initialized


def run_git(repository: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(repository), *arguments], check=True, capture_output=True)


def test_is_initialized_rejects_a_repository_without_transcrypt_password(tmp_path: Path) -> None:
    run_git(tmp_path, "init")

    assert not is_initialized(tmp_path)


def test_is_initialized_accepts_a_repository_with_transcrypt_password(tmp_path: Path) -> None:
    run_git(tmp_path, "init")
    run_git(tmp_path, "config", "--local", "transcrypt.password", "fake-password-for-test")

    assert is_initialized(tmp_path)

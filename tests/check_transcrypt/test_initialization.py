import base64
import subprocess
from pathlib import Path

from pre_commit_hooks.check_transcrypt.initialization import ensure_initialized, is_initialized


def run_git(repository: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(repository), *arguments], check=True, capture_output=True)


def test_is_initialized_rejects_a_repository_without_transcrypt_password(tmp_path: Path) -> None:
    run_git(tmp_path, "init")

    assert not is_initialized(tmp_path)


def test_is_initialized_accepts_a_repository_with_transcrypt_password(tmp_path: Path) -> None:
    run_git(tmp_path, "init")
    run_git(tmp_path, "config", "--local", "transcrypt.password", "fake-password-for-test")

    assert is_initialized(tmp_path)


def git_output(repository: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments], check=True, capture_output=True, text=True
    ).stdout


def create_repository(directory: Path) -> Path:
    repository = directory / "repository"
    repository.mkdir()
    run_git(repository, "init")
    run_git(repository, "config", "--local", "user.name", "test")
    run_git(repository, "config", "--local", "user.email", "test@example.com")
    return repository


def create_password_file(directory: Path) -> Path:
    password_file = directory / "password"
    password_file.write_text("fake-password-for-test\n")
    return password_file


def test_ensure_initialized_makes_transcrypt_encrypt_committed_secrets(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)

    ensure_initialized(repository, create_password_file(tmp_path))

    (repository / ".gitattributes").write_text("secrets.* filter=crypt diff=crypt merge=crypt\n")
    (repository / "secrets.env").write_text("API_TOKEN=plain-value\n")
    run_git(repository, "add", ".gitattributes", "secrets.env")
    run_git(repository, "commit", "--message", "add secrets")
    stored_blob = git_output(repository, "cat-file", "blob", "HEAD:secrets.env")
    assert base64.b64decode(stored_blob).startswith(b"Salted__")


def test_ensure_initialized_leaves_an_initialized_repository_untouched(tmp_path: Path) -> None:
    repository = create_repository(tmp_path)
    run_git(repository, "config", "--local", "transcrypt.password", "fake-password-for-test")

    ensure_initialized(repository, create_password_file(tmp_path))

    filter_lookup = subprocess.run(
        ["git", "-C", str(repository), "config", "--local", "--get", "filter.crypt.clean"], capture_output=True
    )
    assert filter_lookup.returncode != 0

import base64
import subprocess
from pathlib import Path

import pytest

from tests.conftest import HookRunner, run_git

TRANSCRYPT_LINE = "secrets.* filter=crypt diff=crypt merge=crypt\n"


@pytest.fixture
def home(tmp_path: Path) -> dict[str, str]:
    """Fait pointer ~ vers un dossier temporaire, qui contient un faux ~/.thing."""
    home = tmp_path / "home"
    home.mkdir()
    (home / ".thing").write_text("fake-password-for-test\n")
    return {"HOME": str(home)}


@pytest.fixture
def initialized_repository(repository: Path) -> Path:
    run_git(repository, "config", "--local", "transcrypt.password", "fake-password-for-test")
    return repository


def has_crypt_filter(repository: Path) -> bool:
    lookup = subprocess.run(
        ["git", "-C", str(repository), "config", "--local", "--get", "filter.crypt.clean"],
        check=False,
        capture_output=True,
    )
    return lookup.returncode == 0


def test_check_transcrypt_passes_in_an_initialized_repository_with_the_transcrypt_line(
    initialized_repository: Path, run_hook: HookRunner, home: dict[str, str]
) -> None:
    (initialized_repository / ".gitattributes").write_text(TRANSCRYPT_LINE)

    result = run_hook("check-transcrypt", home)

    assert result.returncode == 0


def test_check_transcrypt_fails_and_adds_the_missing_transcrypt_line(
    initialized_repository: Path, run_hook: HookRunner, home: dict[str, str]
) -> None:
    result = run_hook("check-transcrypt", home)

    assert result.returncode == 1
    assert (initialized_repository / ".gitattributes").read_text() == TRANSCRYPT_LINE


def test_check_transcrypt_fails_after_initializing_transcrypt_so_that_secrets_get_encrypted(
    repository: Path, run_hook: HookRunner, home: dict[str, str]
) -> None:
    result = run_hook("check-transcrypt", home)

    assert result.returncode == 1
    assert "git add --renormalize ." in result.stderr
    (repository / "secrets.env").write_text("API_TOKEN=plain-value\n")
    run_git(repository, "add", ".gitattributes", "secrets.env")
    run_git(repository, "commit", "--message", "add secrets")
    stored_blob = run_git(repository, "cat-file", "blob", "HEAD:secrets.env")
    assert base64.b64decode(stored_blob).startswith(b"Salted__")


def test_check_transcrypt_does_not_rerun_transcrypt_in_an_initialized_repository(
    initialized_repository: Path, run_hook: HookRunner, home: dict[str, str]
) -> None:
    (initialized_repository / ".gitattributes").write_text(TRANSCRYPT_LINE)

    run_hook("check-transcrypt", home)

    assert not has_crypt_filter(initialized_repository)

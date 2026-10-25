import subprocess
from pathlib import Path

import pytest

from pre_commit_hooks.sync_pre_commit_config.repository import (
    find_latest_tag,
    read_file_at_tag,
)


def run_git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-C", str(repository), *arguments], check=True, capture_output=True
    )


def commit_file(repository: Path, content: str) -> None:
    (repository / "reference.yaml").write_text(content)
    run_git(repository, "add", "reference.yaml")
    run_git(
        repository,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "--message",
        content,
    )


@pytest.fixture
def repository(tmp_path: Path) -> Path:
    run_git(tmp_path, "init", "--initial-branch", "main")
    commit_file(tmp_path, "first")
    run_git(tmp_path, "tag", "1.9.0")
    commit_file(tmp_path, "second")
    run_git(tmp_path, "tag", "1.10.0")
    commit_file(tmp_path, "untagged")
    return tmp_path


def test_find_latest_tag_orders_tags_as_versions_not_as_text(repository: Path) -> None:
    assert find_latest_tag(str(repository)) == "1.10.0"


def test_find_latest_tag_fails_when_the_repository_has_no_tag(tmp_path: Path) -> None:
    run_git(tmp_path, "init", "--initial-branch", "main")
    commit_file(tmp_path, "first")

    with pytest.raises(LookupError):
        find_latest_tag(str(tmp_path))


def test_read_file_at_tag_returns_the_content_of_the_tagged_version(
    repository: Path,
) -> None:
    assert read_file_at_tag(str(repository), "1.9.0", "reference.yaml") == "first"

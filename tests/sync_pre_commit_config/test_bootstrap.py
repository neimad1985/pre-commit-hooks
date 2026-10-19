from pathlib import Path

from pre_commit_hooks.sync_pre_commit_config.bootstrap import is_hooks_repository


def test_is_hooks_repository_rejects_a_repository_without_manifest(tmp_path: Path) -> None:
    assert not is_hooks_repository(tmp_path)

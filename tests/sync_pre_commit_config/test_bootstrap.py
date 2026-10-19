from pathlib import Path
from textwrap import dedent

import yaml

from pre_commit_hooks.sync_pre_commit_config.bootstrap import is_hooks_repository, localize_reference

REPOSITORY_URL = "https://example.com/hooks"

REFERENCE = dedent("""\
    repos:
      - repo: https://example.com/hooks
        rev: {rev}
        hooks:
          - id: sync-pre-commit-config
""")

MANIFEST = dedent("""\
    - id: sync-pre-commit-config
      name: sync pre-commit config
      entry: sync-pre-commit-config
      language: python
      always_run: true
      pass_filenames: false
""")


def test_is_hooks_repository_recognizes_a_repository_whose_manifest_declares_sync_pre_commit_config(tmp_path: Path) -> None:
    (tmp_path / ".pre-commit-hooks.yaml").write_text(MANIFEST)

    assert is_hooks_repository(tmp_path)


def test_is_hooks_repository_rejects_a_repository_without_manifest(tmp_path: Path) -> None:
    assert not is_hooks_repository(tmp_path)


def test_localize_reference_replaces_the_remote_block_by_a_local_block(tmp_path: Path) -> None:
    (tmp_path / ".pre-commit-hooks.yaml").write_text(MANIFEST)

    localized = yaml.safe_load(localize_reference(REFERENCE, tmp_path, REPOSITORY_URL))

    assert [block["repo"] for block in localized["repos"]] == ["local"]


def test_localize_reference_runs_each_hook_from_the_manifest_through_uv(tmp_path: Path) -> None:
    (tmp_path / ".pre-commit-hooks.yaml").write_text(MANIFEST)

    localized = yaml.safe_load(localize_reference(REFERENCE, tmp_path, REPOSITORY_URL))

    assert localized["repos"][0]["hooks"] == [
        {
            "id": "sync-pre-commit-config",
            "name": "sync pre-commit config",
            "entry": "uv run sync-pre-commit-config",
            "language": "system",
            "always_run": True,
            "pass_filenames": False,
        }
    ]

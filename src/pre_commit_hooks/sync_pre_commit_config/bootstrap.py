from pathlib import Path
from typing import Any

import yaml

from pre_commit_hooks.sync_pre_commit_config.config import (
    SYNC_PRE_COMMIT_CONFIG_HOOK_ID,
    declares_sync_hook,
)

MANIFEST_FILENAME = ".pre-commit-hooks.yaml"


def is_hooks_repository(directory: Path) -> bool:
    manifest_path = directory / MANIFEST_FILENAME
    if not manifest_path.exists():
        return False
    return any(
        hook["id"] == SYNC_PRE_COMMIT_CONFIG_HOOK_ID
        for hook in yaml.safe_load(manifest_path.read_text())
    )


def localize_hook(manifest_hook: dict[str, Any]) -> dict[str, Any]:
    return manifest_hook | {
        "entry": f"uv run {manifest_hook['entry']}",
        "language": "system",
    }


def localize_block(
    remote_block: dict[str, Any], manifest_hooks: list[dict[str, Any]]
) -> dict[str, Any]:
    manifest_hooks_by_id = {hook["id"]: hook for hook in manifest_hooks}
    return {
        "repo": "local",
        "hooks": [
            localize_hook(manifest_hooks_by_id[hook["id"]])
            for hook in remote_block["hooks"]
        ],
    }


def localize_reference(reference: str, directory: Path) -> str:
    """
    Remplace le bloc du dépôt de hooks par un bloc local.

    Ce bloc local lance le code du répertoire de travail.
    """
    config = yaml.safe_load(reference)
    manifest_hooks = yaml.safe_load((directory / MANIFEST_FILENAME).read_text())
    config["repos"] = [
        localize_block(block, manifest_hooks) if declares_sync_hook(block) else block
        for block in config["repos"]
    ]
    return yaml.safe_dump(config, sort_keys=False)

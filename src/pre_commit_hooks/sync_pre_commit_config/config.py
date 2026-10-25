from pathlib import Path
from typing import Any

import yaml

SYNC_PRE_COMMIT_CONFIG_HOOK_ID = "sync-pre-commit-config"


def is_up_to_date(config_path: Path, expected_content: str) -> bool:
    return config_path.exists() and config_path.read_text() == expected_content


def declares_sync_hook(block: dict[str, Any]) -> bool:
    return any(hook["id"] == SYNC_PRE_COMMIT_CONFIG_HOOK_ID for hook in block["hooks"])


def find_hooks_repository_url(config_path: Path) -> str:
    """Renvoie l'adresse du dépôt qui fournit sync-pre-commit-config au projet."""
    for block in yaml.safe_load(config_path.read_text())["repos"]:
        if declares_sync_hook(block):
            return block["repo"]
    message = (
        f"No repository declares {SYNC_PRE_COMMIT_CONFIG_HOOK_ID} in {config_path}"
    )
    raise LookupError(message)

from pathlib import Path


def is_up_to_date(config_path: Path, expected_content: str) -> bool:
    return config_path.exists() and config_path.read_text() == expected_content

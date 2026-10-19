from pathlib import Path


def is_python_project(directory: Path) -> bool:
    return (directory / "pyproject.toml").exists()

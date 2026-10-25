from pathlib import Path


def read_lines(gitignore_path: Path) -> list[str]:
    return gitignore_path.read_text().splitlines() if gitignore_path.exists() else []


def find_missing_lines(gitignore_path: Path, required_lines: list[str]) -> list[str]:
    present_lines = set(read_lines(gitignore_path))
    return [line for line in required_lines if line not in present_lines]


def append_lines(gitignore_path: Path, lines: list[str]) -> None:
    existing_content = gitignore_path.read_text() if gitignore_path.exists() else ""
    separator = "\n" if existing_content and not existing_content.endswith("\n") else ""
    gitignore_path.write_text(
        existing_content + separator + "".join(f"{line}\n" for line in lines)
    )

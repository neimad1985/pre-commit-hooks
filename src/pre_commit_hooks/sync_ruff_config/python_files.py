import subprocess
from pathlib import Path


def contains_python_files(repository: Path) -> bool:
    tracked_python_files = subprocess.run(
        ["git", "-C", str(repository), "ls-files", "--", "*.py"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return tracked_python_files != ""

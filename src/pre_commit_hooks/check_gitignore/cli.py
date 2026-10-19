from pathlib import Path

import typer

from pre_commit_hooks.check_gitignore.gitignore import append_lines, find_missing_lines

REQUIRED_LINES = ["__pycache__/", ".venv/"]
GITIGNORE_PATH = Path(".gitignore")

app = typer.Typer()


@app.command()
def main() -> None:
    """Add the required lines missing from .gitignore and fail if any was missing."""
    missing_lines = find_missing_lines(GITIGNORE_PATH, REQUIRED_LINES)
    if not missing_lines:
        return
    append_lines(GITIGNORE_PATH, missing_lines)
    typer.echo(
        f"{GITIGNORE_PATH} completed with {', '.join(missing_lines)}, run `git add {GITIGNORE_PATH}` and commit again.",
        err=True,
    )
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

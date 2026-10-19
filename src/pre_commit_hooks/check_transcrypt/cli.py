from pathlib import Path

import typer

from pre_commit_hooks.check_gitignore.gitignore import append_lines, find_missing_lines
from pre_commit_hooks.check_transcrypt.initialization import ensure_initialized

REQUIRED_LINES = ["secrets.* filter=crypt diff=crypt merge=crypt"]
GITATTRIBUTES_PATH = Path(".gitattributes")
PASSWORD_FILE = Path("~/.thing").expanduser()

app = typer.Typer()


@app.command()
def main() -> None:
    """Add the transcrypt line missing from .gitattributes, initialize transcrypt if needed."""
    initialized = ensure_initialized(Path.cwd(), PASSWORD_FILE)
    if initialized:
        # Les secrets indexés avant l'initialisation l'ont été sans filtre, donc en clair.
        typer.echo("transcrypt initialized, run `git add --renormalize .` and commit again.", err=True)
    missing_lines = find_missing_lines(GITATTRIBUTES_PATH, REQUIRED_LINES)
    if missing_lines:
        append_lines(GITATTRIBUTES_PATH, missing_lines)
        typer.echo(f"{GITATTRIBUTES_PATH} completed, run `git add {GITATTRIBUTES_PATH}` and commit again.", err=True)
    if initialized or missing_lines:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

from pathlib import Path

import typer

from pre_commit_hooks.sync_pre_commit_config.config import is_up_to_date
from pre_commit_hooks.sync_ruff_config.project import is_python_project
from pre_commit_hooks.sync_ruff_config.reference import read_reference

RUFF_CONFIG_PATH = Path("ruff.toml")

app = typer.Typer()


@app.command()
def main() -> None:
    """Rewrite ruff.toml from the reference in a Python project and fail if it changed."""
    if not is_python_project(Path.cwd()):
        return
    expected_content = read_reference()
    if is_up_to_date(RUFF_CONFIG_PATH, expected_content):
        return
    RUFF_CONFIG_PATH.write_text(expected_content)
    typer.echo(
        f"{RUFF_CONFIG_PATH} synchronized with the reference, run `git add {RUFF_CONFIG_PATH}` and commit again.",
        err=True,
    )
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

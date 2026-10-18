from pathlib import Path

import typer

from pre_commit_hooks.sync_config.config import is_up_to_date
from pre_commit_hooks.sync_config.reference import render_reference
from pre_commit_hooks.sync_config.repository import find_latest_tag, read_file_at_tag

REPOSITORY_URL = "https://github.com/neimad1985/pre-commit-hooks"
REFERENCE_PATH = "reference/pre-commit-config.yaml"
CONFIG_PATH = Path(".pre-commit-config.yaml")

app = typer.Typer()


@app.command()
def main() -> None:
    """Rewrite .pre-commit-config.yaml from the latest reference and fail if it changed."""
    latest_tag = find_latest_tag(REPOSITORY_URL)
    expected_content = render_reference(read_file_at_tag(REPOSITORY_URL, latest_tag, REFERENCE_PATH), latest_tag)
    if is_up_to_date(CONFIG_PATH, expected_content):
        return
    CONFIG_PATH.write_text(expected_content)
    typer.echo(f"{CONFIG_PATH} synchronized with {latest_tag}, commit it and run again.", err=True)
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

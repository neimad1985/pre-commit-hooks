from pathlib import Path

import typer

from pre_commit_hooks.sync_pre_commit_config.bootstrap import is_hooks_repository, localize_reference
from pre_commit_hooks.sync_pre_commit_config.config import find_hooks_repository_url, is_up_to_date
from pre_commit_hooks.sync_pre_commit_config.reference import render_reference
from pre_commit_hooks.sync_pre_commit_config.repository import find_latest_tag, read_file_at_tag

REFERENCE_PATH = "reference/pre-commit-config.yaml"
CONFIG_PATH = Path(".pre-commit-config.yaml")

app = typer.Typer()


def expected_config() -> str:
    if is_hooks_repository(Path.cwd()):
        return localize_reference(Path(REFERENCE_PATH).read_text(), Path.cwd())
    repository_url = find_hooks_repository_url(CONFIG_PATH)
    latest_tag = find_latest_tag(repository_url)
    return render_reference(read_file_at_tag(repository_url, latest_tag, REFERENCE_PATH), latest_tag)


@app.command()
def main() -> None:
    """Rewrite .pre-commit-config.yaml from the reference and fail if it changed."""
    expected_content = expected_config()
    if is_up_to_date(CONFIG_PATH, expected_content):
        return
    CONFIG_PATH.write_text(expected_content)
    typer.echo(
        f"{CONFIG_PATH} synchronized with the latest reference, run `git add {CONFIG_PATH}` and commit again.", err=True
    )
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()

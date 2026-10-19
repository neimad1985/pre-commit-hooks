from pathlib import Path
from textwrap import dedent

from conftest import HookRunner


def test_check_gitignore_passes_and_keeps_a_complete_gitignore(repository: Path, run_hook: HookRunner) -> None:
    content = dedent("""\
        /legacy
        __pycache__/
        .venv/
    """)
    (repository / ".gitignore").write_text(content)

    result = run_hook("check-gitignore")

    assert result.returncode == 0
    assert (repository / ".gitignore").read_text() == content


def test_check_gitignore_fails_and_appends_missing_lines_after_existing_ones(
    repository: Path, run_hook: HookRunner
) -> None:
    (repository / ".gitignore").write_text("/legacy")

    result = run_hook("check-gitignore")

    assert result.returncode == 1
    assert (repository / ".gitignore").read_text() == dedent("""\
        /legacy
        __pycache__/
        .venv/
    """)
    assert "git add .gitignore" in result.stderr


def test_check_gitignore_fails_and_creates_a_missing_gitignore(repository: Path, run_hook: HookRunner) -> None:
    result = run_hook("check-gitignore")

    assert result.returncode == 1
    assert (repository / ".gitignore").read_text() == dedent("""\
        __pycache__/
        .venv/
    """)


def test_check_gitignore_requires_the_trailing_slash_of_pycache(repository: Path, run_hook: HookRunner) -> None:
    (repository / ".gitignore").write_text(dedent("""\
        __pycache__
        .venv/
    """))

    result = run_hook("check-gitignore")

    assert result.returncode == 1
    assert (repository / ".gitignore").read_text() == dedent("""\
        __pycache__
        .venv/
        __pycache__/
    """)

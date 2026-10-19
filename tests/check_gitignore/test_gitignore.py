from pathlib import Path
from textwrap import dedent

from pre_commit_hooks.check_gitignore.gitignore import append_lines, find_missing_lines

REQUIRED_LINES = ["__pycache__/", ".venv/"]


def test_find_missing_lines_accepts_a_gitignore_with_required_lines_among_others(tmp_path: Path) -> None:
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(dedent("""\
        /legacy
        __pycache__/
        .venv/
    """))

    assert find_missing_lines(gitignore, REQUIRED_LINES) == []


def test_append_lines_adds_missing_lines_at_the_end_and_keeps_existing_ones(tmp_path: Path) -> None:
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("/legacy")

    append_lines(gitignore, find_missing_lines(gitignore, REQUIRED_LINES))

    assert gitignore.read_text() == dedent("""\
        /legacy
        __pycache__/
        .venv/
    """)


def test_append_lines_creates_a_missing_gitignore_with_required_lines(tmp_path: Path) -> None:
    gitignore = tmp_path / ".gitignore"

    append_lines(gitignore, find_missing_lines(gitignore, REQUIRED_LINES))

    assert gitignore.read_text() == dedent("""\
        __pycache__/
        .venv/
    """)


def test_find_missing_lines_requires_an_exact_match(tmp_path: Path) -> None:
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(dedent("""\
        __pycache__
        .venv/
    """))

    assert find_missing_lines(gitignore, REQUIRED_LINES) == ["__pycache__/"]

from textwrap import dedent

import pytest

from pre_commit_hooks.sync_pre_commit_config.reference import render_reference


def test_render_reference_replaces_the_rev_placeholder_with_the_given_tag() -> None:
    template = dedent("""\
        repos:
          - repo: https://example.com/hooks
            rev: {rev}
    """)

    rendered = render_reference(template, "1.2.0")

    assert rendered == dedent("""\
        repos:
          - repo: https://example.com/hooks
            rev: 1.2.0
    """)


def test_render_reference_rejects_a_template_without_rev_placeholder() -> None:
    with pytest.raises(ValueError, match="placeholder"):
        render_reference("repos: []", "1.2.0")

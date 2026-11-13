"""Deduce the Conventional Commits type from staged files.

The heuristic is shared by the ``set-type-from-status`` hook
(``prepare-commit-msg``) and the ``check-type-from-status`` hook
(``commit-msg``), so the rule lives here only once.
"""

# ruff: file-ignore[suspicious-subprocess-import, start-process-with-partial-path]

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING, Final

from icecream import ic

from incolume.py.githooks.core.rules import Result, Status, TypeCommit

if TYPE_CHECKING:
    from collections.abc import Sequence

TYPE_BUILD: Final[str] = 'build'
TYPE_CI: Final[str] = 'ci'
TYPE_TEST: Final[str] = 'test'
TYPE_DOCS: Final[str] = 'docs'
TYPE_FEAT: Final[str] = 'feat'

TYPES_PRECEDENCE: Final[tuple[str, ...]] = (
    TYPE_BUILD,
    TYPE_CI,
    TYPE_TEST,
    TYPE_DOCS,
    TYPE_FEAT,
)
BUILD_FILES: Final[frozenset[str]] = frozenset({
    'pyproject.toml',
    'uv.lock',
})
CHANGELOG: Final[str] = 'CHANGELOG.md'
TYPE_TOKENS: Final[str] = '|'.join(
    sorted({
        *TypeCommit.to_set(),
        *(n.lower() for n in TypeCommit.__members__),
    })
)
TYPE_PATTERN: Final[re.Pattern[str]] = re.compile(
    rf'^({TYPE_TOKENS})(\([\w\W\s]+\))?!?:'
)
ISSUE_PREFIX_PATTERN: Final[re.Pattern[str]] = re.compile(r'^\[ISSUE-\d+\]\s*')


def _is_code(path: str) -> bool:
    """Check if the path is product code, not an ancillary artifact.

    Args:
        path: staged path, relative to the repository.

    Returns:
        True when the path is not a build, ci, test or docs artifact.

    .. versionadded:: 1.23.0a2

    """
    name = Path(path).name
    if name in BUILD_FILES or name == 'version.txt':
        return False
    if path.startswith('.github/'):
        return False
    if (
        path.startswith('tests/')
        or name.startswith('test_')
        or name.endswith('_test.py')
    ):
        return False
    return not (
        path.startswith('docs/')
        or path.endswith('.md')
        or path == 'mkdocs.yml'
    )


def deduce_type(paths: Sequence[str | Path] | None = None) -> str:
    """Deduce the commit type from staged paths.

    Product code dominates: when any staged path is code, the type is
    ``feat`` (the author refines it to ``fix``/``refactor`` when needed).
    Without code, the precedence is highest first: build, ci, test,
    docs. A lone ``CHANGELOG.md`` is a generated build artifact; next
    to other files it counts as documentation.

    Args:
        paths: staged paths; ``None`` or empty yields no suggestion.

    Returns:
        One of ``build``, ``ci``, ``test``, ``docs``, ``feat``, or an empty
        string when there is nothing staged.

    Examples:
        >>> deduce_type(['docs/hooks.md'])
        'docs'
        >>> deduce_type(['pyproject.toml', 'docs/hooks.md'])
        'build'
        >>> deduce_type(['incolume/py/githooks/cli/cli.py', 'pyproject.toml'])
        'feat'
        >>> deduce_type([])
        ''

    """
    staged = [Path(path).as_posix() for path in paths or []]
    if not staged:
        return ''
    if any(_is_code(path) for path in staged):
        return TYPE_FEAT
    names = {Path(path).name for path in staged}
    if names & BUILD_FILES or 'version.txt' in names or staged == [CHANGELOG]:
        return TYPE_BUILD
    if any(path.startswith('.github/') for path in staged):
        return TYPE_CI
    if any(path.startswith('tests/') for path in staged):
        return TYPE_TEST
    return TYPE_DOCS


def get_staged_files() -> list[str]:
    """Return the paths staged in the index.

    Returns:
        Staged paths, or an empty list when git is unavailable.

    """
    try:
        output = subprocess.check_output(
            ['git', 'diff', '--cached', '--name-only'],
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        ic('staged files unavailable')
        return []
    return [line.strip() for line in output.splitlines() if line.strip()]


def _message_type(message: str) -> tuple[str, str]:
    """Return the ``[ISSUE-*]`` prefix and the declared type."""
    prefix = ISSUE_PREFIX_PATTERN.match(message)
    header = prefix.group(0) if prefix else ''
    match = TYPE_PATTERN.match(message[len(header) :])
    if not match:
        return header, ''
    return header, TypeCommit(match.group(1).upper()).value


def declared_type(message: str) -> str:
    """Return the Conventional Commits type declared in the message.

    Args:
        message: commit message content.

    Returns:
        The declared type (``feat``, ``fix``, ...) or an empty string when
        the message does not declare one.

    """
    return _message_type(message)[1]


def set_type_commit_msg(
    commit_msg_filepath: Path | str,
    paths: Sequence[str | Path] | None = None,
    commit_type: str = '',
) -> Result:
    """Inject the deduced type into the commit message template.

    An existing type, a message given with ``-m`` and an empty template are
    never rewritten.

    Args:
        commit_msg_filepath: path to the commit message file.
        paths: staged paths; when ``None`` they are read from git.
        commit_type: third ``prepare-commit-msg`` argument.

    Returns:
        Result with the status and a human readable message.

    """
    if commit_type == 'message':
        return Result(
            Status.SUCCESS,
            'Hook not executed because of commit_type=message.',
        )

    msg_file = Path(commit_msg_filepath)
    if not msg_file.is_file():
        return Result(
            Status.FAILURE,
            f'Commit message file not found: {msg_file}',
        )

    content = msg_file.read_text(encoding='utf-8')
    deduced = deduce_type(paths if paths is not None else get_staged_files())
    prefix, declared = _message_type(content)
    if not deduced or declared or not content.strip():
        return Result(Status.SUCCESS, 'Commit message type unchanged.')

    msg_file.write_text(
        f'{prefix}{deduced}: {content[len(prefix) :]}',
        encoding='utf-8',
    )
    return Result(
        Status.SUCCESS,
        f'Type "{deduced}" added to the commit message.',
    )

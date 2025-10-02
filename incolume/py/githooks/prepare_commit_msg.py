"""Module for validate commit message."""

# ruff: noqa: E501
from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import rich
from icecream import ic

from incolume.py.githooks.rules import (
    FAILURE,
    RULE_COMMITFORMAT,
    SUCCESS,
)
from incolume.py.githooks.utils import Result, debug_enable

if TYPE_CHECKING:
    from collections.abc import Sequence

debug_enable()

MESSAGESUCCESS = '[green]Commit message is validated [OK][/green]'
MESSAGERROR = """[red]
    Your commit was rejected due to the [bold underline]invalid commit message[/bold underline]...

    Please use the following format:
      [green]<type>(optional scope): #id-issue <description>[/green]

    [cyan]type values: feature | feat, bugfix | fix, chore, refactor, docs, style, test, perf, ci, build or revert[/cyan]

    Examples:
      #1 <type>: #id-issue <description>:
            git commit -m 'feature: #1234 feature example comment'
      #2 <type>(scope): #id-issue <description>:
            git commit -m 'feat(docs): #1234 feature example comment'
      #3 <type>(scope): #id-issue <description>:
            git commit -m 'fix(ui): #4321 bugfix example comment'
      #4 <type>!: #id-issue <description>:
            git commit -m 'fix!: #4321 chore example comment with possible breaking change'
      #5 <type>!: #id-issue <description>:
            git commit -m 'bugfix!: #4321 chore example comment with possible breaking change'
      #6 <type>(scope)!: #id-issue <description>:
            git commit -m 'refactor(chore)!: #4321 chore example comment with possible breaking change'
      #7 <type>(scope)!: #id-issue <description>:
            git commit -m 'chore(fix)!: #4321 drop support for Python 2.6' -m 'BREAKING CHANGE: Some features not available in Python 2.7-.'

    [yellow] >>> More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/[/yellow]
    [/red]"""


def prepare_commit_msg(msgfile: Path | str | None = None) -> Result:
    """Prepend the commit message with `text`."""
    msgfile = Path(msgfile)
    result = Result(SUCCESS, MESSAGESUCCESS)
    regex = re.compile(RULE_COMMITFORMAT, flags=re.IGNORECASE)
    logging.debug('%s', str(regex.pattern))

    try:
        with msgfile.open('rb') as f:
            content = f.read().strip().decode()
            logging.debug('%s', ic(content))

        if not regex.match(content):
            raise AssertionError  # noqa: TRY301
    except (AssertionError, FileNotFoundError, FileExistsError):
        result = Result(FAILURE, MESSAGERROR)

    return result


def check_type_commit_msg(commit_msg_filepath: Path | str = '') -> Result:
    """Check type commit messagem."""
    regex = re.compile(
        r'^(feat|fix|chore|docs|style|refactor|test|perf|ci|build):'
    )
    commit_msg_filepath = Path(commit_msg_filepath)
    result = Result(SUCCESS, MESSAGESUCCESS)
    with Path(commit_msg_filepath).open('rb') as f:
        commit_message = f.read().decode().strip()

    # Example validation: Ensure message starts with a type (e.g., feat, fix, chore)
    if not regex.match(commit_message):
        result = Result(
            code=FAILURE,
            message='Error: Commit message must start with a type (e.g., feat:, fix:).',
        )
    return result


def check_type_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> sys.exit:
    """Check commit message."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    result = check_type_commit_msg(*args.filenames)
    rich.print(result.message)
    sys.exit(result.code)  # Validation passed or failure, allowing commit


def check_min_len_first_line_commit_msg(
    commit_msg_filepath: Path | str, len_line: int = 10
) -> Result:
    """Check len of first line from commit message.

    Returns:
        bool:

    """
    commit_msg_filepath = Path(commit_msg_filepath)
    len_line = min(10, len_line)
    result = Result(
        SUCCESS,
        '[green]Commit minimum length for message is validated [OK][/green]',
    )

    commit_message = commit_msg_filepath.read_text(encoding='utf-8').strip()

    # Example validation: Check subject line length (e.g., 50 character limit)
    first_line = commit_message.split('\n')[0]
    if len(first_line) < len_line:
        result.code = FAILURE
        result.message = f'Error: Commit subject line has an insufficient number of {len_line} characters allowed ({len(first_line)}).'
    return result


def check_max_len_first_line_commit_msg(
    commit_msg_filepath: Path | str, len_line: int = 50
) -> Result:
    """Check len of first line from commit message.

    Returns:
        bool:

    """
    commit_msg_filepath = Path(commit_msg_filepath)
    len_line = min(50, len_line)
    result = Result(
        SUCCESS,
        '[green]Commit maximum length for message is validated [OK][/green]',
    )

    commit_message = commit_msg_filepath.read_text(encoding='utf-8').strip()

    # Example validation: Check subject line length (e.g., 50 character limit)
    first_line = commit_message.split('\n')[0]
    if len(first_line) > len_line:
        result.code = FAILURE
        result.message = f'Error: Commit subject line exceeds {len_line} characters ({len(first_line)}).'
    return result


def check_len_first_line_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Check commit message."""
    results = []
    result_code = SUCCESS
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    parser.add_argument(
        '--min-first-line',
        default=10,
        type=int,
        help='Minimum Length of line for first line',
    )
    parser.add_argument(
        '--max-first-line',
        default=50,
        type=int,
        help='Maximum Length of line for first line',
    )
    args = parser.parse_args(argv)
    results.extend((
        check_min_len_first_line_commit_msg(
            *args.filenames, len_line=args.min_first_line
        ),
        check_max_len_first_line_commit_msg(
            *args.filenames, len_line=args.max_first_line
        ),
    ))
    for result in results:
        rich.print(result.message)
        result_code |= result.code

    sys.exit(result_code)  # Validation passed, allow commit

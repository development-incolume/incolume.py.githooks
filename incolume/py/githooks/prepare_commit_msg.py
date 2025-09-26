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

from incolume.py.githooks import FAILURE, RULE_COMMITFORMAT, SUCCESS, Result

if TYPE_CHECKING:
    from collections.abc import Sequence

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


def prepare_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> sys.exit:
    """Run CLI for prepare-commit-msg hook."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    ic(fl := Path('.git/COMMIT_EDITMSG'))
    ic(fl.is_file())
    logging.debug('msgfile: %s', args)

    result = prepare_commit_msg(*args.filenames)

    rich.print(result.message)
    sys.exit(result.code)


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
    result = Result(SUCCESS, MESSAGESUCCESS)

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
    result = Result(SUCCESS, MESSAGESUCCESS)

    commit_message = commit_msg_filepath.read_text(encoding='utf-8').strip()

    # Example validation: Check subject line length (e.g., 50 character limit)
    first_line = commit_message.split('\n')[0]
    if len(first_line) > len_line:
        result.code = FAILURE
        result.message = f'Error: Commit subject line exceeds {len_line} characters ({len(first_line)}).'
    return result


def check_max_len_first_line_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Check commit message."""
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    result = check_max_len_first_line_commit_msg(*args.filenames)

    rich.print(result.message)
    sys.exit(result.code)  # Validation passed, allow commit


def clean_commit_msg_cli(
    argv: Sequence[str] | None = None,
) -> int:
    """Remove the help message.

    Remove "# Please enter the commit message..." from help message.

    Args:
        argv: Arguments values sequence:
          - commit_msg_file (Path or str): The path to the commit message file.
          - commit_source (str): The source of the commit message.
          - commit_hash (str): The commit hash.

    Returns:
        int: SUCCESS code if the operation completes.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('commit_msg_file', help='Filename for commit message')
    parser.add_argument('commit_source', help='Commit source')
    parser.add_argument('commit_hash', help='Commit hash')
    args = parser.parse_args(argv)
    commit_msg_file = args.commit_msg_file
    commit_source = args.commit_source
    commit_hash = args.commit_hash

    ic(commit_msg_file, commit_source, commit_hash)

    commit_msg_file = Path(commit_msg_file)

    backup = commit_msg_file.with_suffix(commit_msg_file.suffix + '.bak')
    backup.write_bytes(commit_msg_file.read_bytes())

    result = []
    skipping = False

    for line in commit_msg_file.read_text(encoding='utf-8').splitlines(
        keepends=True
    ):
        if not skipping and line.lstrip().startswith(
            'Please enter the commit message'
        ):
            skipping = True
            continue
        if skipping and line.strip() == '#':
            skipping = False
            continue
        if not skipping:
            result.append(line)

    commit_msg_file.write_text(''.join(result), encoding='utf-8')

    return SUCCESS


def check_prospect() -> None:
    r"""Check prospect.

    #!/bin/sh
    #
    # An example hook script to prepare the commit log message.
    # Called by "git commit" with the name of the file that has the
    # commit message, followed by the description of the commit
    # message's source.  The hook's purpose is to edit the commit
    # message file.  If the hook fails with a non-zero status,
    # the commit is aborted.
    #
    # To enable this hook, rename this file to "prepare-commit-msg".

    # This hook includes three examples. The first one removes the
    # "# Please enter the commit message..." help message.
    #
    # The second includes the output of "git diff --name-status -r"
    # into the message, just before the "git status" output.  It is
    # commented because it doesn't cope with --amend or with squashed
    # commits.
    #
    # The third example adds a Signed-off-by line to the message, that can
    # still be edited.  This is rarely a good idea.

    COMMIT_MSG_FILE=$1
    COMMIT_SOURCE=$2
    SHA1=$3

    /usr/bin/perl -i.bak -ne 'print unless(m/^. Please enter the commit message/..m/^#$/)' "$COMMIT_MSG_FILE"

    # case "$COMMIT_SOURCE,$SHA1" in
    #  ,|template,)
    #    /usr/bin/perl -i.bak -pe '
    #       print "\n" . `git diff --cached --name-status -r`
    #        if /^#/ && $first++ == 0' "$COMMIT_MSG_FILE" ;;
    #  *) ;;
    # esac

    # SOB=$(git var GIT_COMMITTER_IDENT | sed -n 's/^\\(.*>\\).*$/Signed-off-by: \1/p')
    # git interpret-trailers --in-place --trailer "$SOB" "$COMMIT_MSG_FILE"
    # if test -z "$COMMIT_SOURCE"
    # then
    #   /usr/bin/perl -i.bak -pe 'print "\n" if !$first_line++' "$COMMIT_MSG_FILE"
    # fi
    """


if __name__ == '__main__':
    raise SystemExit(prepare_commit_msg_cli())

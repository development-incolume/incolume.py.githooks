"""Example.

diponível em https://www.atlassian.com/br/git/tutorials/git-hooks
"""

import re
import sys
from pathlib import Path
from subprocess import (  # ruff: ignore[suspicious-subprocess-import]
    check_output,
)

import click
from icecream import ic

from incolume.py.githooks.core import (
    CONTEXT_SETTINGS_CLICK,
    __package_name__,
    __version__,
)


@click.command(context_settings=CONTEXT_SETTINGS_CLICK, no_args_is_help=True)
@click.version_option(
    __version__,
    '-V',
    '--version',
    package_name=__package_name__,
    prog_name='populate-issue',
)
@click.argument(
    'commit_msg_filepath',
    required=True,
    type=click.Path(exists=True),
    help='commit message filename',
)
@click.argument(
    'commit_type', required=False, default='', type=str, help='commit type'
)
@click.argument(
    'commit_hash', required=False, default='', type=str, help='commit hash'
)
def populate_issue(
    commit_msg_filepath: Path, commit_type: str, commit_hash: str
) -> None:
    """Populate the commit message with the issue #, if there is one."""
    ic(
        f'prepare-commit-msg: \n\tFile: {commit_msg_filepath}\n\t'
        f'Type: {commit_type}\n\tHash: {commit_hash}'
    )

    # Figure out which branch we're on
    branch = (
        check_output(['git', 'symbolic-ref', '--short', 'HEAD'])  # ruff: ignore[start-process-with-partial-path]
        .strip()
        .decode(encoding='utf-8')
    )
    ic(f"prepare-commit-msg: On branch '{branch}'")

    if branch.startswith('issue-'):
        ic("prepare-commit-msg: Oh hey, it's an issue branch.")
        result = re.match(r'issue-(.*)', branch)
        issue_number = result.group(1)

        with Path(commit_msg_filepath).open('r+', encoding='utf-8') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(f'ISSUE-{issue_number} {content}')


if __name__ == '__main__':
    sys.exit(populate_issue(sys.argv[1:]))

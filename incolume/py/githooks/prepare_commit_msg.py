"""Module for validate commit message."""

# ruff: noqa: T201 E501

import logging
import re
import sys
from pathlib import Path

COMMITFORMAT = r'^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\(.*\))?\!?: #[0-9]+) .*(\n.*)*)$'

MESSAGESUCCESS = '\033[92m{}\033[0m'.format('Commit message is validated [OK]')
MESSAGERROR = '\033[91m{}\033[0m'.format("""
    Your commit was rejected due to the invalid commit message...

    Please use the following format:
    <type>(optional scope): #id-issue <description>

    types: feature/feat, fix, chore, refactor, docs, style, test, perf, ci, build and revert

    Examples:
    #1-> git commit -m 'feature: #1234 feature example comment'
    #2-> git commit -m 'feat(docs): #1234 feature example comment'
    #3-> git commit -m 'fix(ui): #4321 bugfix example comment'
    #4-> git commit -m 'fix!: #4321 chore example comment with possible breaking change'
    #5-> git commit -m 'chore!: #4321 chore example comment with possible breaking change'
    #6-> git commit -m 'refactor(chore)!: #4321 chore example comment with possible breaking change'
    #7-> git commit -m 'chore(fix)!: #4321 drop support for Python 2.6' -m 'BREAKING CHANGE: Some features not available in Python 2.7-.'

    More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/""")


def prepend_commit_msg() -> None:
    """Prepend the commit message with `text`."""
    msgfile = sys.argv[1]
    logging.debug('msgfile: %s', msgfile)

    with Path(msgfile).open() as f:
        contents = f.read().strip()
        logging.debug('%s', contents)

    regex = re.compile(COMMITFORMAT, flags=re.IGNORECASE)
    logging.debug('%s', str(regex.pattern))
    try:
        if not regex.match(contents):
            raise AssertionError  # noqa: TRY301
    except AssertionError:
        print(MESSAGERROR)
        sys.exit(1)
    print(MESSAGESUCCESS)
    sys.exit(0)


def run() -> None:
    """Run it."""
    prepend_commit_msg()


if __name__ == '__main__':
    raise SystemExit(run())

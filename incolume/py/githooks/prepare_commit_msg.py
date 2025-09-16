"""Module for validate commit message."""

# ruff: noqa: E501

import logging
import re
import sys
from pathlib import Path

import rich
from colorama import Fore, Style
from icecream import ic

from incolume.py.githooks import RULE_COMMITFORMAT, Result

MESSAGESUCCESS = (
    f'{Fore.GREEN}Commit message is validated [OK]{Style.RESET_ALL}'
)
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

    More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/
    [/]"""


def prepend_commit_msg() -> int:
    """Prepend the commit message with `text`."""
    msgfile = sys.argv[1]
    ic(msgfile)
    logging.debug('msgfile: %s', msgfile)

    result = Result(0, MESSAGESUCCESS)

    with Path(msgfile).open(encoding='utf-8') as f:
        content = f.read().strip()
        logging.debug('%s', ic(content))

    regex = re.compile(RULE_COMMITFORMAT, flags=re.IGNORECASE)
    logging.debug('%s', str(regex.pattern))
    if not regex.match(content):
        result = Result(1, MESSAGERROR)
    rich.print(result.message)
    sys.exit(result.code)


def run() -> None:
    """Run it."""
    prepend_commit_msg()


if __name__ == '__main__':
    raise SystemExit(run())

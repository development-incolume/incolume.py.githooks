"""Module for check branchname."""

# ruff: noqa: T201 E501

import logging
import platform
import re
import subprocess
import sys
from colorama import Fore, Style
from incolume.py.githooks import RULE_BRANCHNAME


BRANCH = subprocess.check_output(
    ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
).strip()


def run() -> None:
    """Run it."""
    logging.debug(platform.python_version_tuple())
    result = f'{Fore.GREEN}branching name rules. [OK]\033[0m'
    status = 0
    if not re.match(RULE_BRANCHNAME, BRANCH):
        result = (
            f'{Fore.RED}Your commit was rejected due to branching name '
            f'incompatible with rules.{Style.RESET_ALL}\n'
            f"{Fore.RED}Please rename your branch with '<(enhancement|feature|feat"
            f"|bug|bugfix|fix)>/epoch#<timestamp>' syntax{Style.RESET_ALL}"
        )
        status = 1
    print(result)
    sys.exit(status)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())

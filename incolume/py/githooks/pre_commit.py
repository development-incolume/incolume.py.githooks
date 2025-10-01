"""Module for check branchname."""

# ruff: noqa: T201

import logging
import platform
import re
import sys

from colorama import Fore, Style

from incolume.py.githooks.rules import RULE_BRANCHNAME
from incolume.py.githooks.utils import get_branchname


def valid_branchname() -> None:
    """Run it."""
    logging.debug(platform.python_version_tuple())
    result = f'{Fore.GREEN}Branching name rules. [OK]{Style.RESET_ALL}'
    status = 0
    if not re.match(RULE_BRANCHNAME, get_branchname()):
        result = (
            f'{Fore.RED}Your commit was rejected due to branching name '
            'incompatible with rules.\n'
            "Please rename your branch with '<(enhancement|feature|feat"
            f"|bug|bugfix|fix)>/epoch#<timestamp>' syntax{Style.RESET_ALL}"
        )
        status = 1
    print(result)
    sys.exit(status)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(valid_branchname())

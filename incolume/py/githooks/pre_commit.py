"""Module for check branchname."""

# ruff: noqa: T201 E501

import logging
import platform
import re
import subprocess
import sys

BRANCH = subprocess.check_output(
    ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
).strip()
REGEX = r'^((enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9\-]+))$'


def run() -> None:
    """Run it."""
    logging.debug(platform.python_version_tuple())
    if not re.match(REGEX, BRANCH):
        print(
            '\033[91mYour commit was rejected due to branching name '
            'incompatible with rules.\033[0m',
            "\033[91mPlease rename your branch with '<(enhancement|feature|feat"
            "|bug|bugfix|fix)>/epoch#<timestamp>' syntax\033[0m",
            sep='\n',
        )
        sys.exit(1)
    else:
        print()
        print('\033[92mbranching name rules. [OK]\033[0m')
        print()
        sys.exit(0)


if __name__ == '__main__':  # pragma: no cover
    raise SystemExit(run())

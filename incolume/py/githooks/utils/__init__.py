"""Module utils for project."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from os import getenv
from subprocess import check_output  # noqa: S404

from icecream import ic

from incolume.py.githooks.rules import SUCCESS as SUCCESS
from incolume.py.githooks.rules import Status

ic.disable()


def debug_enable() -> bool:
    """Enable debug mode."""
    valid: list = ['1', 'True', 'true']
    debug: bool = (
        False
        or getenv('INCOLUME_DEBUG_MODE') in valid
        or getenv('DEBUG_MODE') in valid
        or getenv('DEBUG') in valid
    )

    ic.disable()  # Disable by default

    if debug:
        ic.enable()

    return debug


@dataclass
class Result:
    """Result dataclass for hooks this project."""

    code: Status = Status.SUCCESS
    message: str = ''


def get_branchname() -> str:
    """Get current branch name."""
    branch = (
        check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],  # noqa: S607
        )
        .strip()
        .decode('utf-8')
    )
    logging.debug(ic(branch))
    return branch

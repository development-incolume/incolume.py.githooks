"""Module utils for project."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, auto
from os import getenv
from subprocess import check_output  # noqa: S404

from icecream import ic

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

ic.disable()


def debug_enable() -> bool:
    """Enable debug mode."""
    valid: list = ['1', 'True', 'true']
    debug: bool = (
        False
        or getenv('DEBUG') in valid
        or getenv('DEBUG_MODE') in valid
        or getenv('INCOLUME_DEBUG_MODE') in valid
    )

    ic.disable()  # Disable by default

    if debug:
        ic.enable()

    return debug


@dataclass
class Result:
    """Result dataclass for hooks this project."""

    code: int
    message: str


class AutoName(Enum):
    """Rule for next value."""

    @staticmethod
    def _generate_next_value_(
        name: str, start: any, count: any, last_values: any
    ) -> str:
        """Gernerate next value."""
        ic(name, start, count, last_values)
        return name.casefold()


class TypeCommit(AutoName):
    """Enum para Type commiting."""

    BUILD = auto()
    CHORE = auto()
    CI = auto()
    DOCS = auto()
    FEAT = auto()
    FIX = auto()
    PERF = auto()
    REFACTOR = auto()
    REVERT = auto()
    STYLE = auto()
    TEST = auto()
    BUGFIX = 'fix'
    DOC = 'docs'
    FEATURE = 'feat'
    TESTS = 'test'

    @classmethod
    def _missing_(cls, value: str) -> Self | None:
        """Get self instance."""
        value = value.upper().strip()
        for key, member in cls._member_map_.items():
            ic(value, key, member.name, member.value)
            if value == key:
                return member
        return None


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

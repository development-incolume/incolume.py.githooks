"""Module tests."""

from dataclasses import dataclass, field
from os import getenv

from icecream import ic

from incolume.py.githooks.rules import SUCCESS

DEBUG_MODE = getenv('DEBUG_MODE') or getenv('INCOLUME_DEBUG_MODE') or False
ic.disable()  # Disable by default

if DEBUG_MODE:
    ic.enable()


@dataclass
class Expected:
    """Expected values."""

    code: int = SUCCESS
    message: str = ''


@dataclass
class MainEntrance:
    """Entrance values."""

    commit_msg_file: str = ''
    commit_source: str = ''
    commit_hash: str = ''
    args: list[str] = field(default_factory=list)
    diff_output: str = ''

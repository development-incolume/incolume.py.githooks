"""Module tests."""

from dataclasses import dataclass, field

from incolume.py.githooks.rules import SUCCESS
from incolume.py.githooks.utils import debug_enable

debug_enable()


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

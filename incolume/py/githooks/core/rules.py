"""Module for rules of incolume githooks."""

# ruff: noqa: E501

from __future__ import annotations

import contextlib
import logging
from collections import ChainMap
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Final

from icecream import ic

with contextlib.suppress(ImportError, ModuleNotFoundError):
    from typing import Self  # type: ignore[import]

with contextlib.suppress(ImportError, ModuleNotFoundError):
    from typing_extensions import Self  # type: ignore[import]

if TYPE_CHECKING:
    from collections.abc import Callable

ic.disable()


def add_class_method_decorator(
    method: Callable, method_modo: Callable = classmethod
) -> Self:
    """Decorate dynamically add a class method into any class."""

    def wrapper(cls: Self) -> Self:
        """Wrap to add class method."""
        setattr(cls, method.__name__, method_modo(method))
        return cls

    return wrapper


def _missing_(cls: Self, value: str) -> Self | None:
    """Get self instance."""
    value = value.upper().strip()
    if value.isdigit():
        value = int(value)

    member = ChainMap(cls._member_map_, cls._value2member_map_).get(value)
    if member:
        logging.debug(ic(f'{value=}, {member.name=}, {member.value=}'))
    return member


def _generate_next_value_(
    name: str, start: any, count: any, last_values: any
) -> str:
    """Gernerate next value."""
    logging.debug(ic(name, start, count, last_values))
    return name.casefold()


def to_set(cls: Self) -> set[str]:
    """Enum to set."""
    return set(cls._value2member_map_)


def to_list(cls: Self) -> list[str]:
    """Enum to list."""
    return list(cls._value2member_map_)


@add_class_method_decorator(_generate_next_value_, method_modo=staticmethod)
@add_class_method_decorator(_missing_)
@add_class_method_decorator(to_set)
@add_class_method_decorator(to_list)
class AutoName(Enum):
    """Rule for next value."""


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
    BUG = 'fix'
    BUGFIX = 'fix'
    CD = 'ci'
    CICD = 'ci'
    DOC = 'docs'
    FEATURE = 'feat'
    TESTS = 'test'


class ProtectedBranchName(AutoName):
    """Protected Branchname for project."""

    DEV: str = auto()
    MAIN: str = auto()
    MASTER: str = auto()
    TAGS: str = auto()
    DEVELOPMENT: str = 'dev'


class RefusedBranchName(AutoName):
    """Refused Branchname for project."""

    WIP: str = auto()


@add_class_method_decorator(_missing_)
class Status(Enum):
    """Status result for CLI."""

    SUCCESS: int = 0
    FAILURE: int = 1

    def __or__(self, obj: Self | int) -> Status:
        """Override the | operator to combine Status values."""
        if isinstance(obj, int):
            obj = Status(obj)
        return Status(self.value | obj.value)

    def __ror__(self, value: Self | int) -> Status:
        """Override the | operator to combine Status values."""
        return self.__or__(value)


@add_class_method_decorator(_missing_)
class LoggingLevel(Enum):
    """The textual or numeric representation of logging level package."""

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


@dataclass
class Result:
    """Result dataclass for hooks this project."""

    code: Status = Status.SUCCESS
    message: str = ''


@dataclass
class MainEntrance:
    """Entrance values."""

    commit_msg_file: str = ''
    commit_source: str = ''
    commit_hash: str = ''
    args: list[str] = field(default_factory=list)
    diff_output: str = ''


REGEX_SEMVER: Final[str] = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
RULE_BRANCHNAME_REFUSED: Final[str] = (
    rf'^(?=.*({"|".join(RefusedBranchName.to_set())})).*$'
)
RULE_BRANCHNAME_NOT_REFUSED: Final[str] = (
    rf'^(?!.*({"|".join(RefusedBranchName.to_set())})).*$'
)
RULE_BRANCHNAME: Final[str] = (
    r'^((enhancement-\d{,11})|(feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9áàãâéèêíìóòõôúùüç\-_]+))$'
)
RULE_COMMITFORMAT: Final[str] = (
    r'^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\(.*\))?\!?: #[0-9]+) .*(\n.*)*)$'
)
SNAKE_CASE: Final[str] = r'^[a-z_][a-z_0-9]+$'

MESSAGES: Final[list[str]] = [
    'Boa! Continue o bom trabalho com a força, Jedi!',
    'Boa! Continue trabalhando campeão!',
    'Executado com sucesso.',
]

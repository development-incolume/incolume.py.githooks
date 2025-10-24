"""Module for rules of incolume githooks."""

# ruff: noqa: E501

from __future__ import annotations

import contextlib
from enum import Enum, auto
from typing import Final

from icecream import ic

with contextlib.suppress(ImportError, ModuleNotFoundError):
    from typing import Self  # type: ignore[import]

with contextlib.suppress(ImportError, ModuleNotFoundError):
    from typing_extensions import Self  # type: ignore[import]


ic.disable()


class AutoName(Enum):
    """Rule for next value."""

    @staticmethod
    def _generate_next_value_(
        name: str, start: any, count: any, last_values: any
    ) -> str:
        """Gernerate next value."""
        ic(name, start, count, last_values)
        return name.casefold()

    @classmethod
    def _missing_(cls, value: str) -> Self | None:
        """Get self instance."""
        value = value.upper().strip()
        for key, member in cls._member_map_.items():
            ic(value, key, member.name, member.value)
            if value == key:
                return member
        return None

    @classmethod
    def to_set(cls) -> set[str]:
        """Enum to set."""
        return set(cls._value2member_map_)

    @classmethod
    def to_list(cls) -> list[str]:
        """Enum to list."""
        return list(cls.to_set())


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


class Status(Enum):
    """Status result for CLI."""

    SUCCESS: int = 0
    FAILURE: int = 1

    @classmethod
    def _missing_(cls, value: str) -> Self | None:
        """Get self instance."""
        value = value.upper().strip()
        for key, member in cls._member_map_.items():
            ic(value, key, member.name, member.value)
            if value == key:
                return member
        return None

    def __or__(self, obj: Self | int) -> Status:
        """Override the | operator to combine Status values."""
        if isinstance(obj, int):
            obj = Status(obj)
        return Status(self.value | obj.value)

    def __ror__(self, value: Self | int) -> Status:
        """Override the | operator to combine Status values."""
        return self.__or__(value)


SUCCESS: Final[Status] = Status.SUCCESS
FAILURE: Final[Status] = Status.FAILURE

REGEX_SEMVER: Final[str] = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
RULE_BRANCHNAME: Final[str] = (
    r'^((enhancement-\d{,11})|(enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9áàãâéèêíìóòõôúùüç\-_]+))$'
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

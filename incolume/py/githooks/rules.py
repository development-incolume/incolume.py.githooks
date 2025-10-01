"""Module for rules of incolume githooks."""

# ruff: noqa: E501

from __future__ import annotations

from typing import Final

SUCCESS: Final[int] = 0
FAILURE: Final[int] = 1
REGEX_SEMVER: Final[str] = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
RULE_BRANCHNAME: Final[str] = (
    r'^((enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9\-]+))$'
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

"""Module for rules of incolume githooks."""

# ruff: noqa: E501

from __future__ import annotations

from typing import Final

SUCCESS: Final[int] = 0
FAILURE: Final[int] = 1
REGEX_SEMVER: Final = r'^\d+(\.\d+){2}((-\w+\.\d+)|(\w+\d+))?$'
RULE_BRANCHNAME: Final = r'^((enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9\-]+))$'
RULE_COMMITFORMAT = r'^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\(.*\))?\!?: #[0-9]+) .*(\n.*)*)$'

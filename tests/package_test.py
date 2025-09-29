"""Test module for package."""
# ruff: noqa: E501

from incolume.py.githooks.rules import (
    REGEX_SEMVER,
    RULE_BRANCHNAME,
    RULE_COMMITFORMAT,
)
import pytest
from typing import NoReturn


class TestCasePackage:
    """Test class for package."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                REGEX_SEMVER,
                '^\\d+(\\.\\d+){2}((-\\w+\\.\\d+)|(\\w+\\d+))?$',
                marks=[],
            ),
            pytest.param(
                RULE_BRANCHNAME,
                '^((enhancement|feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\\-[a-z0-9\\-]+))$',
                marks=[],
            ),
            pytest.param(
                RULE_COMMITFORMAT,
                '^(((Merge|Bumping|Revert)|(bugfix|build|chore|ci|docs|feat|feature|fix|other|perf|refactor|revert|style|test)(\\(.*\\))?\\!?: #[0-9]+) .*(\\n.*)*)$',
                marks=[],
            ),
        ],
    )
    def test_package(self, entrance, expected) -> NoReturn:
        """Test package."""
        assert entrance == expected

"""Test module for package."""
# ruff: noqa: E501

from incolume.py.githooks.rules import (
    REGEX_SEMVER,
    RULE_BRANCHNAME,
    RULE_COMMITFORMAT,
)
import pytest
from typing import NoReturn
import rich
from rich.console import Console


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
                r'^((enhancement-\d{,11})|(feature|feat|bug|bugfix|fix|refactor)/(epoch|issue)#([0-9]+)|([0-9]+\-[a-z0-9áàãâéèêíìóòõôúùüç\-_]+))$',
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

    def test_rich_output(self, capsys) -> NoReturn:
        """Test rich output."""
        console = Console()
        console.print('Hello from Rich!')
        rich.print('[red]Error message[/red]')

        captured = capsys.readouterr()

        assert 'Hello from Rich!' in captured.out
        assert 'Error message' in captured.out
        # Note: Rich typically renders ANSI escape codes for styling,
        # so direct string comparison might need to account for them.
        # You might need to strip ANSI codes or use a library to parse Rich's output.

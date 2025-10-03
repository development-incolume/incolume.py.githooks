"""Test for commit message hook."""

import pytest
from incolume.py.githooks.commit_msg import check, get_msg
from incolume.py.githooks.rules import MESSAGES


class TestCaseCommitMsg:
    """Test case for commit message hook."""

    @pytest.mark.parametrize(
        'expected',
        [
            pytest.param('Number of arguments: '),
            pytest.param('Arguments List: '),
        ],
    )
    def test_check(self, capsys, expected) -> None:
        """Test check function."""
        check()
        captured = capsys.readouterr()
        assert expected in captured.out

    def test_get_msg(self) -> None:
        """Test get_msg function."""
        result = get_msg()
        assert any(msg in result.strip() for msg in MESSAGES)

"""Module test for get_issue_from_branch."""

from incolume.py.githooks.cli.get_issue_from_branch import main
import pytest


class TestCaseGetIssueFromBranch:
    """Test cases CLI main for get_issue_from_branch function."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(('', '', ''), '', marks=[]),
        ]
    )
    def test_get_issue_from_branch(self, entrance, expected) -> None:
        """Test get_issue_from_branch function."""
        result = main(*entrance)
        assert result == expected

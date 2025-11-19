"""Test for commit message hook."""

from incolume.py.githooks.commit_msg import get_msg

from incolume.py.githooks.core.rules import MESSAGES


class TestCaseCommitMsg:
    """Test case for commit message hook."""

    def test_get_msg(self) -> None:
        """Test get_msg function."""
        result = get_msg()

        assert any(msg in result.strip() for msg in MESSAGES)

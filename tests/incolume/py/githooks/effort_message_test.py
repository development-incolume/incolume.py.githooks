"""Module for effort message tests."""

from incolume.py.githooks.effort_message import effort_msg, effort_random_msg
from incolume.py.githooks.core.rules import MESSAGES


class TestCaseEffort:
    """Test case for effort message."""

    def test_effort_msg(self) -> None:
        """Test effort message."""
        result = effort_msg('Test message')
        assert 'Test message' in result
        assert '\033[32m' in result  # Fore.GREEN

    def test_get_msg(self) -> None:
        """Test get_msg function."""
        result = effort_random_msg()

        assert any(msg in result.strip() for msg in MESSAGES)

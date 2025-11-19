"""Module for effort message tests."""

from incolume.py.githooks.effort_message import effort_msg


class TestCaseEffort:
    """Test case for effort message."""

    def test_effort_msg(self) -> None:
        """Test effort message."""
        result = effort_msg('Test message')
        assert 'Test message' in result
        assert '\033[32m' in result  # Fore.GREEN

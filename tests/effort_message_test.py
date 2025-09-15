"""Module for effort message tests."""

import pytest

from incolume.py.githooks import effort_message


class TestCaseEffort:
    """Test case for effort message."""

    def test_effort_msg(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test effort message."""
        effort_message.effort_msg('Test message')
        captured = capsys.readouterr()
        assert 'Test message' in captured.out
        assert '\033[32m' in captured.out  # Fore.GREEN

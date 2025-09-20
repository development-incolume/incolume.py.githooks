"""Module for effort message tests."""

import pytest

from incolume.py.githooks.effort_message import effort_msg, run


class TestCaseEffort:
    """Test case for effort message."""

    def test_effort_msg(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test effort message."""
        effort_msg('Test message')
        captured = capsys.readouterr()
        assert 'Test message' in captured.out
        assert '\033[32m' in captured.out  # Fore.GREEN

    def test_run(self, capsys) -> None:
        """Teste CLI."""
        run()
        captured = capsys.readouterr()
        assert 'Boa! Continue trabalhando com dedicação!' in captured.out

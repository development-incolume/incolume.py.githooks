"""Test module for prepare_commit_msg."""

from typing import NoReturn
import pytest


class TestCasePrepareCommitMsg:
    """Test class for prepare commit message."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                '',
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
        ],
    )
    def test_messages(self, entrance, expected) -> NoReturn:
        """Test messages."""
        assert entrance == expected

    @pytest.mark.xfail(reason='Test not implemented yet')
    def test_prepend_commit_msg(self) -> NoReturn:
        """Test prepend commit message."""
        assert False

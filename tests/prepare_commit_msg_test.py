"""Test module for prepare_commit_msg."""

from typing import NoReturn
import pytest
from incolume.py.githooks.prepare_commit_msg import (
    MESSAGERROR,
    MESSAGESUCCESS,
    prepend_commit_msg,
)
from icecream import ic


class TestCasePrepareCommitMsg:
    """Test class for prepare commit message."""

    __test__ = False

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                MESSAGERROR,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
            pytest.param(
                MESSAGESUCCESS,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
            pytest.param(
                prepend_commit_msg,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
            pytest.param(
                '',
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
        ],
    )
    def test_messages(self, entrance, expected) -> NoReturn:
        """Test messages."""
        assert ic(entrance) == expected

    @pytest.mark.xfail(reason='Test not implemented yet')
    def test_prepend_commit_msg(self) -> NoReturn:
        """Test prepend commit message."""
        assert False

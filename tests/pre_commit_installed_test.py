"""Tests for pre-commit installed."""

from typing import NoReturn
from incolume.py.githooks.pre_commit_installed import run
import pytest
from icecream import ic


class TestCaseInstalled:
    """Testcase for pre-commit installed."""

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param('', marks=[pytest.mark.xfail(raises=NotImplemented)]),
        ],
    )
    def test_precommit_installed(self, entrance) -> NoReturn:
        """Test for pre-commit installed."""
        ic(run, entrance)
        with pytest.raises(SystemExit):
            run()

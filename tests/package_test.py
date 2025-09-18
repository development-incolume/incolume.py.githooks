"""Test module for package."""

from incolume.py.githooks import (
    REGEX_SEMVER,
    RULE_BRANCHNAME,
    RULE_COMMITFORMAT,
    __version__,
)
import pytest
from typing import NoReturn


class TestCasePackage:
    """Test class for package."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                REGEX_SEMVER,
                '',
                marks=[],
            ),
            pytest.param(
                RULE_BRANCHNAME,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
            pytest.param(
                RULE_COMMITFORMAT,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
            pytest.param(
                __version__,
                '',
                marks=[pytest.mark.xfail(reason='Test not implemented yet')],
            ),
        ],
    )
    def test_package(self, entrance, expected) -> NoReturn:
        """Test package."""
        assert entrance == expected

"""Test module for decorators."""

import pytest
from incolume.py.githooks.utils import decorators


class TestCaseDecorators:
    """Test case for decorators module."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('value1', None),
            pytest.param('data', None),
        ],
    )
    def test_critical_log_call(self, entrance: str, expected: None) -> None:
        """Test critical_log_call decorator."""

        @decorators.critical_log_call
        def sample_function(a: str) -> None:
            """Sample function to be decorated."""
            return a

        result = sample_function(entrance)
        assert result == expected

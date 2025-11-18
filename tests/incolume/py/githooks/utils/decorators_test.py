"""Test module for decorators."""

import logging
import pytest
from incolume.py.githooks.utils import decorators


class TestCaseDecorators:
    """Test case for decorators module."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                'value1',
                'Function **sample_function** called with critial status.',
            ),
            pytest.param(
                'data',
                'Function **sample_function** called with critial status.',
            ),
        ],
    )
    def test_critical_log_call(
        self, caplog, entrance: str, expected: None
    ) -> None:
        """Test critical_log_call decorator."""

        @decorators.critical_log_call
        def sample_function(a: str) -> None:
            """Sample function to be decorated."""
            return a

        result = sample_function(entrance)
        assert result == entrance

        with caplog.at_level(logging.CRITICAL, logger="root.baz"):
            for record in caplog.records:
                match record.levelname:
                    case 'CRITICAL':
                        assert expected == record.getMessage()

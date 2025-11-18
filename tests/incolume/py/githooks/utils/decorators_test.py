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
                ['Function **sample_function** called with critial status.'],
            ),
            pytest.param(
                'data',
                ['Function **sample_function** called with critial status.'],
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

        with caplog.at_level(logging.CRITICAL):
            result = sample_function(entrance)

            assert result == entrance
            assert [rec.message for rec in caplog.records] == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                'value1',
                [('root', 10, 'executado via teste')],
            ),
            pytest.param(
                'data',
                [('root', 10, 'Function **sample_function** called.')],
            ),
        ],
    )
    def test_logging_call(self, caplog, entrance: str, expected: list) -> None:
        """Test logging_call decorator."""

        @decorators.logging_call('info', expected[0][2])
        def sample_function(a: str = 'word') -> None:
            """Sample function to be decorated."""
            return a

        result = sample_function(entrance)

        assert result == entrance
        assert expected[0][2] in [rec.message for rec in caplog.records]
        # assert set(expected).issubset(caplog.record_tuples)

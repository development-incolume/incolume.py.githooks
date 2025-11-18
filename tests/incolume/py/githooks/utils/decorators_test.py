"""Test module for decorators."""

import logging
import pytest
from incolume.py.githooks.utils import decorators
from os import environ


class TestCaseDecorators:
    """Test case for decorators module."""

    @pytest.mark.parametrize(
        ['entrance', 'expected', 'debug_mode'],
        [
            pytest.param(
                'value1',
                ['Function **sample_function** called with critial status.'],
                False,
            ),
            pytest.param(
                'data',
                ['Function **sample_function** called with critial status.'],
                True,
            ),
        ],
    )
    def test_critical_log_call(
        self, caplog, entrance: str, expected: None, *, debug_mode: bool
    ) -> None:
        """Test critical_log_call decorator."""

        @decorators.critical_log_call
        def sample_function(a: str) -> None:
            """Sample function to be decorated."""
            return a

        with caplog.at_level(logging.CRITICAL):
            environ['DEBUG_MODE'] = str(debug_mode)
            result = sample_function(entrance)

            assert result == entrance
            assert [rec.message for rec in caplog.records] == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected', 'debug_mode'],
        [
            pytest.param(
                'value1',
                ('root', 10, 'executado via teste'),
                False,
            ),
            pytest.param(
                'data',
                (
                    'root',
                    10,
                    'Function **sample_function** called into tests.',
                ),
                True,
            ),
        ],
    )
    def test_logging_call(
        self, caplog, entrance: str, expected: list, *, debug_mode: bool
    ) -> None:
        """Test logging_call decorator."""

        @decorators.logging_call(
            logging.getLevelName(expected[1]), expected[2]
        )
        def sample_function(a: str = 'word') -> None:
            """Sample function to be decorated."""
            return a

        environ['DEBUG_MODE'] = str(debug_mode)

        result = sample_function(entrance)

        assert result == entrance
        assert expected[2] in [rec.message for rec in caplog.records]
        assert set(caplog.record_tuples).issuperset({expected})

"""Test module for decorators."""

import logging
import pytest
from incolume.py.githooks.core.decorators import critical_log_call, logging_call
from incolume.py.githooks.core.rules import LoggingLevel
from os import environ
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Mapping


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
        self,
        caplog: pytest.LogCaptureFixture,
        entrance: str,
        expected: None,
        *,
        debug_mode: bool,
    ) -> None:
        """Test critical_log_call decorator."""

        @critical_log_call
        def sample_function(a: str) -> str:
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
                ('root', 'warning', 'executado via teste'),
                False,
            ),
            pytest.param(
                'data',
                (
                    'root',
                    'warn',
                    'Function **sample_function** called into tests.',
                ),
                True,
            ),
            pytest.param(
                'CRITICAL',
                ('root', 50, 'critical executado via teste por decorador'),
                False,
            ),
            pytest.param(
                'WARN',
                ('root', 30, 'warning executado via teste por decorador'),
                False,
            ),
            pytest.param(
                'ERROR',
                ('root', 40, 'error executado via teste por decorador'),
                False,
            ),
            pytest.param(
                'INFO',
                ('root', 20, 'info executado via teste por decorador'),
                False,
            ),
            pytest.param(
                'DEBUG',
                ('root', 10, 'debug executado via teste por decorador'),
                False,
            ),
        ],
    )
    def test_logging_call(
        self, caplog, entrance, expected, *, debug_mode
    ) -> None:
        """Test logging_call decorator."""

        @logging_call(LoggingLevel(expected[1]), expected[2])
        def sample_function(a: str = 'word') -> str:
            """Sample function to be decorated."""
            return a

        environ['DEBUG_MODE'] = str(debug_mode)
        expected = (expected[0], LoggingLevel(expected[1]).value, expected[2])

        result = sample_function(entrance)

        assert result == entrance
        assert expected[2] in [rec.message for rec in caplog.records]
        assert set(caplog.record_tuples).issuperset({expected})

    def test_multiples_logging_call(
        self,
        caplog,
    ) -> None:
        """Test logging_call decorator."""
        entrance: list[Mapping[str, Any]] = [
            {
                'level': LoggingLevel.DEBUG,
                'message': 'debug executado via teste',
            },
            {
                'level': LoggingLevel.WARNING,
                'message': 'warning executado via teste',
            },
            {
                'level': LoggingLevel.CRITICAL,
                'message': 'critical executado via teste',
            },
            {
                'level': LoggingLevel.ERROR,
                'message': 'error executado via teste',
            },
        ]

        @logging_call(**entrance[0])
        @logging_call(**entrance[1])
        @logging_call(**entrance[2])
        @logging_call(**entrance[3])
        def sample_function(a: str = 'word') -> str:
            """Sample function to be decorated."""
            return a

        sample_function()

        assert entrance[0]['message'] in [
            rec.message for rec in caplog.records
        ]
        assert set(caplog.record_tuples).issuperset(
            ('root', rec['level'].value, rec['message']) for rec in entrance
        )

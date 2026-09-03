"""Test module for decorators."""

import logging
import pytest
from incolume.py.githooks.core import decorators, debug_enable
from incolume.py.githooks.core.rules import LoggingLevel
from os import environ
from typing import TYPE_CHECKING, Any
from collections.abc import Callable
from icecream import ic

if TYPE_CHECKING:
    from collections.abc import Mapping


class TestCaseDecorators:
    """Test case for decorators module."""

    def setup_method(self, method: Callable[[], None]) -> None:
        """Set method."""
        ic(f'setup execution for {method.__name__}.')
        environ['DEBUG_MODE'] = '1'
        debug_enable()

    def teardown_method(self, method: Callable[[], None]) -> None:
        """Teardown method."""
        ic(f'teardown execution for {method.__name__}.')
        environ.pop('DEBUG_MODE')
        debug_enable()

    def test_my_decorator(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test para decorador my-decorator."""
        expected = (
            'Before function "sample_function" call',
            'After function "sample_function" call',
        )

        @decorators.my_decorator
        def sample_function(a: str) -> str:
            """Sample function to be decorated."""
            return a

        sample_function('abc')
        capture = capsys.readouterr()
        assert all(e in capture.err for e in expected)

    @pytest.mark.noci
    def test_simple_decorator(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test para decorador my-decorator."""
        expected = (
            'Debug mode enabled.',
            'Before function "sample_function" call',
            'After function "sample_function" call',
        )

        @decorators.simple_decorator
        def sample_function(a: str) -> str:
            """Sample function to be decorated."""
            return a

        environ['DEBUG_MODE'] = '1'
        debug_enable()

        sample_function('abc')
        capture = capsys.readouterr()
        assert all(e in capture.err for e in expected)

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

        @decorators.critical_log_call
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
        self,
        caplog: pytest.LogCaptureFixture,
        entrance: str,
        expected: tuple[str, int, str],
        *,
        debug_mode: bool,
    ) -> None:
        """Test logging_call decorator."""

        @decorators.logging_call(LoggingLevel(expected[1]), expected[2])
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
        caplog: pytest.LogCaptureFixture,
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

        @decorators.logging_call(**entrance[0])
        @decorators.logging_call(**entrance[1])
        @decorators.logging_call(**entrance[2])
        @decorators.logging_call(**entrance[3])
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

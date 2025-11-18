"""Test module for decorators."""

import logging
from pathlib import Path
import pytest
from incolume.py.githooks.utils import decorators
from tempfile import NamedTemporaryFile
from icecream import ic


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

        with (
            NamedTemporaryFile(delete=False, suffix='.log') as logger,
            caplog.at_level(logging.DEBUG, logger=logger.name),
        ):
            caplog.clear()
            sample_function(entrance)

            ic(logger.name)
            assert Path(logger.name).read_text(encoding='utf-8') == 'abc'

"""Tests for util."""

import pytest
from incolume.py.githooks.utils import debug_enable
from unittest import mock
import os
from icecream import ic
import contextlib


class TestCaseUtils:
    """Testcase for utils module."""

    def setup_method(self, method) -> None:
        """Set method."""
        ic(method)

        with contextlib.suppress(KeyError):
            del os.environ['INCOLUME_DEBUG_MODE']
            del os.environ['DEBUG_MODE']
            del os.environ['DEBUG']

    @pytest.mark.parametrize(
        ['envname', 'entrance', 'expected'],
        [
            pytest.param('DEBUG', '', False),
            pytest.param('DEBUG', 'false', False),
            pytest.param('DEBUG', 'true', True),
            pytest.param('DEBUG', True, True),
            pytest.param('DEBUG', False, False),
            pytest.param('DEBUG', 1, True),
            pytest.param('DEBUG', 0, False),
            pytest.param('DEBUG', None, False),
            pytest.param('DEBUG_MODE', '', False),
            pytest.param('DEBUG_MODE', 'false', False),
            pytest.param('DEBUG_MODE', 'true', True),
            pytest.param('DEBUG_MODE', True, True),
            pytest.param('DEBUG_MODE', False, False),
            pytest.param('DEBUG_MODE', 1, True),
            pytest.param('DEBUG_MODE', 0, False),
            pytest.param('DEBUG_MODE', None, False),
            pytest.param('INCOLUME_DEBUG_MODE', '', False),
            pytest.param('INCOLUME_DEBUG_MODE', 'false', False),
            pytest.param('INCOLUME_DEBUG_MODE', 'true', True),
            pytest.param('INCOLUME_DEBUG_MODE', True, True),
            pytest.param('INCOLUME_DEBUG_MODE', False, False),
            pytest.param('INCOLUME_DEBUG_MODE', 1, True),
            pytest.param('INCOLUME_DEBUG_MODE', 0, False),
            pytest.param('INCOLUME_DEBUG_MODE', None, False),
        ],
    )
    def test_debug_enable(self, envname, entrance, expected) -> None:
        """Test debug enable."""
        with mock.patch.dict(os.environ, clear=True):
            os.environ[envname] = str(entrance)
            assert debug_enable() is expected

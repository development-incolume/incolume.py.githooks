"""Tests for util."""

import pytest
from incolume.py.githooks import core
from incolume.py.githooks.core.rules import TypeCommit
from unittest import mock
import os
from icecream import ic
import contextlib
from unittest.mock import patch


class TestCaseUtilsEnviron:
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
            assert core.debug_enable() is expected


class TestCaseUtilsModule:
    """Testcase for utils module."""

    @pytest.mark.parametrize(
        'entrance',
        [pytest.param('A\tincolume/py/githooks/module_xpto.py', marks=[])],
    )
    def test_get_diff(self, entrance, mocker) -> None:
        """Test get_diff_files function."""
        mocker.patch('subprocess.check_output', return_value=entrance)
        assert core.get_git_diff() == entrance

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('build', 'build', marks=[]),
            pytest.param('chore', 'chore', marks=[]),
            pytest.param('ci', 'ci', marks=[]),
            pytest.param('docs', 'docs', marks=[]),
            pytest.param('feat', 'feat', marks=[]),
            pytest.param('fix', 'fix', marks=[]),
            pytest.param('perf', 'perf', marks=[]),
            pytest.param('refactor', 'refactor', marks=[]),
            pytest.param('revert', 'revert', marks=[]),
            pytest.param('style', 'style', marks=[]),
            pytest.param('test', 'test', marks=[]),
            pytest.param('bugfix', 'fix', marks=[]),
            pytest.param('doc', 'docs', marks=[]),
            pytest.param('feature', 'feat', marks=[]),
            pytest.param('tests', 'test', marks=[]),
            pytest.param('BUILD', 'build', marks=[]),
            pytest.param('CHORE', 'chore', marks=[]),
            pytest.param('CI', 'ci', marks=[]),
            pytest.param('DOCS', 'docs', marks=[]),
            pytest.param('FEAT', 'feat', marks=[]),
            pytest.param('FIX', 'fix', marks=[]),
            pytest.param('PERF', 'perf', marks=[]),
            pytest.param('REFACTOR', 'refactor', marks=[]),
            pytest.param('REVERT', 'revert', marks=[]),
            pytest.param('STYLE', 'style', marks=[]),
            pytest.param('TEST', 'test', marks=[]),
            pytest.param('BUGFIX', 'fix', marks=[]),
            pytest.param('DOC', 'docs', marks=[]),
            pytest.param('FEATURE', 'feat', marks=[]),
            pytest.param('TESTS', 'test', marks=[]),
            pytest.param(' BugFix ', 'fix', marks=[]),
            pytest.param('BugFix ', 'fix', marks=[]),
            pytest.param(' BugFix', 'fix', marks=[]),
            pytest.param(
                'buggy',
                {'expected_exception': ValueError, 'match': None},
                marks=[],
            ),
        ],
    )
    def test_type_commit(self, entrance, expected) -> None:
        """Test for Enum TypeCommit."""
        if 'expected_exception' in expected:
            with pytest.raises(**expected):  # noqa: PT010
                TypeCommit(entrance)
        else:
            assert TypeCommit(entrance).value == expected

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param('80-fatora-código\n', marks=[]),
            pytest.param('\n80-açaí-código\n\n', marks=[]),
        ],
    )
    def test_get_branchname(self, entrance: str) -> None:
        """Test for get branch names."""
        with patch.object(
            core.subprocess, 'check_output', return_value=entrance.encode()
        ):
            assert core.get_branchname() == entrance.strip()

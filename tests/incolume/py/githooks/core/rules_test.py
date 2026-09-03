"""Test for rules module."""

from typing import Any

import pytest
import incolume.py.githooks.core.rules as pkg
from tempfile import gettempdir
from pathlib import Path
from inspect import stack


class TestCaseRules:
    """Test case rules."""

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(0),
            pytest.param(1),
        ],
    )
    def test_status_value(self, entrance: int) -> None:
        """Test status enum."""
        assert pkg.Status(entrance).value == entrance

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('success', 0),
            pytest.param('failure', 1, marks=[]),
            pytest.param(0, 0, marks=[]),
            pytest.param(1, 1, marks=[]),
            pytest.param('SUCCESS', 0),
            pytest.param('FAILURE', 1, marks=[]),
            pytest.param('0', 0),
            pytest.param('1', 1),
        ],
    )
    def test_status_enum(self, entrance: str | int, expected: int) -> None:
        """Test status enum."""
        assert pkg.Status(entrance).value == expected

    @pytest.mark.parametrize(
        ['ent0', 'ent1', 'expected'],
        [
            pytest.param(pkg.Status(0), pkg.Status(0), pkg.Status(0)),
            pytest.param(pkg.Status(0), pkg.Status(1), pkg.Status(1)),
            pytest.param(pkg.Status(1), pkg.Status(0), pkg.Status(1)),
            pytest.param(pkg.Status(1), pkg.Status(1), pkg.Status(1)),
            pytest.param(pkg.Status(0), 0, pkg.Status(0)),
            pytest.param(pkg.Status(0), 1, pkg.Status(1)),
            pytest.param(0, pkg.Status(0), pkg.Status(0)),
            pytest.param(1, pkg.Status(0), pkg.Status(1)),
        ],
    )
    def test_status_op(
        self, ent0: pkg.Status, ent1: pkg.Status, expected: pkg.Status
    ) -> None:
        """Status operations."""
        assert ent0 | ent1 == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                '0',
                pkg.Status(0),
            ),
            pytest.param(
                5,
                {
                    'expected_exception': ValueError,
                    'match': '5 is not a valid Status',
                },
            ),
            pytest.param(
                '-1',
                {
                    'expected_exception': ValueError,
                    'match': "'-1' is not a valid Status",
                },
            ),
            pytest.param(
                'fail',
                {
                    'expected_exception': ValueError,
                    'match': "'fail' is not a valid Status",
                },
            ),
            pytest.param('failure', pkg.Status.FAILURE),
        ],
    )
    def test_status_missing(
        self, entrance: str, expected: pkg.Status | dict[str, object]
    ) -> None:
        """Status missing."""
        try:
            assert pkg.Status(entrance) == expected
        except ValueError:
            with pytest.raises(**expected):  # ruff: ignore[pytest-raises-without-exception]
                assert pkg.Status(entrance)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(0, 0),
            pytest.param(1, 1),
        ],
    )
    def test_status_casting(self, entrance: int, expected: int) -> None:
        """Casting Status."""
        assert pkg.Status(entrance).value == expected

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(0),
            pytest.param(1),
        ],
    )
    def test_status_value_int(self, entrance: int) -> None:
        """Casting Status."""
        assert isinstance(pkg.Status(entrance).value, int)

    def test_type_commit_tolist(self) -> None:
        """Test TypeCommit enum."""
        assert sorted(pkg.TypeCommit.to_list()) == [
            'build',
            'chore',
            'ci',
            'docs',
            'feat',
            'fix',
            'perf',
            'refactor',
            'revert',
            'style',
            'test',
        ]

    def test_type_commit_toset(self) -> None:
        """Test TypeCommit enum."""
        assert pkg.TypeCommit.to_set() == {
            'docs',
            'build',
            'feat',
            'chore',
            'perf',
            'refactor',
            'revert',
            'style',
            'test',
            'ci',
            'fix',
        }

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('WARNING', 30),
            pytest.param('WARN', 30),
            pytest.param('Warn', 30),
            pytest.param('warn', 30),
            pytest.param(pkg.logging.WARNING, 30),
            pytest.param(pkg.logging.WARN, 30),
            pytest.param(
                'warnning',
                {
                    'expected_exception': ValueError,
                    'match': r'.* is not a valid LoggingLevel',
                },
            ),
            pytest.param('30', 30),
        ],
    )
    def test_logging_level(
        self, entrance: str | int, expected: int | dict[str, Any] | None
    ) -> None:
        """Test LoggingLevel."""
        match expected:
            case int():
                assert pkg.LoggingLevel(entrance).value == expected
            case dict():
                with pytest.raises(**expected):  # ruff: ignore[pytest-raises-without-exception]
                    pkg.LoggingLevel(entrance)
            case _:
                pytest.mark.xfail(reason='Not implemented yet.')

    @pytest.mark.parametrize(
        ['method', 'mode', 'expected'],
        [
            pytest.param(int, None, 'int', marks=[]),
            pytest.param(float, 'staticmethod', 'float', marks=[]),
            pytest.param(int, 'classmethod', 'int', marks=[]),
        ],
    )
    def test_add_class_method_decorator(
        self, method: type, mode: str | None, expected: str
    ) -> None:
        """Test add_class_method_decorator."""

        @pkg.add_class_method_decorator(method=method, method_modo=mode)
        class Klass:
            """Fake class for test."""

        obj = Klass()

        assert isinstance(obj, Klass)
        assert expected in dir(obj)

    @pytest.mark.parametrize(
        ['test_file', 'method', 'expected'],
        [
            pytest.param('module/file.py', 'refname', 'file', marks=[]),
            pytest.param(
                'module/__init__.py', 'refname', '__init__', marks=[]
            ),
            pytest.param('module/file.py', 'has_filename', True, marks=[]),
            pytest.param('module/file.py', 'is_dundle_init', False, marks=[]),
            pytest.param(
                'module/__init__.py', 'is_dundle_init', True, marks=[]
            ),
            pytest.param('module/file.py', 'is_python_file', True, marks=[]),
            pytest.param(
                'module/README.md', 'is_python_file', False, marks=[]
            ),
            pytest.param(
                'tests/file.py',
                'is_not_test_filename',
                False,
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                'module/file_tests.py',
                'is_not_test_filename',
                False,
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                'module/file.py',
                'is_not_test_filename',
                True,
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                'module/__init__.py',
                'is_not_test_filename',
                True,
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                'tests/file.py',
                'has_test_pathname',
                True,
                marks=[],
            ),
            pytest.param(
                'module/file.py',
                'has_test_pathname',
                False,
                marks=[pytest.mark.xfail],
            ),
        ],
    )
    def test_request_file_class_model(
        self, test_file: str, method: str, expected: Any
    ) -> None:
        """Test for RequestFl."""
        fout: Path = (
            Path(gettempdir())
            / self.__class__.__name__
            / stack()[0][3]
            / test_file
        )
        tfile: pkg.RequestFl = pkg.RequestFl(fout)
        result = getattr(tfile, method)
        assert result == expected

"""Module to validate filenames."""

from __future__ import annotations
from pathlib import Path
from typing import NoReturn
from tempfile import NamedTemporaryFile, gettempdir

from icecream import ic
import pytest
from incolume.py.githooks.core.rules import (
    Expected,
    Result,
    FAILURE,
    SUCCESS,
    Status,
)
from incolume.py.githooks.valid_filename import ValidateFilename
from inspect import stack


class TestCaseValidFilename:
    """Test cases for the `is_valid_filename` function."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    @pytest.fixture(scope='class')
    def filefortest(self) -> Path:
        """Get the path to this file."""
        with NamedTemporaryFile(dir=gettempdir(), suffix='.py') as tf:
            return Path(tf.name)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                'alphabet',
                'abcdefghijklmnopqrstuvwxyz0123456789_áàãâéèêíìîóòõôúùûç',
                marks=[],
            ),
            pytest.param('considers_underscore', True, marks=[]),
            pytest.param('min_len', 3, marks=[]),
            pytest.param('max_len', 256, marks=[]),
            pytest.param('code', SUCCESS, marks=[]),
            pytest.param('message', '', marks=[]),
        ],
    )
    def test_validfilename_init(
        self, filefortest: Path, entrance: str, expected: object
    ) -> NoReturn:
        """Test the initialization of the ValidateFilename class."""
        vf = ValidateFilename(filename=filefortest)
        assert filefortest.as_posix() in vf.filename.as_posix()
        assert getattr(vf, entrance) == expected

    def test_refname(self, filefortest: Path) -> NoReturn:
        """Test the refname property."""
        vf = ValidateFilename(filename=filefortest)
        assert vf.refname == filefortest.stem

    @pytest.mark.parametrize(
        ['filename', 'min_len', 'expected'],
        [
            pytest.param(
                'ab.py',
                3,
                Expected(
                    code=1,
                    message='[red]Name too short (self.min_len=3):',
                ),
                marks=[],
            ),
            pytest.param(
                'abcefghij.py',
                10,
                Expected(
                    code=1,
                    message='[red]Name too short (self.min_len=10):',
                ),
                marks=[],
            ),
            pytest.param('abcd.py', 3, Expected(code=0, message=''), marks=[]),
        ],
    )
    def test_is_too_short(
        self, filefortest: Path, filename, min_len, expected: Expected
    ) -> NoReturn:
        """Test the is_too_short method."""
        filename = filefortest.with_name(filename)
        vf = ValidateFilename(filename=filename, min_len=min_len)
        result = vf.is_too_short()
        assert Status(result.code) == Status(expected.code)
        assert expected.message in result.message

    @pytest.mark.parametrize(
        ['filename', 'max_len', 'expected'],
        [
            pytest.param(
                'abcefghijk.py',
                9,
                Expected(
                    code=1,
                    message='\n[red]Name too long (self.max_len=9):',
                ),
                marks=[],
            ),
            pytest.param(
                'abcefghijk.py',
                10,
                Expected(
                    code=0,
                    message='',
                ),
                marks=[],
            ),
        ],
    )
    def test_is_too_long(
        self, filefortest: Path, filename, max_len, expected: Expected
    ) -> NoReturn:
        """Test the is_too_long method."""
        filename = filefortest.with_name(filename)
        vf = ValidateFilename(filename=filename, max_len=max_len)
        result = vf.is_too_long()
        assert Status(result.code) == Status(expected.code)
        assert expected.message in result.message

    @pytest.mark.parametrize(
        ['filename', 'expected'],
        [
            pytest.param(
                'valid_name.py', Expected(code=0, message=''), marks=[]
            ),
            pytest.param(
                'invalidName.py',
                Expected(
                    code=1,
                    message='[red]Filename is not in snake_case:',
                ),
                marks=[],
            ),
        ],
    )
    def test_is_snake_case(
        self, filefortest: Path, filename: Path, expected: Expected
    ) -> NoReturn:
        """Test the is_snake_case method."""
        vf = ValidateFilename(filename=filefortest.with_name(filename))
        result = vf.is_snake_case()
        assert Status(result.code) == Status(expected.code)
        assert expected.message in result.message

    @pytest.mark.parametrize(
        ['filename', 'expected'],
        [
            pytest.param(
                test_dir / 'tests' / 'fake_module_test.py',
                Result(SUCCESS, ['']),
                marks=[],
            ),  # Path, but valid name
            pytest.param(
                test_dir / 'tests' / 'fake_module.py',
                Result(
                    FAILURE,
                    (
                        'Parece ser um arquivo de test.\n'
                        'Try: tests/fake_module_test.py'
                    ),
                ),
                marks=[],
            ),  # Path, but valid name
            pytest.param(
                'incolume/py/githooks/fakepackage/test_fake_module.py',
                Result(FAILURE, 'kxz'),
                marks=[pytest.mark.xfail(reason='Not implemented yet')],
            ),  # Path, but valid name
            pytest.param(
                'incolume/py/githooks/fakepackage/fake_test_module.py',
                Result(FAILURE, 'kxz'),
                marks=[pytest.mark.xfail(reason='Not implemented yet')],
            ),  # Path, but valid name
        ],
    )
    def test_has_testing_in_pathname(
        self, filename, expected: Expected
    ) -> NoReturn:
        """Test the has_testing_in_pathname method."""
        vf = ValidateFilename(filename=filename)
        result = vf.has_testing_in_filename()
        assert Status(result.code) == Status(expected.code)
        assert all(m1 in result.message for m1 in expected.message)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'filename': '__main__.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': '__init__.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': '_validname01.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname01.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'valid_name01.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname_01.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'valid_name_01.py'},
                Result(SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname.py'},
                Result(SUCCESS, ''),
                id='validname.py',
            ),
            pytest.param(
                {'filename': 'valid_name.py'},
                Result(SUCCESS, ''),
                id='valid_name.py',
            ),
            pytest.param(
                {'filename': 'another_valid_name.txt'},
                Result(SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'a_bc.py', 'min_len': 3},
                Result(SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'snake_case_file.md'},
                Result(SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': '0_invalid_name.py'},
                Result(
                    FAILURE,
                    '\n[red]Filename is not in'
                    ' snake_case: 0_invalid_name.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '0_Invalid_Name.py'},
                Result(
                    FAILURE,
                    '[red]Filename is not in snake_case: 0_Invalid_Name.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '0InvalidName.py'},
                Result(
                    FAILURE,
                    '[red]Filename is not in snake_case: 0InvalidName.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'InvalidName.py'},
                Result(
                    FAILURE,
                    '[red]Filename is not in snake_case: InvalidName.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'short.py', 'min_len': 6},
                Result(FAILURE, 'Name too short (min_len=6): short.py'),
                marks=[],
            ),  # Too short
            pytest.param(
                {'filename': 'noextension'}, Result(SUCCESS, ''), marks=[]
            ),  # No extension, but valid name
            pytest.param(
                {'filename': 'UPPERCASE.TXT'},
                Result(
                    FAILURE,
                    '[red]Name too short (min_len=3): UPPERCASE.TXT[/]'
                    '\n[red]Filename is not in snake_case: UPPERCASE.TXT[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'mixed_Case.py'},
                Result(
                    FAILURE, 'Filename is not in snake_case: mixed_Case.py'
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '.hiddenfile'},
                Result(SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.gitignore'},
                Result(SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.editorconfig'},
                Result(SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.coveragerc'},
                Result(SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '..doublehidden'},
                Result(
                    FAILURE,
                    'Name too short (min_len=3): ..doublehidden[/]\n'
                    '[red]Filename is not in snake_case: ..doublehidden',
                ),
            ),  # Hidden file, no name
            pytest.param(
                {
                    'filename': 'a_b_c_d_e_f_g_h_i_j_k_l_m'
                    '_n_o_p_q_r_s_t_u_v_w_x_y_z.py'
                },
                Result(SUCCESS, ''),
            ),  # Long valid name
            pytest.param(
                {'filename': 'a' * 256 + '.py'}, Result(SUCCESS, '')
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'a' * 257 + '.py'},
                Result(FAILURE, 'Name too long (max_len=256)'),
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'incolume/py/fakepackage/fake_test_module.py'},
                Result(FAILURE, 'asdf'),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'incolume/py/fakepackage/fake_module.py'},
                Result(SUCCESS, ''),
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module.py'},
                Result(FAILURE, 'asd'),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/test_fake_module.py'},
                Result(FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module_test.py'},
                Result(SUCCESS, ''),
                marks=[],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'test/fake_module.py'},
                Result(FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'test/test_fake_module.py'},
                Result(FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
        ],
    )
    def test_check_if_valid_filenames(
        self, entrance: dict, expected: Result
    ) -> NoReturn:
        """Test invalid filenames."""
        result = ValidateFilename.is_valid(**entrance)
        ic(result)
        assert Status(result.code) is Status(expected.code)  # Not snake_case
        assert expected.message in result.message

"""Module to validate filenames."""

from __future__ import annotations
from pathlib import Path
from tempfile import NamedTemporaryFile, gettempdir
from typing import TYPE_CHECKING

from icecream import ic
import pytest
from incolume.py.githooks.core.rules import (
    Result,
    Status,
)
from incolume.py.githooks.validate_filename import ValidateFilename
from inspect import stack

if TYPE_CHECKING:
    from collections.abc import Mapping


class TestCaseValidFilename:
    """Test cases for the `is_valid_filename` function."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    @pytest.fixture(scope='class')
    def filefortest(self) -> Path:
        """Get the path to this file."""
        dout: Path = self.test_dir / 'files'
        dout.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=dout, suffix='.py') as tf:
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
            pytest.param('code', Status.SUCCESS, marks=[]),
            pytest.param('messages', [''], marks=[]),
        ],
    )
    def test_validfilename_init(
        self, filefortest: Path, entrance: str, expected: object
    ) -> None:
        """Test the initialization of the ValidateFilename class."""
        vf = ValidateFilename(filename=filefortest)
        assert filefortest.as_posix() in vf.filename.as_posix()
        assert getattr(vf, entrance) == expected

    def test_refname(self, filefortest: Path) -> None:
        """Test the refname property."""
        vf = ValidateFilename(filename=filefortest)
        assert vf.refname == filefortest.stem

    @pytest.mark.parametrize(
        ['filename', 'min_len', 'expected'],
        [
            pytest.param(
                'ab.py',
                3,
                Result(
                    code=1,
                    message='[red]Name too short (self.min_len=3):',
                ),
                marks=[],
            ),
            pytest.param(
                'abcefghij.py',
                10,
                Result(
                    code=1,
                    message='[red]Name too short (self.min_len=10):',
                ),
                marks=[],
            ),
            pytest.param('abcd.py', 3, Result(code=0, message=''), marks=[]),
        ],
    )
    def test_is_too_short(
        self, filefortest: Path, filename: str, min_len: int, expected: Result
    ) -> None:
        """Test the is_too_short method."""
        fltest = filefortest.with_name(filename)
        vf = ValidateFilename(filename=fltest, min_len=min_len)
        result = vf.is_too_short()
        assert Status(result.code) == Status(expected.code)
        # assert any({expected.message}.issubset(m) for m in result.messages)
        assert (expected.message in m for m in result.messages)

    @pytest.mark.parametrize(
        ['filename', 'max_len', 'expected'],
        [
            pytest.param(
                'abcefghijk.py',
                9,
                Result(
                    code=1,
                    message='\n[red]Name too long (self.max_len=9):',
                ),
                marks=[],
            ),
            pytest.param(
                'abc.py',
                2,
                Result(
                    code=1,
                    message='\n[red]Name too long (self.max_len=2):',
                ),
                marks=[],
            ),
            pytest.param(
                'abcefghijk.py',
                10,
                Result(
                    code=0,
                    message='',
                ),
                marks=[],
            ),
        ],
    )
    def test_is_too_long(
        self, filefortest: Path, filename: str, max_len: int, expected: Result
    ) -> None:
        """Test the is_too_long method."""
        fltest = filefortest.with_name(filename)
        vf = ValidateFilename(filename=fltest, max_len=max_len)
        result = vf.is_too_long()
        assert Status(result.code) == Status(expected.code)
        assert (expected.message in m for m in result.messages)

    @pytest.mark.parametrize(
        ['filename', 'expected'],
        [
            pytest.param(
                'valid_name.py', Result(code=0, message=''), marks=[]
            ),
            pytest.param(
                'invalidName.py',
                Result(
                    code=1,
                    message='[red]Filename is not in snake_case:',
                ),
                marks=[],
            ),
            pytest.param('__init__.py', Result(code=0, message=''), marks=[]),
            pytest.param('_core.py', Result(code=0, message=''), marks=[]),
            pytest.param('_core4pkg.py', Result(code=0, message=''), marks=[]),
            pytest.param('README.md', Result(code=0, message=''), marks=[]),
        ],
    )
    def test_is_snake_case(
        self, filefortest: Path, filename: Path, expected: Result
    ) -> None:
        """Test the is_snake_case method."""
        vf = ValidateFilename(filename=filefortest.with_name(str(filename)))
        result = vf.is_snake_case()
        assert Status(result.code) == Status(expected.code)
        assert (expected.message in m for m in result.messages)

    @pytest.mark.parametrize(
        ['filename', 'expected'],
        [
            pytest.param(
                test_dir / 'tests' / 'fake_module_test.py',
                True,
                marks=[],
            ),
            pytest.param(
                test_dir / 'tests' / 'fake_module.py',
                True,
                marks=[],
            ),
            pytest.param(
                Path('incolume/py/githooks/fakepackage/test_fake_module.py'),
                False,
                marks=[],
            ),
            pytest.param(
                'incolume/py/githooks/fakepackage/fake_test_module.py',
                False,
                marks=[],
            ),
        ],
    )
    def test_has_testing_in_pathname(
        self, filename: str, *, expected: bool
    ) -> None:
        """Test the has_testing_in_pathname method."""
        vf = ValidateFilename(filename=filename)
        result = vf.rule_has_test_in_pathname
        assert result == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            # If is dundler init file
            pytest.param(
                {'filename': 'a.py', 'rule': 'rule_is_dundle_init'}, False
            ),
            pytest.param(
                {'filename': '__init__.py', 'rule': 'rule_is_dundle_init'}, True
            ),
            pytest.param(
                {'filename': 'tests/__init__.py', 'rule': 'rule_is_dundle_init'}, True
            ),
            # If is Python file
            pytest.param(
                {'filename': 'a.py', 'rule': 'rule_is_python_file'}, True
            ),
            pytest.param(
                {'filename': 'a.txt', 'rule': 'rule_is_python_file'}, False
            ),
            pytest.param(
                {'filename': '__init__.py', 'rule': 'rule_is_python_file'},
                True,
            ),
            # If has test into pathname
            pytest.param(
                {'filename': 'a.txt', 'rule': 'rule_has_test_in_pathname'},
                False,
            ),
            pytest.param(
                {
                    'filename': 'test/a.txt',
                    'rule': 'rule_has_test_in_pathname',
                },
                True,
            ),
            pytest.param(
                {
                    'filename': 'tests/a.txt',
                    'rule': 'rule_has_test_in_pathname',
                },
                True,
            ),
            pytest.param(
                {
                    'filename': 'test/__init__.py',
                    'rule': 'rule_has_test_in_pathname',
                },
                True,
            ),
            # If has test into filename
            pytest.param(
                {'filename': 'a.txt', 'rule': 'rule_has_test_into_filename'},
                False,
            ),
            pytest.param(
                {
                    'filename': 'test_a.txt',
                    'rule': 'rule_has_test_into_filename',
                },
                True,
            ),
            pytest.param(
                {
                    'filename': 'a_tests.txt',
                    'rule': 'rule_has_test_into_filename',
                },
                True,
            ),
            pytest.param(
                {
                    'filename': 'a_test.py',
                    'rule': 'rule_has_test_into_filename',
                },
                True,
            ),
            pytest.param(
                {
                    'filename': 'test/__init__.py',
                    'rule': 'rule_has_test_into_filename',
                },
                True,
            ),
            # If has filename ends with test or tests
            pytest.param(
                {
                    'filename': 'test/__init__.py',
                    'rule': 'rule_has_filename_ends_with_test',
                },
                False,
            ),
            pytest.param(
                {
                    'filename': 'a_test.py',
                    'rule': 'rule_has_filename_ends_with_test',
                },
                True,
                marks=[]
            ),
            pytest.param(
                {
                    'filename': 'a_tests.py',
                    'rule': 'rule_has_filename_ends_with_test',
                },
                True,
                marks=[]
            ),
            pytest.param(
                {
                    'filename': 'test_s.py',
                    'rule': 'rule_has_filename_ends_with_test',
                },
                False,
            ),
            # rule_not_started_with_number
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': '4file.py'}, False),
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': '4_file.py'}, False),
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': '4.py'}, False),
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': 'file.py'}, True),
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': 'file_4.py'}, True),
            pytest.param({'rule': 'rule_not_started_with_number', 'filename': 'f4.py'}, True),
        ],
    )
    def test_rules(
        self, entrance: Mapping[str, str], *, expected: bool
    ) -> None:
        """Test rules."""
        vf = ValidateFilename(entrance.get('filename'))
        assert getattr(vf, entrance.get('rule', '')) == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('', True, marks=[]),
            pytest.param('4file.py', True, marks=[]),
            pytest.param('README.md', True, marks=[]),
            pytest.param('module/module_test.py', False, marks=[pytest.mark.xfail]),
            pytest.param('module/module_tests.py', False, marks=[pytest.mark.xfail]),
            pytest.param('module/tests_module.py', False, marks=[pytest.mark.xfail]),
            pytest.param('test/README.md', True, marks=[]),
            pytest.param('test/__init__.py', True, marks=[]),
            pytest.param('test/module_test.py', True, marks=[pytest.mark.xfail]),
            pytest.param('test/module_tests.py', True, marks=[pytest.mark.xfail]),
            pytest.param('test/test_module.py', False, marks=[pytest.mark.xfail]),
            pytest.param('test/tests_module.py', False, marks=[pytest.mark.xfail]),
            pytest.param('tests/README.md', True, marks=[]),
            pytest.param('tests/module_test.py', True, marks=[pytest.mark.xfail]),
            pytest.param('tests/module_tests.py', True, marks=[pytest.mark.xfail]),
            pytest.param('tests/test_module.py', False, marks=[pytest.mark.xfail]),
        ],
    )
    def test_is_valid_testing_filename(
        self, entrance: str, *, expected: bool
    ) -> None:
        """Test is_valid_testing_filename."""
        vf = ValidateFilename(filename=entrance)
        assert vf.is_valid_testing_filename() == expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'filename': '__main__.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': '__init__.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': '_validname01.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname01.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'valid_name01.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname_01.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'valid_name_01.py'},
                Result(Status.SUCCESS, ''),
            ),
            pytest.param(
                {'filename': 'validname.py'},
                Result(Status.SUCCESS, ''),
                id='validname.py',
            ),
            pytest.param(
                {'filename': 'valid_name.py'},
                Result(Status.SUCCESS, ''),
                id='valid_name.py',
            ),
            pytest.param(
                {'filename': 'another_valid_name.txt'},
                Result(Status.SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'a_bc.py', 'min_len': 3},
                Result(Status.SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'snake_case_file.md'},
                Result(Status.SUCCESS, ''),
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': '0_invalid_name.py'},
                Result(
                    Status.FAILURE,
                    '\n[red]Filename is not in'
                    ' snake_case: 0_invalid_name.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '0_Invalid_Name.py'},
                Result(
                    Status.FAILURE,
                    '[red]Filename is not in snake_case: 0_Invalid_Name.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '0InvalidName.py'},
                Result(
                    Status.FAILURE,
                    '[red]Filename is not in snake_case: 0InvalidName.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'InvalidName.py'},
                Result(
                    Status.FAILURE,
                    '[red]Filename is not in snake_case: InvalidName.py[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'short.py', 'min_len': 6},
                Result(Status.FAILURE, 'Name too short (min_len=6): short.py'),
                marks=[],
            ),  # Too short
            pytest.param(
                {'filename': 'noextension'},
                Result(Status.SUCCESS, ''),
                marks=[],
            ),  # No extension, but valid name
            pytest.param(
                {'filename': 'UPPERCASE.TXT'},
                Result(
                    Status.FAILURE,
                    '[red]Name too short (min_len=3): UPPERCASE.TXT[/]'
                    '\n[red]Filename is not in snake_case: UPPERCASE.TXT[/]',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': 'mixed_Case.py'},
                Result(
                    Status.FAILURE,
                    'Filename is not in snake_case: mixed_Case.py',
                ),
                marks=[],
            ),  # Not snake_case
            pytest.param(
                {'filename': '.hiddenfile'},
                Result(Status.SUCCESS, ''),
                marks=[],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.gitignore'},
                Result(Status.SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.editorconfig'},
                Result(Status.SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.coveragerc'},
                Result(Status.SUCCESS, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '..doublehidden'},
                Result(
                    Status.FAILURE,
                    'Name too short (min_len=3): ..doublehidden[/]\n'
                    '[red]Filename is not in snake_case: ..doublehidden',
                ),
            ),  # Hidden file, no name
            pytest.param(
                {
                    'filename': 'a_b_c_d_e_f_g_h_i_j_k_l_m'
                    '_n_o_p_q_r_s_t_u_v_w_x_y_z.py'
                },
                Result(Status.SUCCESS, ''),
            ),  # Long valid name
            pytest.param(
                {'filename': 'a' * 256 + '.py'}, Result(Status.SUCCESS, '')
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'a' * 257 + '.py'},
                Result(Status.FAILURE, 'Name too long (max_len=256)'),
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'incolume/py/fakepackage/fake_test_module.py'},
                Result(Status.FAILURE, 'asdf'),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'incolume/py/fakepackage/fake_module.py'},
                Result(Status.SUCCESS, ''),
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module.py'},
                Result(Status.FAILURE, 'asd'),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/test_fake_module.py'},
                Result(Status.FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module_test.py'},
                Result(Status.SUCCESS, ''),
                marks=[],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'test/fake_module.py'},
                Result(Status.FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'test/test_fake_module.py'},
                Result(Status.FAILURE, ''),
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
        ],
    )
    def test_check_if_valid_filenames(
        self, entrance: Mapping[str, str], expected: Result
    ) -> None:
        """Test invalid filenames."""
        fout = (
            self.test_dir
            / stack()[0][3]
            / entrance.get('filename', 'missing-file.txt')
        )
        fout.parent.mkdir(parents=True, exist_ok=True)
        vf = ValidateFilename(filename=fout)
        result = vf.is_valid()
        ic(result)
        assert Status(result.code) is Status(expected.code)  # Not snake_case
        assert expected.message in result.message

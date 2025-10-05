"""Module to validate filenames."""

from __future__ import annotations
from typing import NoReturn

from icecream import ic
import pytest
from incolume.py.githooks.rules import FAILURE, SUCCESS
from incolume.py.githooks.utils import Result
from incolume.py.githooks.valid_filename import ValidateFilename


class TestCaseValidFilename:
    """Test cases for the `is_valid_filename` function."""

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
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
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
        result = ValidateFilename.is_valid_filename(**entrance)
        ic(result)
        assert result.code is expected.code  # Not snake_case
        assert expected.message in result.message

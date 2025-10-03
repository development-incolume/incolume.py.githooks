"""Module to validate filenames."""

from __future__ import annotations
from typing import NoReturn

from icecream import ic
import pytest
from incolume.py.githooks.rules import FAILURE, SUCCESS
from incolume.py.githooks.valid_filename import is_valid_filename


class TestCaseValidFilename:
    """Test cases for the `is_valid_filename` function."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'filename': '__main__.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': '__init__.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': '_validname01.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': 'validname01.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': 'valid_name01.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': 'validname_01.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': 'valid_name_01.py'},
                SUCCESS,
            ),
            pytest.param(
                {'filename': 'validname.py'}, SUCCESS, id='validname.py'
            ),
            pytest.param(
                {'filename': 'valid_name.py'}, SUCCESS, id='valid_name.py'
            ),
            pytest.param(
                {'filename': 'another_valid_name.txt'},
                SUCCESS,
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'a_bc.py', 'min_len': 3},
                SUCCESS,
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'snake_case_file.md'},
                SUCCESS,
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': '0_invalid_name.py'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '0_Invalid_Name.py'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '0InvalidName.py'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'InvalidName.py'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'short.py', 'min_len': 6}, FAILURE, marks=[]
            ),  # Too short
            pytest.param(
                {'filename': 'noextension'}, SUCCESS, marks=[]
            ),  # No extension, but valid name
            pytest.param(
                {'filename': 'UPPERCASE.TXT'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'mixed_Case.py'}, FAILURE, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '.hiddenfile'},
                SUCCESS,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.gitignore'},
                SUCCESS,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.editorconfig'},
                SUCCESS,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '.coveragerc'},
                SUCCESS,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Hidden file, no name
            pytest.param(
                {'filename': '..doublehidden'}, False
            ),  # Hidden file, no name
            pytest.param(
                {
                    'filename': 'a_b_c_d_e_f_g_h_i_j_k_l_m'
                    '_n_o_p_q_r_s_t_u_v_w_x_y_z.py'
                },
                True,
            ),  # Long valid name
            pytest.param(
                {'filename': 'a' * 256 + '.py'}, True
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'a' * 257 + '.py'}, False
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'a' * 1001 + '.py'}, False
            ),  # Very long name, but valid
            pytest.param(
                {'filename': 'incolume/py/fakepackage/fake_module.py'}, True
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module.py'},
                False,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/test_fake_module.py'},
                False,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
            pytest.param(
                {'filename': 'tests/fake_module_test.py'},
                True,
                marks=[
                    pytest.mark.xfail(
                        raises=AssertionError, reason='Not implemented yet'
                    )
                ],
            ),  # Path, but valid name
        ],
    )
    def test_check_if_valid_filenames(
        self, entrance, expected, capsys
    ) -> NoReturn:
        """Test invalid filenames."""
        result = capsys.readouterr()
        ic(result)
        assert is_valid_filename(**entrance).code is expected  # Not snake_case

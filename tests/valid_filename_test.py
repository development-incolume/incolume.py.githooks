"""Module to validate filenames."""

from __future__ import annotations
from typing import NoReturn

from icecream import ic
import pytest
from incolume.py.githooks.valid_filename import is_valid_filename, main


class TestCaseValidFilename:
    """Test cases for the `is_valid_filename` function."""

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'filename': '__main__.py'},
                True,
            ),
            pytest.param(
                {'filename': '__init__.py'},
                True,
            ),
            pytest.param(
                {'filename': '_validname01.py'},
                True,
            ),
            pytest.param(
                {'filename': 'validname01.py'},
                True,
            ),
            pytest.param(
                {'filename': 'valid_name01.py'},
                True,
            ),
            pytest.param(
                {'filename': 'validname_01.py'},
                True,
            ),
            pytest.param(
                {'filename': 'valid_name_01.py'},
                True,
            ),
            pytest.param(
                {'filename': 'validname.py'}, True, id='validname.py'
            ),
            pytest.param(
                {'filename': 'valid_name.py'}, True, id='valid_name.py'
            ),
            pytest.param(
                {'filename': 'another_valid_name.txt'},
                True,
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'a_bc.py', 'min_len': 3},
                True,
                id='another_valid_name.txt',
            ),
            pytest.param(
                {'filename': 'snake_case_file.md'},
                True,
                id='another_valid_name.txt',
            ),
        ],
    )
    def test_valid_filenames(self, entrance, expected) -> NoReturn:
        """Test valid filenames."""
        assert is_valid_filename(**entrance) is expected

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'filename': '0_invalid_name.py'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '0_Invalid_Name.py'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '0InvalidName.py'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'InvalidName.py'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'short.py', 'min_len': 6}, False, marks=[]
            ),  # Too short
            pytest.param(
                {'filename': 'noextension'}, True, marks=[]
            ),  # No extension, but valid name
            pytest.param(
                {'filename': 'UPPERCASE.TXT'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': 'mixed_Case.py'}, False, marks=[]
            ),  # Not snake_case
            pytest.param(
                {'filename': '.hiddenfile'}, True, marks=[pytest.mark.skip]
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
        ],
    )
    def test_invalid_filenames(self, entrance, expected, capsys) -> None:
        """Test invalid filenames."""
        result = capsys.readouterr()
        ic(result)
        assert is_valid_filename(**entrance) is expected  # Not snake_case

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {'Jürgen'}, 'Filename is not in snake_case:', marks=[]
            ),
            pytest.param({'x' * 257}, 'Name too long', marks=[]),
            pytest.param({'x.py'}, 'Name too short', marks=[]),
            pytest.param(
                {'xVar.toml'}, 'Filename is not in snake_case', marks=[]
            ),
            pytest.param({'x.py', '--min-len=5'}, 'Name too short', marks=[]),
            pytest.param(
                {'abc_defg.py', '--min-len=10'},
                'Name too short',
                marks=[],
            ),
        ],
    )
    def test_main(self, capsys, entrance, expected) -> None:
        """Test CLI."""
        main([*entrance])
        captured = capsys.readouterr()
        assert expected in captured.out

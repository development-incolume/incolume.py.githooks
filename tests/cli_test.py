"""Test module for CLI."""

import pytest
from incolume.py.githooks.cli import check_valid_filenames_cli


class TestCaseAllCLI:
    """Test cases for all CLI into the package."""

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
            pytest.param(
                {'abcdefghijklm.py', '--max-len=10'},
                'Name too long',
                marks=[],
            ),
        ],
    )
    def test_check_valid_filenames_cli(
        self, capsys, entrance, expected
    ) -> None:
        """Test CLI."""
        check_valid_filenames_cli([*entrance])
        captured = capsys.readouterr()
        assert expected in captured.out

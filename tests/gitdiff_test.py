"""Test Module for gitdiff."""

import incolume.py.githooks.gitdiff as pkg
import pytest
import tempfile
from pathlib import Path


class TestCaseGitDiff:
    """Test Case for gitdiff."""

    @pytest.mark.parametrize(
        'entrance',
        [pytest.param('A\tincolume/py/githooks/module_xpto.py', marks=[])],
    )
    def test_get_diff(self, entrance, mocker) -> None:
        """Test get_diff_files function."""
        mocker.patch('subprocess.check_output', return_value=entrance)
        assert pkg.get_git_diff() == entrance

    @pytest.mark.parametrize(
        ['commit_msg_file', 'diff_output', 'expected'],
        [
            pytest.param('', '', '', marks=[]),
            pytest.param(
                '',
                'A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                '',
                marks=[],
            ),
            pytest.param(
                'feat: bla bla bla\n\n#',
                'A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                'feat: bla bla bla\n\n\nA\tincolume/py/fake/nothing.py'
                '\nM\tincolume/py/none.py\n#',
                marks=[],
            ),
        ],
    )
    def test_insert_git_diff(
        self, commit_msg_file, diff_output, expected
    ) -> None:
        """Test insert_git_diff function."""
        with tempfile.NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text(commit_msg_file, encoding='utf-8')
        pkg.insert_git_diff(test_file, diff_output)
        assert test_file.read_text(encoding='utf-8') == expected

    def test_main(self) -> None:
        """Test CLI function."""
        pytest.skip('Not implemented yet')

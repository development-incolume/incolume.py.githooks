"""Test Module for gitdiff."""

from incolume.py.githooks.rules import SUCCESS
import incolume.py.githooks.gitdiff as pkg
import pytest
import tempfile
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Expected:
    """Expected values."""

    code: int = pkg.SUCCESS
    msg: str = ''


@dataclass
class MainEntrance:
    """Entrance values."""

    commit_msg_file: str = ''
    commit_source: str = ''
    commit_hash: str = ''
    diff_output: str = ''


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

    @pytest.mark.parametrize(
        [
            'entrance',
            'expected',
        ],
        [
            pytest.param(MainEntrance(), Expected(SUCCESS, ''), marks=[]),
            pytest.param(
                MainEntrance(
                    commit_msg_file='feat: bla bla bla\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                ),
                Expected(
                    msg='feat: bla bla bla\n\n\nA\tincolume/py/fake/'
                    'nothing.py\nM\tincolume/py/none.py\n#',
                ),
                marks=[],
            ),
            pytest.param(
                MainEntrance(commit_msg_file='ci: #123 added ci/cd\n\n#'),
                Expected(SUCCESS, 'ci: #123 added ci/cd\n\n#'),
                marks=[],
            ),
            pytest.param(
                MainEntrance(
                    commit_source='template',
                    commit_msg_file='ci: #123 added ci/cd\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                ),
                Expected(
                    code=SUCCESS,
                    msg='ci: #123 added ci/cd\n\n\nA\tincolume/py/fake/'
                    'nothing.py'
                    '\nM\tincolume/py/none.py\n#',
                ),
                marks=[],
            ),
        ],
    )
    def test_main(
        self,
        mocker,
        entrance: MainEntrance,
        expected: Expected,
    ) -> None:
        """Test CLI function."""
        mocker.patch(
            'subprocess.check_output',
            return_value=entrance.diff_output,
        )
        with tempfile.NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text(entrance.commit_msg_file, encoding='utf-8')
        entrance = [
            test_file.as_posix(),
            entrance.commit_source,
            entrance.commit_hash,
        ]

        assert pkg.main(entrance) == expected.code
        assert test_file.read_text(encoding='utf-8') == expected.msg

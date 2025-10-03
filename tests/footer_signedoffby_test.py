"""Module test footer_signedoffby hook."""

from __future__ import annotations
from typing import NoReturn
import incolume.py.githooks.footer_signedoffby as pkg
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch


class TestCaseFooterSignedOffBy:
    """Test class for footer_signedoffby module."""

    def test_clean_commit_msg(self) -> NoReturn:
        """Test clean_commit_msg function."""
        with tempfile.NamedTemporaryFile('bw+') as tf:
            test_file = Path(tf.name)

        content = (
            'Please enter the commit message for your changes.'
            ' Lines starting\n'
            "# with '#' will be ignored, and an"
            ' empty message aborts the commit.\n'
            '#\n'
            '# On branch main\n'
            '#\n'
            '# Changes to be committed:\n'
            '#	modified:   file1.txt\n'
            '#	modified:   file2.txt\n'
            '#\n'
            '# Untracked files:\n'
            '#	file3.txt\n'
            '#\n'
        )
        test_file.write_text(content, encoding='utf-8')
        assert pkg.clean_commit_msg(test_file)

    def test_get_signed_off_by(self) -> NoReturn:
        """Test get_signed_off_by function."""
        with patch.object(
            pkg.subprocess,
            'check_output',
            return_value='John Doe <john_doe@example.com>',
        ) as m:
            assert (
                pkg.get_signed_off_by()
                == 'Signed-off-by: John Doe <john_doe@example.com>'
            )
            m.assert_called_once_with(
                ['git', 'var', 'GIT_COMMITTER_IDENT'],
                text=True,
            )

    def test_add_signed_off_by(self) -> NoReturn:
        """Test add_signed_off_by function."""
        with tempfile.NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text('Initial commit message\n', encoding='utf-8')
        pkg.add_signed_off_by(
            path=test_file,
            sob='Signed-off-by: John Doe <john_doe@example.com>',
        )
        assert 'Signed-off-by:' in test_file.read_text(encoding='utf-8')
        assert 'John Doe' in test_file.read_text(encoding='utf-8')
        assert 'john_doe@example.com' in test_file.read_text(encoding='utf-8')

    @pytest.mark.parametrize(
        ['entrance', 'commit_source', 'expected'],
        [
            pytest.param('', '', '', marks=[]),
            pytest.param(
                'Initial commit message',
                '',
                '\nInitial commit message',
                marks=[],
            ),
            pytest.param('', 'feat: add new feature', '', marks=[]),
            pytest.param('blue', '', '\nblue', marks=[]),
        ],
    )
    def test_add_blank_line_if_needed(
        self, entrance, commit_source, expected
    ) -> NoReturn:
        """Test add_blank_line_if_needed function."""
        with tempfile.NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text(entrance, encoding='utf-8')
        pkg.add_blank_line_if_needed(test_file, commit_source)
        assert test_file.read_text(encoding='utf-8') == expected

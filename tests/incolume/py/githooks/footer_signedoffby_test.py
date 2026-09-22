"""Module test footer_signedoffby hook."""

from __future__ import annotations
import incolume.py.githooks.footer_signedoffby as pkg
import pytest
import tempfile
import inspect
from pathlib import Path
from unittest.mock import patch
import shutil


class TestCaseFooterSignedOffBy:
    """Test class for footer_signedoffby module."""

    test_dir: Path = Path(tempfile.gettempdir(), inspect.stack()[0][3])

    @classmethod
    def setup_class(cls) -> None:
        """Set class."""
        cls.test_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class.

        Teardown da classe. Remove todos os arquivos
         e diretórios gerados ao final.
        """
        shutil.rmtree(cls.test_dir)

    def test_clean_commit_msg(self) -> None:
        """Test clean_commit_msg function."""
        with tempfile.NamedTemporaryFile(
            mode='bw+', dir=self.test_dir, suffix='.txt'
        ) as tf:
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

    def test_get_signed_off_by(self) -> None:
        """Test get_signed_off_by function."""
        expected: str = 'John Doe <john_doe@example.com>'
        with patch.object(
            pkg.subprocess,
            'check_output',
            return_value=expected,
        ) as m:
            assert pkg.get_signed_off_by() == f'Signed-off-by: {expected}'
            m.assert_called_once_with(
                ['git', 'var', 'GIT_COMMITTER_IDENT'],
                text=True,
            )

    def test_add_signed_off_by(self) -> None:
        """Test add_signed_off_by function."""
        with tempfile.NamedTemporaryFile(
            dir=self.test_dir, suffix='.txt'
        ) as tf:
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
        self, entrance: str, commit_source: str, expected: str
    ) -> None:
        """Test add_blank_line_if_needed function."""
        with tempfile.NamedTemporaryFile(
            dir=self.test_dir, suffix='.txt'
        ) as tf:
            test_file = Path(tf.name)
        test_file.write_text(entrance, encoding='utf-8')
        pkg.add_blank_line_if_needed(test_file, commit_source)
        assert test_file.read_text(encoding='utf-8') == expected

    def test_bkp_file(self) -> None:
        """Test add_signed_off_by function."""
        with tempfile.NamedTemporaryFile(
            dir=self.test_dir, suffix='.txt'
        ) as tf:
            test_file = Path(tf.name).with_stem('test-file')
        test_file.write_text('Initial commit message\n', encoding='utf-8')

        pkg.clean_commit_msg(path=test_file)
        pkg.clean_commit_msg(path=test_file)
        pkg.clean_commit_msg(path=test_file)

        assert test_file.is_file()
        assert test_file.with_suffix(test_file.suffix + '.bkp').is_file()
        assert test_file.with_suffix(test_file.suffix + '.bkp.1').is_file()
        assert test_file.with_suffix(test_file.suffix + '.bkp.2').is_file()

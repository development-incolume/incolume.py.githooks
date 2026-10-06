"""Test module."""

import pytest
import incolume.py.githooks.core.utils as pkg
from tempfile import gettempdir
from pathlib import Path
import inspect
import re
from icecream import ic
import shutil
import tempfile
from dataclasses import dataclass


@dataclass
class EntranceBkp:
    """Entrada para teste de backup."""

    regex: str
    prefix: str = ''
    ext_fl: str = '.txt'
    ext_bkp: str = '.bkp'
    content: str = ''
    expected: str = ''


class TestCaseUtils:
    """Case test for utils."""

    test_dir: Path = Path(gettempdir(), inspect.stack()[0][3])

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class.

        Teardown da classe. Remove todos os arquivos
         e diretórios gerados ao final.
        """
        ic(f'finished class {cls.__name__} execution')

        for name in (
            name
            for name, _ in inspect.getmembers(
                cls, predicate=inspect.isfunction
            )
        ):
            dout = cls.test_dir / name
            shutil.rmtree(dout, ignore_errors=True)

    @pytest.mark.parametrize(
        'entrance',
        [
            'pyproject.toml',
            '.git',
            'requirements.txt',
            'setup.cfg',
            '.venv',
        ],
    )
    def test_markers(self, entrance: str) -> None:
        """Markers values."""
        assert entrance in pkg.MARKERS

    def test_find_project_root_1(self) -> None:
        """Test for find_project_root."""
        dbase = self.test_dir / inspect.stack()[0][3]
        dout = dbase / 'incolume' / 'py' / 'fake' / 'project'
        dout.mkdir(exist_ok=True, parents=True)
        dbase.joinpath('pyproject.toml').touch()
        assert pkg.find_project_root(start_dir=dout).is_dir()

    def test_find_project_root_2(self) -> None:
        """Test for find_project_root."""
        dbase = self.test_dir / inspect.stack()[0][3]
        dout = dbase / 'incolume' / 'py' / 'fake' / 'project'
        dout.mkdir(exist_ok=True, parents=True)
        dbase.joinpath('.venv').mkdir(exist_ok=True, parents=True)
        assert pkg.find_project_root(start_dir=dout).is_dir()

    def test_find_project_root_3(self) -> None:
        """Test for find_project_root."""
        dbase = self.test_dir / inspect.stack()[0][3]
        dout = dbase / 'incolume' / 'py' / 'fake' / 'project'
        dout.mkdir(exist_ok=True, parents=True)
        with pytest.raises(
            FileNotFoundError,
            match=re.escape('Project root not found (no markers detected).'),
        ):
            assert pkg.find_project_root(start_dir=dout) == dbase

    def test_find_project_root_4(self) -> None:
        """Test for find_project_root."""
        dbase = self.test_dir / inspect.stack()[0][3]
        dout = dbase / 'incolume' / 'py' / 'fake' / 'project'
        dout.mkdir(exist_ok=True, parents=True)
        dbase.joinpath('setup.cfg').touch()
        assert pkg.find_project_root(start_dir=dout.as_posix()).is_dir()

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                EntranceBkp(prefix='file-', regex=r'\.bkp/file-.*\.bkp'),
                marks=[],
            ),
            pytest.param(
                EntranceBkp(prefix='fl-', regex=r'.bkp/fl-.*.bkp.1'),
                marks=[],
            ),
            pytest.param(
                EntranceBkp(ext_fl='.xpto', regex=r'.bkp/.*\.xpto\.bkp\.2'),
                marks=[],
            ),
            pytest.param(
                EntranceBkp(
                    prefix='testfile-',
                    ext_fl='.md',
                    content='test: teste da função `backup_file`\n',
                    regex=r'.bkp/testfile-.*.bkp.2',
                ),
                marks=[],
            ),
        ],
    )
    def test_backup_file(self, entrance: EntranceBkp) -> None:
        """Test backup_file."""
        dout = self.test_dir / inspect.stack()[0][3]
        dout.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            dir=dout, prefix=entrance.prefix, suffix=entrance.ext_fl
        ) as tf:
            fout = Path(tf.name)

        fout.write_text(entrance.content, encoding='utf-8')
        results = [
            pkg.backup_file(fout),
            pkg.backup_file(fout),
            pkg.backup_file(fout),
        ]

        assert fout.exists()
        assert all(result.is_file() for result in results)
        assert any(
            re.fullmatch(entrance.regex, result.as_posix())
            for result in results
        )

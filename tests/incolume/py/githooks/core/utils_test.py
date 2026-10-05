"""Test module."""

import pytest
import incolume.py.githooks.core.utils as pkg
from tempfile import gettempdir
from pathlib import Path
import inspect
import re
from icecream import ic
import shutil


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
        ['entrance', 'expected'],
        [
            pytest.param('file.txt', 'file.txt.bkp', marks=[]),
            pytest.param('file.txt', 'file.txt.bkp.1', marks=[]),
            pytest.param('file.txt', 'file.txt.bkp.2', marks=[]),
        ],
    )
    def test_backup_file(self, entrance, expected) -> None:
        """Test backup_file."""
        fout = self.test_dir / inspect.stack()[0][3] / entrance
        fout.parent.mkdir(exist_ok=True, parents=True)
        fout.touch()
        result = pkg.backup_file(fout)

        assert fout.exists()
        assert result.is_file()
        assert result.name == expected

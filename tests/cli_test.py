"""Test module for CLI."""

from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile, gettempdir
from typing import Callable, NoReturn
import pytest
from incolume.py.githooks import cli
from icecream import ic

from incolume.py.githooks.detect_private_key import BLACKLIST
from inspect import stack


class TestCaseAllCLI:
    """Test cases for all CLI into the package."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    def setup_method(self, method: Callable) -> None:
        """Set method.

        Cria a estrutura em arvore de diretórios necessários para os testes.
        """
        ic(f'setup for {method.__name__}')
        self.test_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown class.

        Remove a arvore de diretórios criadas após os testes realizados.
        """
        ic(f'teardown for {cls.__name__}')
        shutil.rmtree(cls.test_dir)

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
        cli.check_valid_filenames_cli([*entrance])
        captured = capsys.readouterr()
        assert expected in captured.out

    @pytest.mark.parametrize(
        'entrance', [pytest.param(line, marks=[]) for line in BLACKLIST]
    )
    def test_main(self, capsys, entrance) -> NoReturn:
        """Test CLI."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)

        ic(test_file, type(test_file))
        test_file.write_bytes(f'----- {entrance} -----\n'.encode())
        cli.detect_private_key_cli([test_file.as_posix()])
        captured = capsys.readouterr()
        assert f'Private key found: {test_file.as_posix()}' in captured.out

    @pytest.mark.parametrize(
        ['args', 'expected'],
        [
            pytest.param(['--help'], '', marks=[pytest.mark.skip]),
            pytest.param(['message fake for commit', '', ''], 0, marks=[]),
            pytest.param(
                ['style: message fake for commit', '', '', '--signoff'],
                0,
                marks=[],
            ),
        ],
    )
    def test_footer_signedoffby_cli(self, args, expected, capsys) -> NoReturn:
        """Test main function."""
        with NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text(args[0], encoding='utf-8')
        args[0] = test_file.as_posix()
        result = cli.footer_signedoffby_cli(args)
        captured = capsys.readouterr()
        assert result == expected
        assert not captured.out

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                '', marks=[pytest.mark.skip(reason='Dont mocked it.')]
            ),
        ],
    )
    def test_precommit_installed(self, mocker, entrance) -> NoReturn:
        """Test for pre-commit installed."""
        ic(entrance)
        ic(__name__)
        with mocker.patch('pathlib.Path.cwd') as m:
            m.return_value = Path(entrance) if entrance else []
            with pytest.raises(SystemExit):
                cli.pre_commit_installed_cli()

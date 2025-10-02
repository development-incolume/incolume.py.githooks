"""Test module for CLI."""

# ruff: noqa: E501

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile, gettempdir
from typing import Callable, NoReturn
import pytest
from incolume.py.githooks import cli
from icecream import ic

from incolume.py.githooks.detect_private_key import BLACKLIST
from inspect import stack

from incolume.py.githooks.prepare_commit_msg import MESSAGERROR
from incolume.py.githooks.rules import FAILURE, MESSAGES, SUCCESS
from incolume.py.githooks.utils import Result


@dataclass
class Entrance:
    """Entrance dataclass for tests."""

    msg_file: str | Path = None
    msg_commit: str = ''
    params: list[str] = field(default_factory=list)
    expected: Result = field(
        default_factory=lambda: Result(FAILURE, MESSAGERROR)
    )


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
        ['entrance', 'exit_code', 'message'],
        [
            pytest.param(
                'WIP',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\nPlease rename your branch with',
                marks=[],
            ),
            pytest.param(
                '123-jesus-loves-you',
                0,
                'xpto',
                marks=[],
            ),
        ],
    )
    def test_check_valid_branchname(
        self, capsys, mocker, entrance, exit_code, message
    ) -> None:
        """Test check_valid_branchname function."""
        ic(entrance, exit_code, message)

        with mocker.patch('incolume.py.githooks.utils') as m:
            m.return_value.get_branchname.return_value = entrance
            result = cli.check_valid_branchname()
            ic(result)
            captured = capsys.readouterr()
            assert message in captured.out
            assert result == exit_code

    @pytest.mark.parametrize(
        ['entrance', 'result_expected', 'expected'],
        [
            pytest.param(
                {'Jürgen'}, 1, 'Filename is not in snake_case:', marks=[]
            ),
            pytest.param({'x' * 257}, 1, 'Name too long', marks=[]),
            pytest.param({'x.py'}, 1, 'Name too short', marks=[]),
            pytest.param(
                {'xVar.toml'}, 1, 'Filename is not in snake_case', marks=[]
            ),
            pytest.param(
                {'x.py', '--min-len=5'}, 1, 'Name too short', marks=[]
            ),
            pytest.param(
                {'abc_defg.py', '--min-len=10'},
                1,
                'Name too short',
                marks=[],
            ),
            pytest.param(
                {'abcdefghijklm.py', '--max-len=10'},
                1,
                'Name too long',
                marks=[],
            ),
            pytest.param({'__main__.py'}, 0, '', marks=[]),
        ],
    )
    def test_check_valid_filenames_cli(
        self, capsys, entrance, result_expected, expected
    ) -> None:
        """Test CLI."""
        result = cli.check_valid_filenames_cli([*entrance])
        captured = capsys.readouterr()
        assert result == result_expected
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

    def test_effort_msg_cli(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Teste CLI."""
        result = cli.effort_msg_cli()
        captured = capsys.readouterr()
        assert result == 0
        assert 'Boa! Continue trabalhando com' in captured.out
        assert '\033[32m' in captured.out  # Fore.GREEN

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_commit='Please enter the commit message\n\n#',
                    expected=Result(SUCCESS, ''),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat: #61 Please enter the commit message',
                    expected=Result(
                        SUCCESS, 'feat: #61 Please enter the commit message'
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit=(
                        'Please enter the commit message\n\n#'
                        '\nconteúdo fake para teste.'
                        '\nA\tfile1.txt'
                        '\nB\tfile2.txt'
                        '\n#\n# On branch main\n'
                    ),
                    expected=Result(
                        SUCCESS,
                        'conteúdo fake para teste.\nA\tfile1.txt\nB\tfile2.txt\n#\n# On branch main\n',
                    ),
                )
            ),
        ],
    )
    def test_clean_commit_msg_cli(self, entrance) -> NoReturn:
        """Test CLI for clean-commit-msg-cli."""
        with NamedTemporaryFile() as fl:
            filename = Path(fl.name)
        filename.write_text(entrance.msg_commit, encoding='utf-8')
        result = cli.clean_commit_msg_cli([filename.as_posix(), '', ''])
        assert result == entrance.expected.code
        assert (
            filename.read_text(encoding='utf-8') == entrance.expected.message
        )

    def test_prepare_commit_msg_cli(self) -> NoReturn:
        """Test CLI prepend commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'xpto: abc')
        with pytest.raises(SystemExit):
            assert cli.prepare_commit_msg_cli([test_file.as_posix()])

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

    def test_get_msg_cli(self, capsys) -> None:
        """Test get_msg function."""
        cli.get_msg_cli()
        captured = capsys.readouterr()
        assert captured.out.strip() in MESSAGES

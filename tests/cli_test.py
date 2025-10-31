"""Test module for CLI."""

# ruff: noqa: E501

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import shutil
from tempfile import NamedTemporaryFile, gettempdir
from typing import NoReturn, TYPE_CHECKING
import pytest
from incolume.py.githooks import cli
from icecream import ic

from incolume.py.githooks.detect_private_key import BLACKLIST
from inspect import stack

from incolume.py.githooks.prepare_commit_msg import MESSAGERROR
from incolume.py.githooks.rules import FAILURE, MESSAGES, SUCCESS, Status
from incolume.py.githooks.utils import Result
from unittest.mock import patch

from . import Expected, MainEntrance


if TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Generator


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
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_commit='docs: #85 Atualizado README.md\nacrescentado os hooks padrões para pre-commit pertinentes ao ecossistema incolume',
                    expected=Result(
                        message=[
                            'Commit minimum length for message is validated',
                            'Commit maximum length for message is validated',
                        ]
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='bugfix(refactor)!: bla bla bla bla bla bla bla',
                    expected=Result(
                        SUCCESS,
                        [
                            'Commit minimum length for message is validated',
                            'Commit maximum length for message is validated',
                        ],
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat' * 15,
                    expected=Result(
                        FAILURE,
                        [
                            'Error: Commit subject line exceeds',
                        ],
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat',
                    expected=Result(
                        FAILURE,
                        [
                            'Error: Commit subject line has an insufficient number of',
                            'Commit maximum length for message is validated',
                        ],
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat',
                    params=['--min-first-line=4', '--max-first-line=5'],
                    expected=Result(
                        SUCCESS,
                        [
                            'Commit minimum length for message is validated',
                            'Commit maximum length for message is validated',
                        ],
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat',
                    params=['--nonexequi'],
                    expected=Result(
                        SUCCESS,
                        [
                            '',
                        ],
                    ),
                ),
                marks=[],
            ),
        ],
    )
    def test_check_len_first_line_commit_msg_cli(
        self, capsys: Generator, entrance: Entrance
    ) -> NoReturn:
        """Test CLI for check len first line commit messages."""
        result = None
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)

        test_file.write_text(f'{entrance.msg_commit}\n', encoding='utf-8')
        result = cli.check_len_first_line_commit_msg_cli([
            test_file.as_posix(),
            '',
            '',
            *entrance.params,
        ])
        captured = capsys.readouterr()
        assert result == entrance.expected.code.value
        assert captured.out.split('\n')
        assert sum(
            m in n
            for m in entrance.expected.message
            for n in captured.out.split('\n')
        ) == len(entrance.expected.message)

    def test_check_type_commit_msg_cli(self) -> NoReturn:
        """Test CLI for check type commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'')
        with pytest.raises(SystemExit):
            assert cli.check_type_commit_msg_cli([test_file.as_posix()])

    @pytest.mark.parametrize(
        ['entrance', 'exit_code', 'message'],
        [
            pytest.param(
                'Wip',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\n - Can be not WIP(Work in Progress)\n',
                marks=[],
            ),
            pytest.param(
                'wip',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\n - Can be not WIP(Work in Progress)\n',
                marks=[],
            ),
            pytest.param(
                'WIP',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\n - Can be not WIP(Work in Progress)\n',
                marks=[],
            ),
            pytest.param(
                'template-Wip',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\n - Can be not WIP(Work in Progress)\n',
                marks=[],
            ),
            pytest.param(
                'Wip-test-for-branch',
                1,
                'Your commit was rejected due to branching name incompatible with rules.\n - Can be not WIP(Work in Progress)\n',
                marks=[],
            ),
            pytest.param(
                'jesus-loves-you',
                1,
                "Your commit was rejected due to branching name incompatible with rules.\nPlease rename your branch with:\n- syntaxe 1: 'enhancement-<epoch-timestamp>'\n- syntaxe 2: '<issue-id>-descri\xe7\xe3o-da-issue'\n- syntaxe 3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'\n- syntaxe 4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'\n",
                marks=[],
            ),
            pytest.param(
                '123-jesus-loves-you',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'refactor/epoch#1234567890',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'feat/issue#123',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'enhancement-1234567890',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                '80-açaí-itú-água-é-ação-de-sertões',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'main',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'tags',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'master',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'dev',
                0,
                'Branching name rules. [OK]',
                marks=[],
            ),
        ],
    )
    def test_check_valid_branchname(
        self, capsys, entrance, exit_code, message
    ) -> None:
        """Test check_valid_branchname function."""
        ic(entrance, exit_code, message)

        with patch.object(cli, 'get_branchname', return_value=entrance):
            result = cli.check_valid_branchname_cli()
            ic(result)
            captured = capsys.readouterr()
            assert message in captured.out
            assert Status(result) == Status(exit_code)

    @pytest.mark.parametrize(
        ['entrance', 'result_expected', 'expected'],
        [
            pytest.param(
                {'Jürgen'}, FAILURE, 'Filename is not in snake_case:', marks=[]
            ),
            pytest.param({'x' * 257}, FAILURE, 'Name too long', marks=[]),
            pytest.param({'x.py'}, 1, 'Name too short', marks=[]),
            pytest.param(
                {'xVar.toml'},
                FAILURE,
                'Filename is not in snake_case',
                marks=[],
            ),
            pytest.param(
                {'x.py', '--min-len=5'}, FAILURE, 'Name too short', marks=[]
            ),
            pytest.param(
                {'abc_defg.py', '--min-len=10'},
                FAILURE,
                'Name too short',
                marks=[],
            ),
            pytest.param(
                {'abcdefghijklm.py', '--max-len=10'},
                FAILURE,
                'Name too long',
                marks=[],
            ),
            pytest.param({'__main__.py'}, SUCCESS, '', marks=[]),
        ],
    )
    def test_check_valid_filenames_cli(
        self, capsys, entrance, result_expected, expected
    ) -> None:
        """Test CLI."""
        result = cli.check_valid_filenames_cli([*entrance])
        captured = capsys.readouterr()
        assert Status(result) == Status(result_expected)
        assert expected in captured.out

    @pytest.mark.parametrize(
        'entrance', [pytest.param(line, marks=[]) for line in BLACKLIST]
    )
    def test_detect_private_key_cli(self, capsys, entrance) -> NoReturn:
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
                ['style: message fake for commit', '', '', '--nonexequi'],
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
        assert Status(result) == Status(expected)
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
            assert cli.validate_format_commit_msg_cli([test_file.as_posix()])

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                '.pre-commit-config.yaml',
                SUCCESS,
                marks=[],
            ),
            pytest.param(
                '',
                FAILURE,
                marks=[],
            ),
        ],
    )
    def test_precommit_installed(self, entrance, expected) -> NoReturn:
        """Test for pre-commit installed."""
        result = FAILURE
        with patch.object(Path, 'cwd') as m:
            m.return_value.glob.return_value = (
                [Path(entrance)] if entrance else []
            )
            result = cli.pre_commit_installed_cli()
        assert Status(result) == Status(expected)

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param([], marks=[]),
            pytest.param(['--fixed'], marks=[]),
            pytest.param(['--nonexequi'], marks=[]),
        ],
    )
    def test_get_msg_cli(self, capsys, entrance) -> None:
        """Test get_msg function."""
        cli.get_msg_cli(entrance)
        captured = capsys.readouterr()
        assert captured.out.strip() in {'', *MESSAGES}

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
                    message='feat: bla bla bla\n\n\nA\tincolume/py/fake/'
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
                    message='ci: #123 added ci/cd\n\n\nA\tincolume/py/fake/'
                    'nothing.py'
                    '\nM\tincolume/py/none.py\n#',
                ),
                marks=[],
            ),
            pytest.param(
                MainEntrance(args=['--nonexequi']),
                Expected(SUCCESS, ''),
                marks=[
                    # pytest.mark.skip
                ],
            ),
            pytest.param(
                MainEntrance(
                    commit_msg_file='ci: #123 added ci/cd\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                    args=['--nonexequi'],
                ),
                Expected(code=SUCCESS, message='ci: #123 added ci/cd\n\n#'),
                marks=[],
            ),
        ],
    )
    def test_insert_diff_cli(
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
        with NamedTemporaryFile() as tf:
            test_file = Path(tf.name)
        test_file.write_text(entrance.commit_msg_file, encoding='utf-8')
        entries = [
            test_file.as_posix(),
            entrance.commit_source,
            entrance.commit_hash,
            *entrance.args,
        ]

        assert cli.insert_diff_cli(entries) == expected.code.value
        assert test_file.read_text(encoding='utf-8') == expected.message

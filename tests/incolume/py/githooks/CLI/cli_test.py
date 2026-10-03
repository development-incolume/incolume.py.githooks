"""Test module for CLI."""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
from tempfile import NamedTemporaryFile, gettempdir
from typing import TYPE_CHECKING, Any
from incolume.py.githooks.core import remove_color_tags
import pytest
from incolume.py.githooks import cli
from icecream import ic
from incolume.py.githooks.detect_private_key import BLACKLIST
from inspect import stack
from incolume.py.githooks.prepare_commit_msg import MESSAGERROR
from incolume.py.githooks.core.rules import (
    MESSAGES,
    Status,
    Result,
)
from unittest.mock import patch
from itertools import chain

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pytest_mock import MockerFixture
    from collections.abc import Callable


@dataclass
class Entrance:
    """Entrance dataclass for tests."""

    msg_file: str | Path = ''
    msg_commit: str = ''
    params: list[str] = field(default_factory=list)
    diff_output: str = ''
    commit_source: str = ''
    commit_hash: str = ''
    expected: Result = field(
        default_factory=lambda: Result(Status.FAILURE, MESSAGERROR)
    )


class TestCaseAllCLI:
    """Test cases for all CLI into the package."""

    test_dir = Path(gettempdir()) / stack()[0][3]

    def setup_method(self, method: Callable) -> None:  # type: ignore[type-arg]
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
                            'Commit minimum length for message is validated [OK]',
                            'Commit maximum length for message is validated [OK]',
                        ]
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='bugfix(refactor)!: bla bla bla bla bla bla bla',
                    expected=Result(
                        Status.SUCCESS,
                        [
                            'Commit minimum length for message is validated [OK]',
                            'Commit maximum length for message is validated [OK]',
                        ],
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat' * 15,
                    expected=Result(
                        Status.FAILURE,
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
                        Status.FAILURE,
                        [
                            'Error: Commit subject line has an insufficient number of 10 characters allowed (4 of 10).',
                            'Error: The first line of the commit violates the defined minimum limits. (min: 10 and max: 50)',
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
                        Status.FAILURE,
                        [
                            'Error: Commit subject line has an insufficient number of 10 characters allowed (4 of 10).',
                            'Error: The first line of the commit violates the defined minimum limits. (min: 10 and max: 50)',
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
                        Status.SUCCESS,
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
        self,
        isolated_cli_runner: CliRunner,
        entrance: Entrance,
    ) -> None:
        """Test CLI for check len first line commit messages."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)

        test_file.write_text(f'{entrance.msg_commit}\n', encoding='utf-8')
        ic(test_file)

        result = isolated_cli_runner.invoke(
            cli.check_len_first_line_commit_msg_cli,
            [
                test_file.as_posix(),
                *entrance.params,
            ],
        )

        assert result.exit_code == entrance.expected.code.value
        assert all(msg in result.output for msg in entrance.expected.message)

    @pytest.mark.parametrize(
        'args',
        [
            pytest.param([]),
            pytest.param(['--nonexequi'], marks=[]),
        ],
    )
    def test_check_type_commit_msg_cli(self, args: list[str]) -> None:
        """Test CLI for check type commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'')
        with pytest.raises(SystemExit):
            assert cli.check_type_commit_msg_cli([
                test_file.as_posix(),
                *args,
            ])

    @pytest.mark.parametrize(
        ['entrance', 'exit_code', 'params', 'message'],
        [
            pytest.param(
                '',
                0,
                ['-N'],
                '',
                marks=[],
            ),
            pytest.param(
                'xpto-wip',
                0,
                ['', '--nonexequi'],
                '',
                marks=[],
            ),
            pytest.param(
                'xpto-wip',
                0,
                ['-N'],
                '',
                marks=[],
            ),
            pytest.param(
                '123-jesus-loves-you',
                0,
                [''],
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'refactor/epoch#1234567890',
                0,
                [''],
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'feat/issue#123',
                0,
                [''],
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'enhancement-1234567890',
                0,
                [''],
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                '80-açaí-itú-água-é-ação-de-sertões',
                0,
                [''],
                'Branching name rules. [OK]',
                marks=[],
            ),
            pytest.param(
                'master',
                1,
                [],
                """Your commit was rejected due to branching name incompatible with rules.
 - Branch name "master" is protected.

:: These syntaxes are allowed for branchname:
 - #1: 'enhancement-<epoch-timestamp>'; or
 - #2: '<issue-id>-issue-description'; or
 - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or
 - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'""",
                marks=[],
            ),
            pytest.param(
                'main',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Branch name \"main\" is protected.\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'Wip',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Can not be WIP (Work in Progress)\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'wip',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Can not be WIP (Work in Progress)\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'WIP',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Can not be WIP (Work in Progress)\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'template-Wip',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Can not be WIP (Work in Progress)\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'Wip-test-for-branch',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n - Can not be WIP (Work in Progress)\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'todo-test-for-branch',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'jesus-loves-you',
                1,
                [''],
                "Your commit was rejected due to branching name incompatible with rules.\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'tags',
                1,
                ['--tags'],
                "Your commit was rejected due to branching name incompatible with rules.\n - Branch name \"tags\" is protected.\n\n:: These syntaxes are allowed for branchname:\n - #1: 'enhancement-<epoch-timestamp>'; or\n - #2: '<issue-id>-issue-description'; or\n - #3: '<(feature|feat|bug|bugfix|fix)>/issue#<issue-id>'; or\n - #4: '<(feature|feat|bug|bugfix|fix)>/epoch#<epoch-timestamp>'",
                marks=[],
            ),
            pytest.param(
                'dev',
                1,
                ['--dev'],
                ' Branch name "dev" is protected.',
                marks=[],
            ),
            pytest.param(
                'dev', 0, ['--no-dev'], '', marks=[pytest.mark.xfail]
            ),
            pytest.param(
                'tags', 0, ['--no-tags'], '', marks=[pytest.mark.xfail]
            ),
            pytest.param(
                'main',
                0,
                ['', '--no-main'],
                '',
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                'master',
                0,
                ['', '--no-main'],
                '',
                marks=[pytest.mark.xfail],
            ),
        ],
    )
    def test_check_valid_branchname(
        self,
        cli_runner: CliRunner,
        entrance: str,
        exit_code: int,
        params: list[str],
        message: str,
    ) -> None:
        """Test check_valid_branchname function."""
        ic(f'{entrance=}, {exit_code=}, {message=}')

        with patch.object(
            subprocess, 'check_output', return_value=bytes(entrance, 'utf-8')
        ):
            result = cli_runner.invoke(cli.check_valid_branchname_cli, params)
            assert result.exit_code == exit_code
            assert message in result.output

    @pytest.mark.parametrize(
        ['entrance', 'result_expected', 'expected'],
        [
            pytest.param(
                ['4File.py'],
                Status.FAILURE,
                'Filename is not in snake_case:',
            ),
            pytest.param(
                ['Jürgen.py'],
                Status.FAILURE,
                'Filename is not in snake_case:',
                marks=[],
            ),
            pytest.param(
                ['Jürgen'],
                Status.FAILURE,
                'Filename structure is invalid.',
                marks=[],
            ),
            pytest.param(
                ['x' * 257 + '.py'],
                Status.FAILURE,
                'Filename too long',
                marks=[],
            ),
            pytest.param(
                ['x.py'], Status.FAILURE, 'Filename too short', marks=[]
            ),
            pytest.param(
                ['x.py', '--nonexequi'], Status.SUCCESS, '', marks=[]
            ),
            pytest.param(
                ['xVar.py'],
                Status.FAILURE,
                'Filename is not in snake_case',
                marks=[],
            ),
            pytest.param(
                ['xVar.toml'],
                Status.SUCCESS,
                '',
                marks=[],
            ),
            pytest.param(
                ['x.py', '--min-len=5'],
                Status.FAILURE,
                'Filename too short',
                marks=[],
            ),
            pytest.param(
                ['abc_defg.py', '--min-len=10'],
                Status.FAILURE,
                'Filename too short',
                marks=[],
            ),
            pytest.param(
                ['abcdefghijklm.py', '--max-len=10'],
                Status.FAILURE,
                'Filename too long',
                marks=[],
            ),
            pytest.param(['__main__.py'], Status.SUCCESS, '', marks=[]),
        ],
    )
    def test_check_valid_filenames_cli(
        self,
        cli_runner: CliRunner,
        entrance: list[str],
        result_expected: Status,
        expected: str,
    ) -> None:
        """Test CLI."""
        result = cli_runner.invoke(cli.check_valid_filenames_cli, entrance)
        assert result.exit_code == result_expected.value
        assert expected in result.output

    @pytest.mark.parametrize(
        ['entrance', 'args', 'msg_output'],
        chain.from_iterable(
            [
                (
                    pytest.param(
                        line,
                        ['--nonexequi'],
                        'Hook not executed due to the `--nonexequi` option.\n',
                        marks=[],
                    )
                    for line in BLACKLIST
                ),
                (
                    pytest.param(
                        line,
                        ['-N'],
                        'Hook not executed due to the `--nonexequi` option.\n',
                        marks=[],
                    )
                    for line in BLACKLIST
                ),
                (
                    pytest.param(line, [], 'Private key found: {}', marks=[])
                    for line in BLACKLIST
                ),
            ],
        ),
    )
    def test_detect_private_key_cli(
        self,
        cli_runner: CliRunner,
        entrance: str,
        args: list[str],
        msg_output: str,
    ) -> None:
        """Test CLI."""
        dout = self.test_dir / stack()[0][3]
        dout.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=dout) as fl:
            test_file = Path(fl.name)

        ic(test_file, type(test_file))
        test_file.write_bytes(f'----- {entrance} -----\n'.encode())
        result = cli_runner.invoke(
            cli.detect_private_key_cli, [test_file.as_posix(), *args]
        )
        if args:
            assert msg_output in result.output
        else:
            assert msg_output.format(test_file.as_posix()) in result.output

    @pytest.mark.parametrize(
        ['args', 'content', 'expected'],
        [
            pytest.param([], 'message fake for commit', 0, marks=[]),
            pytest.param(
                ['--nonexequi'],
                'style: message fake for commit',
                0,
                marks=[],
            ),
            pytest.param(['--help'], '', 0, marks=[]),
            pytest.param(['--nonexequi'], '', 0, marks=[]),
            pytest.param(['-h'], '', 0, marks=[]),
            pytest.param(['-N'], '', 0, marks=[]),
        ],
    )
    def test_footer_signedoffby_cli(
        self,
        content: str,
        args: list[str],
        expected: int,
        capsys: pytest.CaptureFixture[Any],
        cli_runner: CliRunner,
    ) -> None:
        """Test main function."""
        with NamedTemporaryFile(dir=self.test_dir) as tf:
            test_file = Path(tf.name)
            test_file = Path(test_file.parent, stack()[0][3], test_file.name)
        test_file.parent.mkdir(parents=True, exist_ok=True)
        if content:
            test_file.write_text(content, encoding='utf-8')

        result = cli_runner.invoke(
            cli.footer_signedoffby_cli, (test_file.as_posix(), *args)
        )
        captured = capsys.readouterr()
        assert result.exit_code == expected
        assert not captured.out

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                {},
                'Boa! Continue trabalhando com',
                marks=[
                    pytest.mark.xfail(
                        reason='Identify color in output not improved'
                    )
                ],
            ),
            pytest.param({'--nonexequi'}, '', marks=[]),
        ],
    )
    def test_effort_msg_cli(
        self,
        cli_runner: CliRunner,
        capsys: pytest.CaptureFixture[str],
        entrance: str,
        expected: str,
    ) -> None:
        """Teste CLI."""
        result = cli_runner.invoke(cli.effort_msg_cli, entrance)
        captured = capsys.readouterr()
        assert result.exit_code == 0
        assert expected in captured.out
        if not entrance:
            assert '\033[32m' in captured.out  # Fore.GREEN

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_commit='Please enter the commit message\n\n#',
                    expected=Result(Status.SUCCESS, ''),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat: #61 Please enter the commit message',
                    expected=Result(
                        Status.SUCCESS,
                        'feat: #61 Please enter the commit message',
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
                        Status.SUCCESS,
                        'conteúdo fake para teste.\nA\tfile1.txt\nB\tfile2.txt\n#\n# On branch main\n',
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat: #61 Please enter the commit message',
                    expected=Result(
                        Status.SUCCESS,
                        'feat: #61 Please enter the commit message',
                    ),
                    params=['--nonexequi'],
                ),
            ),
            pytest.param(
                Entrance(
                    msg_commit='',
                    expected=Result(Status.SUCCESS, ''),
                    params=['-h'],
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='',
                    expected=Result(Status.SUCCESS, ''),
                    params=['-N'],
                )
            ),
        ],
    )
    def test_clean_commit_msg_cli(
        self, cli_runner: CliRunner, entrance: Entrance
    ) -> None:
        """Test CLI for clean-commit-msg-cli."""
        with NamedTemporaryFile(dir=self.test_dir) as tf:
            test_file = Path(tf.name)
            test_file = Path(test_file.parent, stack()[0][3], test_file.name)
        test_file.parent.mkdir(parents=True, exist_ok=True)

        test_file.write_text(entrance.msg_commit, encoding='utf-8')
        result = cli_runner.invoke(
            cli.clean_commit_msg_cli,
            [
                test_file.as_posix(),
                *entrance.params,
            ],
        )
        assert result.exit_code == entrance.expected.code.value
        assert (
            test_file.read_text(encoding='utf-8') == entrance.expected.message
        )

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    params=['-V'],
                    expected=Result(0, 'is-valid-msg-commit, version'),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['-h'],
                    expected=Result(
                        0,
                        'Usage: is-valid-msg-commit [OPTIONS] [COMMIT_MSG_FILE]...',
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['--nonexequi'],
                    expected=Result(
                        0, 'Hook not executed due to the `--nonexequi` option.'
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['-N'],
                    expected=Result(
                        0, 'Hook not executed due to the `--nonexequi` option.'
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=[], msg_commit='', expected=Result(1, message='')
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=[],
                    msg_commit='fake commit',
                    expected=Result(
                        code=1, message='Please use the following format'
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                Entrance(
                    params=[],
                    msg_commit='feat: #123 fake commit',
                    expected=Result(
                        code=0, message='Commit message is validated'
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
        ],
    )
    def test_validate_format_commit_msg_cli(
        self, cli_runner: CliRunner, entrance: Entrance
    ) -> None:
        """Test CLI prepend commit message."""
        dout: Path = self.test_dir.joinpath(stack()[0][3])
        dout.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(dir=dout) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(entrance.msg_commit.encode(encoding='utf-8'))

        entry: list[str] = [test_file.as_posix(), *entrance.params]

        result = cli_runner.invoke(cli.validate_format_commit_msg_cli, entry)
        assert result.exit_code == entrance.expected.code
        assert entrance.expected.message in result.output

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    params=['-N'],
                    expected=Result(
                        Status.SUCCESS,
                        'Hook not executed due to the `--nonexequi` option.',
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['--nonexequi'],
                    expected=Result(
                        Status.SUCCESS,
                        'Hook not executed due to the `--nonexequi` option.',
                    ),
                ),
                marks=[],
            ),
        ],
    )
    def test_precommit_installed(
        self,
        cli_runner: CliRunner,
        entrance: Entrance,
    ) -> None:
        """Test for pre-commit installed."""
        result = cli_runner.invoke(
            cli.pre_commit_installed_cli, entrance.params
        )
        assert result.exit_code == entrance.expected.code.value
        assert entrance.expected.message in result.output

    def test_precommit_installed1(self, cli_runner: CliRunner) -> None:
        """Test for pre-commit installed."""
        entrance = Entrance(
            msg_file='.pre-commit-config.yaml',
            params=[],
            expected=Result(Status.SUCCESS, ''),
        )
        with (
            patch.object(Path, 'cwd') as m,
            patch.object(os, 'access', return_value=True),
        ):
            m.return_value.glob.return_value = [Path(entrance.msg_file)]
            result = cli_runner.invoke(
                cli.pre_commit_installed_cli, entrance.params
            )
        assert result.exit_code == entrance.expected.code.value
        assert entrance.expected.message in result.output

    def test_precommit_installed2(self, cli_runner: CliRunner) -> None:
        """Test for pre-commit installed."""
        entrance = Entrance(
            msg_file='',
            params=[],
            expected=Result(
                Status.FAILURE,
                'Configuration file ".pre-commit-config.yaml" not detected',
            ),
        )
        with patch.object(Path, 'cwd') as m:
            m.return_value.glob.return_value = (
                [Path(entrance.msg_file)] if entrance else []
            )
            result = cli_runner.invoke(
                cli.pre_commit_installed_cli, entrance.params
            )
        assert result.exit_code == entrance.expected.code.value
        assert entrance.expected.message in result.output

    def test_precommit_installed3(self, cli_runner: CliRunner) -> None:
        """Test for pre-commit installed."""
        entrance = Entrance(
            params=[],
            expected=Result(
                Status.FAILURE,
                '`pre-commit` configuration detected, but `pre-commit install` was never ran.',
            ),
        )
        with patch.object(Path, 'cwd') as m:
            m.return_value.glob.return_value = (
                [Path(entrance.msg_file)] if entrance else []
            )
            result = cli_runner.invoke(
                cli.pre_commit_installed_cli, entrance.params
            )
        assert result.exit_code == entrance.expected.code.value
        assert entrance.expected.message in result.output

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param([], marks=[]),
            pytest.param(['--fixed'], marks=[]),
            pytest.param(['--nonexequi'], marks=[]),
        ],
    )
    def test_effort_random_msg_cli(
        self,
        cli_runner: CliRunner,
        capsys: pytest.CaptureFixture[Any],
        entrance: list[str],
    ) -> None:
        """Test get_msg function."""
        cli_runner.invoke(cli.effort_random_msg_cli, entrance)
        captured = capsys.readouterr()
        assert remove_color_tags(captured.out.strip()) in {'', *MESSAGES}

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    params=['-N'],
                    expected=Result(
                        Status.SUCCESS,
                        'Hook not executed due to the `--nonexequi` option.',
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['--nonexequi'],
                    expected=Result(
                        Status.SUCCESS,
                        'Hook not executed due to the `--nonexequi` option.',
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['-V'],
                    expected=Result(
                        Status.SUCCESS, 'insert-diff-commit, version'
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    params=['--version'],
                    expected=Result(
                        Status.SUCCESS, 'insert-diff-commit, version'
                    ),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    expected=Result(Status.FAILURE, 'abc'),
                ),
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat: bla bla bla\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                    expected=Result(
                        message='feat: bla bla bla\n\n\nA\tincolume/py/fake/'
                        'nothing.py\nM\tincolume/py/none.py\n#',
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                Entrance(
                    msg_commit='ci: #123 added ci/cd\n\n#',
                    expected=Result(
                        Status.SUCCESS, 'ci: #123 added ci/cd\n\n#'
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                Entrance(
                    commit_source='template',
                    msg_commit='ci: #123 added ci/cd\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                    expected=Result(
                        code=Status.SUCCESS,
                        message='ci: #123 added ci/cd\n\n\nA\tincolume/py/fake/'
                        'nothing.py'
                        '\nM\tincolume/py/none.py\n#',
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
            pytest.param(
                Entrance(
                    msg_commit='ci: #123 added ci/cd\n\n#',
                    diff_output='A\tincolume/py/fake/nothing.py\nM\tincolume/py/none.py',
                    params=['--nonexequi'],
                    expected=Result(
                        code=Status.SUCCESS,
                        message='ci: #123 added ci/cd\n\n#',
                    ),
                ),
                marks=[pytest.mark.xfail],
            ),
        ],
    )
    def test_insert_diff_cli(
        self,
        cli_runner: CliRunner,
        mocker: MockerFixture,
        entrance: Entrance,
    ) -> None:
        """Test CLI function."""
        mocker.patch(
            'subprocess.check_output',
            return_value=entrance.diff_output,
        )
        dout: Path = self.test_dir / stack()[0][3]
        dout.mkdir(parents=True, exist_ok=True)

        with NamedTemporaryFile(dir=dout) as tf:
            test_file = Path(tf.name)

        test_file.write_text(entrance.msg_commit, encoding='utf-8')

        entries = [
            test_file.as_posix(),
            entrance.commit_source,
            entrance.commit_hash,
            *entrance.params,
        ]
        ic(entries)
        result = cli_runner.invoke(cli.insert_diff_cli, entries)
        assert test_file.is_file()
        assert result.exit_code == entrance.expected.code.value
        assert entrance.expected.message in result.output
        assert entrance.diff_output in test_file.read_text(encoding='utf-8')

"""Test module for prepare_commit_msg."""

# ruff: noqa: E501
from __future__ import annotations

import shutil
from typing import NoReturn
from icecream import ic
import pytest
from incolume.py.githooks import SUCCESS, FAILURE, Result
from incolume.py.githooks.prepare_commit_msg import (
    MESSAGERROR,
    MESSAGESUCCESS,
    prepare_commit_msg,
    check_max_len_first_line_commit_msg,
    check_type_commit_msg,
    check_max_len_first_line_commit_msg_cli,
    check_type_commit_msg_cli,
    prepare_commit_msg_cli,
    clean_commit_msg_cli,
)
from tempfile import NamedTemporaryFile, gettempdir
from pathlib import Path
from inspect import stack
from dataclasses import dataclass, field


@dataclass
class Entrance:
    """Entrance dataclass for tests."""

    msg_file: str | Path = None
    msg_commit: str = ''
    expected: Result = field(
        default_factory=lambda: Result(FAILURE, MESSAGERROR)
    )


class TestCasePrepareCommitMsg:
    """Test class for prepare commit message."""

    __test__ = True
    test_dir = Path(gettempdir()) / stack()[0][3]

    @classmethod
    def setup_class(cls) -> None:
        """Set method.

        Cria a estrutura em arvore de diretórios necessários para os testes.
        """
        cls.test_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def teardown_class(cls) -> None:
        """Teardown method.

        Remove a arvore de diretórios criadas após os testes realizados.
        """
        shutil.rmtree(cls.test_dir)

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                MESSAGESUCCESS,
                ['Commit message is validated [OK]'],
                marks=[],
            ),
            pytest.param(
                MESSAGERROR,
                [
                    'Your commit was rejected due to the',
                    'invalid commit message',
                    'Please use the following format',
                    '<type>(optional scope): #id-issue <description>',
                    '[red]',
                    'Your commit was rejected due to the [bold underline]invalid commit message[/bold underline]...',
                    'Please use the following format:',
                    '[green]<type>(optional scope): #id-issue <description>[/green]',
                    '[cyan]type values: feature | feat, bugfix | fix, chore, refactor, docs, style, test, perf, ci, build or revert[/cyan]',
                    'Examples:',
                    '#1 <type>: #id-issue <description>:',
                    "git commit -m 'feature: #1234 feature example comment'",
                    '#2 <type>(scope): #id-issue <description>:',
                    "git commit -m 'feat(docs): #1234 feature example comment'",
                    '#3 <type>(scope): #id-issue <description>:',
                    "git commit -m 'fix(ui): #4321 bugfix example comment'",
                    '#4 <type>!: #id-issue <description>:',
                    "git commit -m 'fix!: #4321 chore example comment with possible breaking change'",
                    '#5 <type>!: #id-issue <description>:',
                    "git commit -m 'bugfix!: #4321 chore example comment with possible breaking change'",
                    '#6 <type>(scope)!: #id-issue <description>:',
                    "git commit -m 'refactor(chore)!: #4321 chore example comment with possible breaking change'",
                    '#7 <type>(scope)!: #id-issue <description>:',
                    "git commit -m 'chore(fix)!: #4321 drop support for Python 2.6' -m 'BREAKING CHANGE: Some features not available in Python 2.7-.'",
                    '[yellow] >>> More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/[/yellow]',
                    '[/red]',
                ],
                marks=[],
            ),
        ],
    )
    def test_messages(self, entrance, expected) -> NoReturn:
        """Test messages."""
        assert all(element in entrance for element in expected)

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'invalid-msg.txt',
                    msg_commit='commited this.',
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'valid-msg.txt',
                    msg_commit='feat: #1 implementado o metodo fake.',
                    expected=Result(SUCCESS, MESSAGESUCCESS),
                ),
                marks=[],
            ),
        ],
    )
    def test_prepare_commit_msg(self, entrance) -> NoReturn:
        """Test prepend commit message."""
        entrance.msg_file.write_text(entrance.msg_commit)
        result = prepare_commit_msg(entrance.msg_file)
        ic(result)
        assert result == entrance.expected

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(msg_file=test_dir / 'abc.txt', msg_commit='a' * 50)
            ),
            pytest.param(
                Entrance(msg_file=test_dir / 'bcd.txt', msg_commit='b' * 49)
            ),
            pytest.param(
                Entrance(msg_file=test_dir / 'bcd.txt', msg_commit='b' * 1000)
            ),
        ],
    )
    def test_check_len_first_line_commit_msg(self, entrance) -> NoReturn:
        """Test for check len first line commit messages."""
        entrance.msg_file.write_text(entrance.msg_commit)
        assert check_max_len_first_line_commit_msg(entrance.msg_file)

    def test_check_type_commit_msg(self) -> NoReturn:
        """Test for check type commit message."""
        test_file = self.test_dir / 'bcd.txt'
        test_file.write_bytes(b'xpto: abc')
        assert check_type_commit_msg(test_file).code == FAILURE

    def test_prepare_commit_msg_cli(self) -> NoReturn:
        """Test CLI prepend commit message."""
        test_file = self.test_dir / 'bcd.txt'
        test_file.write_bytes(b'xpto: abc')
        with pytest.raises(SystemExit):
            assert prepare_commit_msg_cli([test_file.as_posix()])

    def test_check_type_commit_msg_cli(self) -> NoReturn:
        """Test CLI for check type commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'')
        with pytest.raises(SystemExit):
            assert check_type_commit_msg_cli([test_file.as_posix()])

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param(
                'bugfix(refactor)!: bla bla bla bla bla bla bla', 0, marks=[]
            ),
            pytest.param('feat' * 15, 0, marks=[]),
        ],
    )
    def test_check_len_first_line_commit_msg_cli(
        self, capsys, entrance, expected
    ) -> NoReturn:
        """Test CLI for check len first line commit messages."""
        result = None
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)

        test_file.write_bytes(f'----- {entrance} -----\n'.encode())
        with pytest.raises(expected_exception=SystemExit):
            result = check_max_len_first_line_commit_msg_cli([
                test_file.as_posix()
            ])
        captured = capsys.readouterr()
        assert bool(result) is bool(expected)
        assert 'Error: Commit subject line exceeds' in captured.out
        assert not captured.err

    @pytest.mark.parametrize(
        ['entrance', 'expected'],
        [
            pytest.param('#Please enter the commit message', SUCCESS),
            pytest.param('feat: #61 Please enter the commit message', SUCCESS),
        ],
    )
    def test_clean_commit_msg_cli(self, entrance, expected) -> NoReturn:
        """Test CLI for clean-commit-msg-cli."""
        with NamedTemporaryFile(delete=False) as fl:
            filename = Path(fl.name)
            filename.write_text(entrance, encoding='utf-8')
        assert clean_commit_msg_cli([filename.as_posix(), '', '']) == expected

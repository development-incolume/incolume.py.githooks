"""Test module for prepare_commit_msg."""

# ruff: noqa: E501
from __future__ import annotations

from dataclasses import dataclass, field
import re
import shutil
from typing import NoReturn
from unittest.mock import patch
from icecream import ic
import pytest
from incolume.py.githooks.core.rules import Result, Status
import incolume.py.githooks.prepare_commit_msg as pkg
from tempfile import NamedTemporaryFile, gettempdir
from pathlib import Path
from inspect import stack


@dataclass
class Entrance:
    """Entrance dataclass for tests."""

    msg_file: str | Path = None
    msg_commit: str = ''
    params: list[str] = field(default_factory=list)
    expected: Result = field(
        default_factory=lambda: Result(Status.FAILURE, pkg.MESSAGERROR)
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
                pkg.MESSAGESUCCESS,
                ['Commit message is validated [OK]'],
                marks=[],
            ),
            pytest.param(
                pkg.MESSAGERROR,
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
                    expected=Result(Status.SUCCESS, pkg.MESSAGESUCCESS),
                ),
                marks=[],
            ),
        ],
    )
    def test_prepare_commit_msg(self, entrance) -> NoReturn:
        """Test prepend commit message."""
        entrance.msg_file.write_text(entrance.msg_commit)
        result = pkg.validate_format_commit_msg(entrance.msg_file)
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
        assert pkg.check_max_len_first_line_commit_msg(entrance.msg_file)

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_commit='a' * 51,
                    expected=Result(
                        Status.FAILURE,
                        message='Error: Commit message must start with a type',
                    ),
                ),
            ),
            pytest.param(
                Entrance(
                    msg_commit='fix: fixed a fake file',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                ),
            ),
            pytest.param(
                Entrance(
                    msg_commit='added: bcd.txt',
                    expected=Result(
                        code=Status.FAILURE, message='Error: Commit message'
                    ),
                ),
            ),
            pytest.param(
                Entrance(
                    msg_commit='feat: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='chore: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='docs: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='style: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='refactor: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='test: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='perf: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='ci: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
            pytest.param(
                Entrance(
                    msg_commit='build: fake feature',
                    expected=Result(
                        code=Status.SUCCESS, message=pkg.MESSAGESUCCESS
                    ),
                )
            ),
        ],
    )
    def test_check_type_commit_msg(self, entrance: Entrance) -> NoReturn:
        """Test for check type commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(entrance.msg_commit.encode())
        result = pkg.check_type_commit_msg(test_file)
        assert result.code == entrance.expected.code
        assert entrance.expected.message in result.message

    @pytest.mark.parametrize(
        ['entrance', 'len_line'],
        [
            pytest.param(
                Entrance(
                    msg_commit='a' * 3,
                    expected=Result(
                        Status.FAILURE,
                        'Error: Commit subject line has an insufficient number of 10 characters allowed (3 - aaa).',
                    ),
                ),
                10,
            ),
            pytest.param(
                Entrance(
                    msg_commit='b' * 10, expected=Result(Status.SUCCESS, '')
                ),
                10,
            ),
            pytest.param(
                Entrance(
                    msg_commit='c' * 20,
                    expected=Result(
                        Status.SUCCESS,
                        '[green]Commit minimum length for message is validated [OK][/green]',
                    ),
                ),
                15,
            ),
        ],
    )
    def test_min_len_first_line_commit_msg(
        self, entrance: Entrance, len_line: int
    ) -> NoReturn:
        """Test for min len first line commit messages."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(entrance.msg_commit.encode())
        result = pkg.check_min_len_first_line_commit_msg(test_file, len_line)
        assert result.code == entrance.expected.code

    @pytest.mark.parametrize(
        ['message_commit', 'return_value', 'expected'],
        [
            pytest.param(
                'new feature implemented about issue.',
                'feature/issue-1234',
                Result(
                    Status.SUCCESS,
                    '',
                ),
            ),
            pytest.param(
                'fixed implemented about bug.',
                'hotfix/issue-4321',
                Result(
                    Status.SUCCESS,
                    '',
                ),
            ),
            pytest.param(
                'incolume-py-githooks 1.99.0',
                'main',
                Result(
                    Status.SUCCESS,
                    '',
                ),
                marks=[],
            ),
            pytest.param(
                'incolume-py-githooks 1.99.0',
                'tests/issue-234',
                Result(
                    Status.FAILURE,
                    '\nIncorrect branch name',
                ),
                marks=[],
            ),
        ],
    )
    def test_prefixing_commit_msg(
        self, message_commit: str, return_value: str, expected: Result
    ) -> None:
        """Test prefixing commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(message_commit.encode())
        with patch.object(
            pkg,
            'get_branchname',
            return_value=return_value,
        ):
            result = pkg.prefixing_commit_msg(test_file)
            assert result == expected
            v = (
                f'[{x.group(2)}] {message_commit}'
                if (
                    x := (
                        re.compile(r'(feature|hotfix)/(\w+-\d+)').fullmatch(
                            return_value
                        )
                    )
                )
                else f'{message_commit}'
            )
            ic(v)
            assert test_file.read_text(encoding='utf-8') == v

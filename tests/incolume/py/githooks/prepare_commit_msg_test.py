"""Test module for prepare_commit_msg."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import shutil
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

    msg_file: str | Path = ''
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
                ],
                marks=[],
            ),
            pytest.param(
                pkg.MESSAGE_ALERT1,
                [
                    'type values: feature | feat, bugfix | fix, chore, refactor, docs, style, test, perf, ci, build or revert',
                ],
                marks=[],
            ),
            pytest.param(
                pkg.MESSAGE_ALERT2,
                [
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
                ],
                marks=[],
            ),
            pytest.param(
                pkg.MESSAGE_ALERT3,
                [
                    ' >>> More details on docs/user_guide/CONVENTIONAL_COMMITS.md or https://www.conventionalcommits.org/pt-br/v1.0.0/',
                ],
                marks=[],
            ),
        ],
    )
    def test_messages(self, entrance: list[str], expected: list[str]) -> None:
        """Verifica se as mensagens esperadas estão presentes na entrada."""
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
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'valid-msg-sem-issue.txt',
                    msg_commit='feat: configuração ruff',
                    expected=Result(Status.SUCCESS, pkg.MESSAGESUCCESS),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'valid-msg-issue-000.txt',
                    msg_commit='feat: #000 configuração ruff',
                    expected=Result(Status.SUCCESS, pkg.MESSAGESUCCESS),
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'invalid-msg-bugfix.txt',
                    msg_commit='bugfix: configuração ruff',
                ),
                marks=[],
            ),
            pytest.param(
                Entrance(
                    msg_file=test_dir / 'invalid-msg-case.txt',
                    msg_commit='Feat: configuração ruff',
                ),
                marks=[],
            ),
        ],
    )
    def test_prepare_commit_msg(self, entrance: Entrance) -> None:
        """Test prepend commit message."""
        Path(entrance.msg_file).write_text(
            entrance.msg_commit, encoding='utf-8'
        )
        result = pkg.validate_format_commit_msg(entrance.msg_file)
        ic(result)
        assert result == entrance.expected

    @pytest.mark.parametrize(
        ['msg_commit', 'len_line', 'expected_code'],
        [
            pytest.param('a' * 50, 50, Status.SUCCESS, marks=[]),
            pytest.param('a' * 51, 50, Status.FAILURE, marks=[]),
            pytest.param('b' * 49, 50, Status.SUCCESS, marks=[]),
            pytest.param('b' * 1000, 50, Status.FAILURE, marks=[]),
            # `max_first_line` abaixo de 50 tem de ser respeitado.
            pytest.param('c' * 6, 5, Status.FAILURE, marks=[]),
            pytest.param('c' * 4, 5, Status.SUCCESS, marks=[]),
        ],
    )
    def test_check_max_len_first_line_commit_msg(
        self, msg_commit: str, len_line: int, expected_code: Status
    ) -> None:
        """`check_max_len_first_line_commit_msg` respeita `len_line`."""
        msg_file = self.test_dir / 'max_len.txt'
        msg_file.write_text(msg_commit, encoding='utf-8')
        result = pkg.check_max_len_first_line_commit_msg(
            msg_file, len_line=len_line
        )
        assert result.code == expected_code

    @pytest.mark.parametrize(
        'entrance',
        [
            pytest.param(
                Entrance(
                    msg_commit='a' * 51,
                    expected=Result(
                        Status.FAILURE,
                        message='Error: Commit message must start with one of types: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test).\n\te.g.: \n\t  git commit -m "feat: commit description;"\n\t  git commit -m "refactor(style)!: commit description;" -m "BREAKING CHANGE: descripton breaking"\n\t  git commit -m "style(lang): adding translation for brazilian portuguese"\n',
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
                        code=Status.FAILURE,
                        message='Error: Commit message must start with one of types: build, chore, ci, docs, feat, fix, perf, refactor, revert, style, test).\n\te.g.: \n\t  git commit -m "feat: commit description;"\n\t  git commit -m "refactor(style)!: commit description;" -m "BREAKING CHANGE: descripton breaking"\n\t  git commit -m "style(lang): adding translation for brazilian portuguese"\n',
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
    def test_check_type_commit_msg(self, entrance: Entrance) -> None:
        """Test for check type commit message."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(entrance.msg_commit.encode())
        result = pkg.check_type_commit_msg(test_file)
        assert result.code == entrance.expected.code
        assert str(entrance.expected.message) in str(result.message)
        assert result.message == entrance.expected.message

    def test_check_type_commit_msg_without_file(self) -> None:
        """Sem arquivo, usa COMMIT_EDITMSG e nao levanta IsADirectoryError."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'feat: fake feature')
        with patch.object(pkg, 'get_commit_msg_file', return_value=test_file):
            result = pkg.check_type_commit_msg()
        assert result.code == Status.SUCCESS
        assert result.message == pkg.MESSAGESUCCESS

    @pytest.mark.parametrize('tipo', sorted(pkg.TypeCommit.to_set()))
    def test_rules_single_type_list(self, tipo: str) -> None:
        """Tipo e formato partilham a mesma lista de tipos."""
        assert re.match(pkg.RULE_TYPE, f'{tipo}: x')
        assert re.match(pkg.RULE_COMMITFORMAT, f'{tipo}: x')

    @pytest.mark.parametrize(
        'tipo', ['bugfix', 'feature', 'other', 'Feat', 'added']
    )
    def test_rules_reject_out_of_list(self, tipo: str) -> None:
        """Tipos fora da lista sao rejeitados pelas duas regras."""
        assert not re.match(pkg.RULE_TYPE, f'{tipo}: x')
        assert not re.match(pkg.RULE_COMMITFORMAT, f'{tipo}: x')

    @pytest.mark.parametrize('tipo', sorted(pkg.TypeCommit.to_set()))
    def test_rules_accept_issue_prefix(self, tipo: str) -> None:
        """Regras aceitam o prefixo [ISSUE-n] do set-issue-from-branch."""
        assert re.match(pkg.RULE_TYPE, f'[ISSUE-434] {tipo}: x')
        assert re.match(pkg.RULE_COMMITFORMAT, f'[ISSUE-434] {tipo}: x')

    @pytest.mark.parametrize(
        'msg',
        ['[ISSUE-434] other: x', '[ISSUE-abc] fix: x'],
    )
    def test_rules_reject_invalid_issue_prefix(self, msg: str) -> None:
        """Prefixo malformado ou tipo fora da lista seguem rejeitados."""
        assert not re.match(pkg.RULE_TYPE, msg)
        assert not re.match(pkg.RULE_COMMITFORMAT, msg)

    def test_rules_reject_issue_prefix_without_description(self) -> None:
        """Formato exige descricao apos o tipo, mesmo com prefixo."""
        assert not re.match(pkg.RULE_COMMITFORMAT, '[ISSUE-434] fix:')

    def test_check_type_commit_msg_with_issue_prefix(self) -> None:
        """Mensagem prefixada pelo set-issue-from-branch passa no tipo."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'[ISSUE-434] fix: #434 ativa hooks')
        result = pkg.check_type_commit_msg(test_file)
        assert result.code == Status.SUCCESS
        assert result.message == pkg.MESSAGESUCCESS

    def test_validate_format_commit_msg_with_issue_prefix(self) -> None:
        """Mensagem prefixada passa na validacao de formato."""
        with NamedTemporaryFile(dir=self.test_dir) as fl:
            test_file = Path(fl.name)
        test_file.write_bytes(b'[ISSUE-434] fix: #434 ativa hooks')
        result = pkg.validate_format_commit_msg(test_file)
        assert result.code == Status.SUCCESS
        assert result.message == pkg.MESSAGESUCCESS

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
    ) -> None:
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

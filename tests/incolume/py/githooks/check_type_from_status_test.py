"""Module test check_type_from_status hook."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from incolume.py.githooks import check_type_from_status as pkg
from incolume.py.githooks.check_type_from_status import (
    check_type_from_status,
)
from incolume.py.githooks.cli.cli import check_type_from_status_cli

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner


def _message(base: Path, text: str) -> Path:
    """Escreve um arquivo de mensagem de commit."""
    path = base / 'commit-msg.txt'
    path.write_text(text, encoding='utf-8')
    return path


def _check(msg: Path, paths: list[str]) -> int:
    """Executa o hook com os paths stageados."""
    result: int = check_type_from_status([str(msg)], paths=paths)
    return result


class TestCaseCheckTypeFromStatus:
    """Criterios do hook check-type-from-status (#376)."""

    @pytest.mark.parametrize(
        ['paths', 'message', 'expected'],
        [
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'docs: ajusta o hook\n',
                1,
            ),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'build: ajusta o hook\n',
                1,
            ),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'test: ajusta o hook\n',
                1,
            ),
            pytest.param(['docs/hooks.md'], 'feat: documenta o hook\n', 1),
            pytest.param(['pyproject.toml'], 'feat: ajusta dependencia\n', 1),
            pytest.param(
                ['tests/incolume/py/githooks/foo_test.py'],
                'feat: cobre o hook\n',
                1,
            ),
            pytest.param(
                ['.github/workflows/ci.yml'],
                'docs: ajusta pipeline\n',
                1,
            ),
            pytest.param(['CHANGELOG.md'], 'feat: atualiza changelog\n', 1),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'feat: novo hook\n',
                0,
            ),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'fix: corrige o hook\n',
                0,
            ),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'refactor: refatora o hook\n',
                0,
            ),
            pytest.param(['docs/hooks.md'], 'docs: documenta o hook\n', 0),
            pytest.param(['pyproject.toml'], 'build: ajusta dependencia\n', 0),
            pytest.param(
                ['.github/workflows/ci.yml'],
                'ci: ajusta pipeline\n',
                0,
            ),
            pytest.param(
                ['tests/incolume/py/githooks/foo_test.py'],
                'test: cobre o hook\n',
                0,
            ),
            pytest.param([], 'feat: qualquer coisa\n', 0),
            pytest.param(
                ['incolume/py/githooks/cli/cli.py'],
                'mensagem sem tipo\n',
                0,
            ),
        ],
    )
    def test_check_type_from_status(
        self,
        tmp_path: Path,
        paths: list[str],
        message: str,
        expected: int,
    ) -> None:
        """Bloqueia apenas divergencia objetiva de tipo."""
        msg = _message(tmp_path, message)

        assert _check(msg, paths) == expected

    def test_issue_prefix_ignorado(self, tmp_path: Path) -> None:
        """O prefixo [ISSUE-*] nao atrapalha a leitura do tipo."""
        msg = _message(tmp_path, '[ISSUE-376] feat: novo hook\n')

        assert _check(msg, ['incolume/py/githooks/cli/cli.py']) == 0

    def test_prefixo_issue_com_tipo_errado(self, tmp_path: Path) -> None:
        """O tipo e lido mesmo com o prefixo [ISSUE-*]."""
        msg = _message(tmp_path, '[ISSUE-376] docs: ajusta o hook\n')

        assert _check(msg, ['incolume/py/githooks/cli/cli.py']) == 1

    def test_multiplos_arquivos_de_mensagem(self, tmp_path: Path) -> None:
        """Qualquer arquivo invalido reprova o commit."""
        ok = _message(tmp_path, 'feat: novo hook\n')
        bad = _message(tmp_path, 'docs: ajusta o hook\n')

        assert (
            check_type_from_status(
                [str(ok), str(bad)],
                paths=['incolume/py/githooks/cli/cli.py'],
            )
            == 1
        )

    def test_codigo_domina_sobre_build(self, tmp_path: Path) -> None:
        """Codigo staged com pyproject: tipo deduzido e feat."""
        msg = _message(tmp_path, 'feat: novo hook\n')

        assert (
            _check(
                msg,
                ['incolume/py/githooks/cli/cli.py', 'pyproject.toml'],
            )
            == 0
        )

    def test_cli_bloqueia(self, tmp_path: Path, cli_runner: CliRunner) -> None:
        """CLI retorna 1 em divergencia objetiva."""
        msg = _message(tmp_path, 'docs: ajusta o hook\n')
        with patch.object(
            pkg,
            'get_staged_files',
            return_value=['incolume/py/githooks/cli/cli.py'],
        ):
            result = cli_runner.invoke(
                check_type_from_status_cli,
                [str(msg)],
            )

        assert result.exit_code == 1

    def test_cli_aceita(self, tmp_path: Path, cli_runner: CliRunner) -> None:
        """CLI retorna 0 sem divergencia."""
        msg = _message(tmp_path, 'feat: novo hook\n')
        with patch.object(
            pkg,
            'get_staged_files',
            return_value=['incolume/py/githooks/cli/cli.py'],
        ):
            result = cli_runner.invoke(
                check_type_from_status_cli,
                [str(msg)],
            )

        assert result.exit_code == 0

    def test_cli_nonexequi(
        self, tmp_path: Path, cli_runner: CliRunner
    ) -> None:
        """Flag -N nao executa o hook."""
        msg = _message(tmp_path, 'docs: ajusta o hook\n')
        with patch.object(
            pkg,
            'get_staged_files',
            return_value=['incolume/py/githooks/cli/cli.py'],
        ):
            result = cli_runner.invoke(
                check_type_from_status_cli,
                ['-N', str(msg)],
            )

        assert result.exit_code == 0

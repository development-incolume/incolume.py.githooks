"""Tests for the set-type-from-status hook."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest

from incolume.py.githooks import type_from_status
from incolume.py.githooks.cli import cli

if TYPE_CHECKING:
    from click.testing import CliRunner
    from pathlib import Path


class TestCaseSetTypeFromStatus:
    """Inject the deduced type into the commit message template."""

    @pytest.mark.parametrize(
        ['paths', 'content', 'expected'],
        [
            pytest.param(
                ['incolume/py/githooks/new_hook.py'],
                'adiciona novo hook\n',
                'feat: adiciona novo hook\n',
            ),
            pytest.param(
                ['docs/hooks.md'],
                'documenta o hook\n',
                'docs: documenta o hook\n',
            ),
            pytest.param(
                ['tests/incolume/py/githooks/new_hook_test.py'],
                'cobre o hook\n',
                'test: cobre o hook\n',
            ),
            pytest.param(
                ['pyproject.toml'],
                'registra entry point\n',
                'build: registra entry point\n',
            ),
            pytest.param(
                ['.github/workflows/ci.yml'],
                'ajusta pipeline\n',
                'ci: ajusta pipeline\n',
            ),
            pytest.param(
                ['docs/hooks.md'],
                'fix: corrige o hook\n',
                'fix: corrige o hook\n',
            ),
            pytest.param(
                ['docs/hooks.md'],
                'bugfix: corrige o hook\n',
                'bugfix: corrige o hook\n',
            ),
            pytest.param(
                ['docs/hooks.md'],
                '[ISSUE-375] documenta o hook\n',
                '[ISSUE-375] docs: documenta o hook\n',
            ),
            pytest.param(
                [],
                'mensagem sem arquivos staged\n',
                'mensagem sem arquivos staged\n',
            ),
        ],
    )
    def test_set_type_from_status(
        self,
        cli_runner: CliRunner,
        tmp_path: Path,
        paths: list[str],
        content: str,
        expected: str,
    ) -> None:
        """Type is injected once, after the issue prefix when present."""
        msg_file = tmp_path / 'COMMIT_EDITMSG'
        msg_file.write_text(content, encoding='utf-8')

        with patch.object(
            type_from_status, 'get_staged_files', return_value=paths
        ):
            result = cli_runner.invoke(
                cli.set_type_from_status_cli, [str(msg_file)]
            )

        assert result.exit_code == 0
        assert msg_file.read_text(encoding='utf-8') == expected

    def test_set_type_from_status_nonexequi(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """--nonexequi leaves the message untouched."""
        msg_file = tmp_path / 'COMMIT_EDITMSG'
        msg_file.write_text('adiciona novo hook\n', encoding='utf-8')

        with patch.object(
            type_from_status,
            'get_staged_files',
            return_value=['incolume/py/githooks/new_hook.py'],
        ):
            result = cli_runner.invoke(
                cli.set_type_from_status_cli, [str(msg_file), '-N']
            )

        assert result.exit_code == 0
        assert 'nonexequi' in result.output
        assert msg_file.read_text(encoding='utf-8') == 'adiciona novo hook\n'

    def test_set_type_from_status_commit_type_message(
        self, cli_runner: CliRunner, tmp_path: Path
    ) -> None:
        """A message given with -m is never rewritten."""
        msg_file = tmp_path / 'COMMIT_EDITMSG'
        msg_file.write_text('adiciona novo hook\n', encoding='utf-8')

        with patch.object(
            type_from_status,
            'get_staged_files',
            return_value=['incolume/py/githooks/new_hook.py'],
        ):
            result = cli_runner.invoke(
                cli.set_type_from_status_cli, [str(msg_file), 'message']
            )

        assert result.exit_code == 0
        assert msg_file.read_text(encoding='utf-8') == 'adiciona novo hook\n'

"""Module test check_manual_changelog hook."""

# ruff: file-ignore[subprocess-without-shell-equals-true, start-process-with-partial-path]

from __future__ import annotations

import os
import subprocess  # ruff: ignore[suspicious-subprocess-import]
from typing import TYPE_CHECKING

import pytest

from incolume.py.githooks.check_manual_changelog import (
    check_manual_changelog,
)
from incolume.py.githooks.cli.cli import check_manual_changelog_cli

if TYPE_CHECKING:
    from pathlib import Path

    from click.testing import CliRunner

_GIT_ENV: dict[str, str] = {
    **os.environ,
    'GIT_CONFIG_GLOBAL': os.devnull,
    'GIT_CONFIG_SYSTEM': os.devnull,
    'GIT_AUTHOR_NAME': 'Tico OpenBot',
    'GIT_AUTHOR_EMAIL': 'dev@incolume.com.br',
    'GIT_COMMITTER_NAME': 'Tico OpenBot',
    'GIT_COMMITTER_EMAIL': 'dev@incolume.com.br',
}

CHANGELOG: str = '# Changelog\n\n## 1.0.0\n'


def _git(repo: Path, *args: str) -> str:
    """Executa um comando git no repositorio descartavel."""
    return subprocess.check_output(
        ['git', *args],
        cwd=repo,
        text=True,
        stderr=subprocess.DEVNULL,
        env=_GIT_ENV,
    ).strip()


def _make_repo(base: Path, files: dict[str, str]) -> Path:
    """Cria um repositorio git com os arquivos no commit inicial."""
    repo = base / 'repo'
    repo.mkdir()
    _git(repo, 'init', '-q')
    for name, content in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    _git(repo, 'add', '-A')
    _git(repo, 'commit', '-q', '-m', 'chore: baseline')
    return repo


def _write(repo: Path, name: str, content: str) -> None:
    """Escreve um arquivo dentro do repositorio."""
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def _message(base: Path, text: str) -> Path:
    """Escreve um arquivo de mensagem de commit."""
    path = base / 'commit-msg.txt'
    path.write_text(text, encoding='utf-8')
    return path


def _check(repo: Path, msg: Path) -> int:
    """Executa o hook apontando para o repositorio descartavel."""
    result: int = check_manual_changelog([str(msg)], repo_root=repo)
    return result


class TestCaseCheckManualChangelog:
    """Criterios do hook check-manual-changelog (#368)."""

    def test_changelog_alterado_sem_build_rejeita(
        self, tmp_path: Path
    ) -> None:
        """CHANGELOG.md staged mudou e mensagem nao e build."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'docs: ajusta changelog\n')

        assert _check(repo, msg) == 1

    def test_changelog_alterado_com_build_aceita(self, tmp_path: Path) -> None:
        """CHANGELOG.md staged mudou com mensagem build."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'build: release 1.1.0\n')

        assert _check(repo, msg) == 0

    def test_sem_alteracao_de_changelog_aceita(self, tmp_path: Path) -> None:
        """Outros arquivos staged nao atingem o changelog."""
        repo = _make_repo(
            tmp_path,
            {'CHANGELOG.md': CHANGELOG, 'README.md': '# x\n'},
        )
        _write(repo, 'README.md', '# x\n\najuste\n')
        _git(repo, 'add', 'README.md')
        msg = _message(tmp_path, 'docs: ajusta readme\n')

        assert _check(repo, msg) == 0

    def test_changelog_novo_sem_head_rejeita(self, tmp_path: Path) -> None:
        """CHANGELOG.md novo no indice, sem versao no HEAD."""
        repo = _make_repo(tmp_path, {'README.md': '# x\n'})
        _write(repo, 'CHANGELOG.md', CHANGELOG)
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'docs: adiciona changelog\n')

        assert _check(repo, msg) == 1

    def test_changelog_removido_rejeita(self, tmp_path: Path) -> None:
        """CHANGELOG.md removido no indice tambem altera o changelog."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        (repo / 'CHANGELOG.md').unlink()
        _git(repo, 'add', '-A')
        msg = _message(tmp_path, 'chore: remove changelog\n')

        assert _check(repo, msg) == 1

    def test_working_tree_sem_stage_aceita(self, tmp_path: Path) -> None:
        """Working tree mudou o changelog, mas o staged nao: aceita."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 9.9.9\n')
        msg = _message(tmp_path, 'docs: sem staged\n')

        assert _check(repo, msg) == 0

    def test_repositorio_sem_changelog_aceita(self, tmp_path: Path) -> None:
        """Repositorio sem CHANGELOG.md."""
        repo = _make_repo(tmp_path, {'README.md': '# x\n'})
        _write(repo, 'README.md', '# x\n\najuste\n')
        _git(repo, 'add', 'README.md')
        msg = _message(tmp_path, 'docs: ajusta readme\n')

        assert _check(repo, msg) == 0

    def test_repositorio_nao_git_aceita(self, tmp_path: Path) -> None:
        """Diretorio sem git: falha aberta, sem erro."""
        plain = tmp_path / 'plain'
        plain.mkdir()
        msg = _message(tmp_path, 'docs: mensagem\n')

        assert _check(plain, msg) == 0

    @pytest.mark.parametrize(
        'text',
        [
            'docs: ajusta changelog\n',
            'feat: nova funcionalidade\n',
        ],
    )
    def test_mensagem_nao_build_rejeita(
        self, tmp_path: Path, text: str
    ) -> None:
        """Somente o prefixo exato `build:` libera a mudanca do changelog."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, text)

        assert _check(repo, msg) == 1

    def test_cli_rejeita_sem_build(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """CLI retorna 1 quando o changelog muda sem build."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'docs: ajusta changelog\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(check_manual_changelog_cli, [str(msg)])

        assert result.exit_code == 1

    def test_cli_aceita_com_build(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """CLI retorna 0 quando o changelog muda com build."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'build: release 1.1.0\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(check_manual_changelog_cli, [str(msg)])

        assert result.exit_code == 0

    def test_cli_nonexequi(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Flag -N nao executa o hook."""
        repo = _make_repo(tmp_path, {'CHANGELOG.md': CHANGELOG})
        _write(repo, 'CHANGELOG.md', f'{CHANGELOG}\n## 1.1.0\n')
        _git(repo, 'add', 'CHANGELOG.md')
        msg = _message(tmp_path, 'docs: ajusta changelog\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(
            check_manual_changelog_cli,
            ['-N', str(msg)],
        )

        assert result.exit_code == 0

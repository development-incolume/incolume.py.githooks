"""Module test check_manual_version hook."""

# ruff: file-ignore[subprocess-without-shell-equals-true, start-process-with-partial-path]

from __future__ import annotations

import os
import subprocess  # ruff: ignore[suspicious-subprocess-import]
from typing import TYPE_CHECKING

import pytest

from incolume.py.githooks.check_manual_version import check_manual_version
from incolume.py.githooks.cli.cli import check_manual_version_cli

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

PYPROJECT: str = """\
[project]
name = "sample"
version = "{version}"

dependencies = [{deps}]

[tool.sample]
version = "{tool_version}"
"""


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


def _pyproject(version: str, deps: str = '', tool: str = '1.0.0') -> str:
    """Monta um pyproject.toml com [project].version controlada."""
    return PYPROJECT.format(version=version, deps=deps, tool_version=tool)


def _check(repo: Path, msg: Path) -> int:
    """Executa o hook apontando para o repositorio descartavel."""
    result: int = check_manual_version([str(msg)], repo_root=repo)
    return result


class TestCaseCheckManualVersion:
    """Criterios do hook check-manual-version (#367)."""

    def test_versao_pyproject_alterada_sem_build_rejeita(
        self, tmp_path: Path
    ) -> None:
        """Versao de [project] staged mudou e mensagem nao e build."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_versao_pyproject_alterada_com_build_aceita(
        self, tmp_path: Path
    ) -> None:
        """Versao de [project] staged mudou com mensagem build."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'build: sample 2.0.0\n')

        assert _check(repo, msg) == 0

    def test_sem_alteracao_de_versao_aceita(self, tmp_path: Path) -> None:
        """Mudanca de dependencia com mensagem comum nao e versao."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(
            repo,
            'pyproject.toml',
            _pyproject('1.0.0', deps='\n    "click>=8.2.1",\n'),
        )
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'chore: ajusta dependencias\n')

        assert _check(repo, msg) == 0

    def test_version_txt_aninhado_sem_build_rejeita(
        self, tmp_path: Path
    ) -> None:
        """version.txt aninhado com valor alterado exige build."""
        repo = _make_repo(
            tmp_path,
            {
                'pyproject.toml': _pyproject('1.0.0'),
                'pkg/version.txt': '1.0.0\n',
            },
        )
        _write(repo, 'pkg/version.txt', '2.0.0\n')
        _git(repo, 'add', 'pkg/version.txt')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_version_txt_aninhado_com_build_aceita(
        self, tmp_path: Path
    ) -> None:
        """version.txt aninhado com valor alterado e mensagem build."""
        repo = _make_repo(
            tmp_path,
            {
                'pyproject.toml': _pyproject('1.0.0'),
                'pkg/version.txt': '1.0.0\n',
            },
        )
        _write(repo, 'pkg/version.txt', '2.0.0\n')
        _git(repo, 'add', 'pkg/version.txt')
        msg = _message(tmp_path, 'build: sample 2.0.0\n')

        assert _check(repo, msg) == 0

    def test_version_txt_tocado_sem_mudanca_de_valor_aceita(
        self, tmp_path: Path
    ) -> None:
        """version.txt staged sem alterar o valor da versao."""
        repo = _make_repo(
            tmp_path,
            {
                'pyproject.toml': _pyproject('1.0.0'),
                'pkg/version.txt': '1.0.0\n',
            },
        )
        _write(repo, 'pkg/version.txt', '1.0.0\n\n')
        _git(repo, 'add', 'pkg/version.txt')
        msg = _message(tmp_path, 'style: ajusta quebra de linha\n')

        assert _check(repo, msg) == 0

    def test_version_txt_no_caminho_real_do_pacote(
        self, tmp_path: Path
    ) -> None:
        """O glob casa o version.txt real: incolume/py/githooks/version.txt."""
        repo = _make_repo(
            tmp_path,
            {
                'pyproject.toml': _pyproject('1.0.0'),
                'incolume/py/githooks/version.txt': '1.23.0a1\n',
            },
        )
        _write(repo, 'incolume/py/githooks/version.txt', '1.23.0a2\n')
        _git(repo, 'add', 'incolume/py/githooks/version.txt')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_version_txt_novo_sem_head_rejeita(self, tmp_path: Path) -> None:
        """version.txt novo no indice, sem versao no HEAD."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pkg/version.txt', '2.0.0\n')
        _git(repo, 'add', 'pkg/version.txt')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_version_txt_removido_rejeita(self, tmp_path: Path) -> None:
        """version.txt removido no indice tambem altera a versao."""
        repo = _make_repo(
            tmp_path,
            {
                'pyproject.toml': _pyproject('1.0.0'),
                'pkg/version.txt': '1.0.0\n',
            },
        )
        (repo / 'pkg' / 'version.txt').unlink()
        _git(repo, 'add', '-A')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_pyproject_removido_rejeita(self, tmp_path: Path) -> None:
        """pyproject.toml removido no indice altera a versao."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        (repo / 'pyproject.toml').unlink()
        _git(repo, 'add', '-A')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_pyproject_sem_project_version_rejeita(
        self, tmp_path: Path
    ) -> None:
        """pyproject.toml staged sem [project].version altera a versao."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', '[project]\nname = "sample"\n')
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_sem_mudanca_staged_aceita(self, tmp_path: Path) -> None:
        """Nada staged: nao ha diff de versao a comparar."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        msg = _message(tmp_path, 'chore: sem alteracoes\n')

        assert _check(repo, msg) == 0

    def test_compara_staged_com_head_ignora_working_tree_aceita(
        self, tmp_path: Path
    ) -> None:
        """Working tree mudou a versao, mas o staged nao: aceita."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(
            repo,
            'pyproject.toml',
            _pyproject('1.0.0', deps='\n    "click>=8.2.1",\n'),
        )
        _git(repo, 'add', 'pyproject.toml')
        _write(repo, 'pyproject.toml', _pyproject('9.9.9'))
        msg = _message(tmp_path, 'chore: ajusta dependencias\n')

        assert _check(repo, msg) == 0

    def test_compara_staged_com_head_ignora_working_tree_rejeita(
        self, tmp_path: Path
    ) -> None:
        """Working tree voltou a versao do HEAD, staged mudou: rejeita."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        _write(repo, 'pyproject.toml', _pyproject('1.0.0'))
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 1

    def test_outro_campo_version_nao_conta(self, tmp_path: Path) -> None:
        """Somente [project].version e [**/version.txt] contam."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('1.0.0', tool='9.9.9'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')

        assert _check(repo, msg) == 0

    def test_sem_arquivo_de_versao_aceita(self, tmp_path: Path) -> None:
        """Repositorio sem pyproject.toml nem version.txt."""
        repo = _make_repo(tmp_path, {'README.md': '# sample\n'})
        _write(repo, 'README.md', '# sample\n\najuste\n')
        _git(repo, 'add', 'README.md')
        msg = _message(tmp_path, 'docs: ajusta readme\n')

        assert _check(repo, msg) == 0

    @pytest.mark.parametrize(
        'text',
        [
            'feat: nova funcionalidade\n',
            'FIX: corrige algo\n',
        ],
    )
    def test_mensagem_nao_build_rejeita(
        self, tmp_path: Path, text: str
    ) -> None:
        """Somente o prefixo exato `build:` libera a mudanca de versao."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, text)

        assert _check(repo, msg) == 1

    def test_cli_rejeita_sem_build(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """CLI retorna 1 quando a versao muda sem build."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(check_manual_version_cli, [str(msg)])

        assert result.exit_code == 1

    def test_cli_aceita_com_build(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """CLI retorna 0 quando a versao muda com build."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'build: sample 2.0.0\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(check_manual_version_cli, [str(msg)])

        assert result.exit_code == 0

    def test_cli_nonexequi(
        self,
        tmp_path: Path,
        cli_runner: CliRunner,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Flag -N nao executa o hook."""
        repo = _make_repo(tmp_path, {'pyproject.toml': _pyproject('1.0.0')})
        _write(repo, 'pyproject.toml', _pyproject('2.0.0'))
        _git(repo, 'add', 'pyproject.toml')
        msg = _message(tmp_path, 'feat: nova funcionalidade\n')
        monkeypatch.chdir(repo)

        result = cli_runner.invoke(check_manual_version_cli, ['-N', str(msg)])

        assert result.exit_code == 0

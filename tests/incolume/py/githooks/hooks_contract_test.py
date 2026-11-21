"""Trava o contrato do hook validate-message-commit nos YAMLs do repo."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

import pytest
import yaml

from incolume.py.githooks import cli
from incolume.py.githooks.core.rules import Status
from incolume.py.githooks.validate_branchname import ValidateBranchname

if TYPE_CHECKING:
    from collections.abc import Callable

REPO_ROOT = Path(__file__).parents[4]
HOOK_ID = 'validate-message-commit'
STAGES = ['commit-msg', 'manual']


def _load(name: str) -> Any:
    """Carrega um YAML da raiz do repositorio."""
    return yaml.safe_load((REPO_ROOT / name).read_text(encoding='utf-8'))


def _config_hook() -> dict[str, Any]:
    """Retorna o bloco do hook no .pre-commit-config.yaml."""
    repos = _load('.pre-commit-config.yaml')['repos']
    for repo in repos:
        for hook in repo.get('hooks', []):
            if hook.get('id') == HOOK_ID:
                return cast('dict[str, Any]', hook)
    pytest.fail(f'{HOOK_ID} ausente do .pre-commit-config.yaml')
    raise AssertionError  # pragma: no cover


def _public_hook() -> dict[str, Any]:
    """Retorna o bloco do hook no .pre-commit-hooks.yaml."""
    for hook in _load('.pre-commit-hooks.yaml'):
        if hook.get('id') == HOOK_ID:
            return cast('dict[str, Any]', hook)
    pytest.fail(f'{HOOK_ID} ausente do .pre-commit-hooks.yaml')
    raise AssertionError  # pragma: no cover


class TestCaseValidateMessageCommitContract:
    """Contrato de stages/types_or do validate-message-commit."""

    def test_config_sem_types_or(self) -> None:
        """O config do repo nao filtra por tipo de arquivo."""
        assert 'types_or' not in _config_hook()

    def test_publico_sem_types_or(self) -> None:
        """O contrato publico nao filtra por tipo de arquivo."""
        assert 'types_or' not in _public_hook()

    @pytest.mark.parametrize('bloco', [_config_hook, _public_hook])
    def test_stages_apenas_commit_msg(
        self,
        bloco: Callable[[], dict[str, Any]],
    ) -> None:
        """O arquivo de mensagem so existe no estagio commit-msg."""
        assert bloco()['stages'] == STAGES

    def test_contratos_concordam(self) -> None:
        """Config local e contrato publico declaram o mesmo comportamento."""
        config, publico = _config_hook(), _public_hook()
        assert config['stages'] == publico['stages']
        assert config['pass_filenames'] == publico['pass_filenames']
        assert config['always_run'] == publico['always_run']

    def test_cli_docstring_reflete_commit_msg(self) -> None:
        """A docstring do comando cita o estagio real do hook."""
        docstring = cli.validate_format_commit_msg_cli.__doc__ or ''
        assert 'commit-msg' in docstring
        assert 'prepare-commit-msg' not in docstring


class TestCaseProtectedBranchesContract:
    """Contrato: `dev` e `tags` protegidos no config do repo e no modelo."""

    def _config_hooks(self) -> dict[str, dict[str, Any]]:
        """Mapa `id` -> bloco do hook no `.pre-commit-config.yaml`."""
        repos = _load('.pre-commit-config.yaml')['repos']
        return {
            cast('dict[str, Any]', hook)['id']: cast('dict[str, Any]', hook)
            for repo in repos
            for hook in repo.get('hooks', [])
        }

    def test_no_commit_to_branch_protege_dev_e_tags(self) -> None:
        """`no-commit-to-branch` bloqueia commit em `dev` e `tags`."""
        args = self._config_hooks()['no-commit-to-branch'].get('args', [])
        protegidas = set(args[1::2])
        assert {'main', 'master', 'dev', 'tags'} <= protegidas

    def test_check_valid_branchname_protege_dev_e_tags(self) -> None:
        """`is-valid-branchname` passa a rodar com `--dev --tags`."""
        args = self._config_hooks()['check-valid-branchname'].get('args', [])
        assert '--dev' in args
        assert '--tags' in args

    def test_readme_model_reflete_protecao(self) -> None:
        """O modelo do README mostra a mesma protecao."""
        modelo = (REPO_ROOT / 'README.md').read_text(encoding='utf-8')
        assert '--branch, dev' in modelo
        assert '--branch, tags' in modelo
        assert '--dev, --tags' in modelo

    @pytest.mark.parametrize('branch', ['dev', 'tags'])
    def test_validate_branchname_rejeita_dev_e_tags(self, branch: str) -> None:
        """O validador rejeita `dev`/`tags` quando protegidos."""
        kwargs: dict[str, Any] = {
            'protected_dev': True,
            'protected_tags': True,
        }
        result = ValidateBranchname().is_valid(branchname=branch, **kwargs)
        assert result.code == Status.FAILURE

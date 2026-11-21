"""Trava o mapa de hooks publicados nao usados neste repo (issue #435)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest
import yaml

REPO_ROOT = Path(__file__).parents[4]

UNUSED_HOOKS = {
    'check-manual-changelog',
    'check-manual-version',
    'check-precommit-installed',
    'check-type-from-status',
    'set-type-from-status',
}
SECTION = '## Hooks publicados não usados neste repositório'


def _load(name: str) -> Any:
    """Carrega um YAML da raiz do repositorio."""
    return yaml.safe_load((REPO_ROOT / name).read_text(encoding='utf-8'))


def _unused_ids() -> set[str]:
    """Ids publicados cujo entry nao roda no config local do repo."""
    used_entries = {
        hook.get('entry')
        for repo in _load('.pre-commit-config.yaml')['repos']
        for hook in repo.get('hooks', [])
    }
    return {
        cast('str', hook['id'])
        for hook in _load('.pre-commit-hooks.yaml')
        if hook['entry'] not in used_entries
    }


def _doc() -> str:
    """Le o docs/hooks.md."""
    return (REPO_ROOT / 'docs' / 'hooks.md').read_text(encoding='utf-8')


class TestCaseUnusedHooksContract:
    """Mapa da #435: hooks publicados sem uso local, com justificativa."""

    def test_mapa_de_nao_usados(self) -> None:
        """O conjunto de nao usados e exatamente o mapa aprovado."""
        assert _unused_ids() == UNUSED_HOOKS

    def test_secao_existe(self) -> None:
        """O docs/hooks.md tem a secao do mapa de nao usados."""
        assert SECTION in _doc()

    @pytest.mark.parametrize('hook_id', sorted(UNUSED_HOOKS))
    def test_justificativa_documentada(self, hook_id: str) -> None:
        """Cada hook nao usado tem subsecao propria com justificativa."""
        doc = _doc()
        heading = f'### `{hook_id}`'
        assert heading in doc
        body = doc.split(heading, 1)[1].split('\n#', 1)[0].strip()
        assert body

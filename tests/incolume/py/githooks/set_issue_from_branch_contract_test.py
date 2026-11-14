"""Trava o contrato do hook set-issue-from-branch no manifesto publico."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest
import yaml

REPO_ROOT = Path(__file__).parents[4]
HOOK_ID = 'set-issue-from-branch'
ENTRY = 'set-issue-from-branch'


def _public_hooks() -> list[dict[str, Any]]:
    """Hooks do contrato publico `.pre-commit-hooks.yaml`."""
    hooks = yaml.safe_load(
        (REPO_ROOT / '.pre-commit-hooks.yaml').read_text(encoding='utf-8')
    )
    return cast('list[dict[str, Any]]', hooks)


def _public_hook(hook_id: str) -> dict[str, Any]:
    """Bloco de um hook no contrato publico."""
    for hook in _public_hooks():
        if hook.get('id') == hook_id:
            return hook
    pytest.fail(f'{hook_id} ausente do .pre-commit-hooks.yaml')
    raise AssertionError  # pragma: no cover


def _docs_hook_ids() -> list[str]:
    """Ids da tabela de hooks de `docs/hooks.md`."""
    lines = (
        (REPO_ROOT / 'docs' / 'hooks.md')
        .read_text(encoding='utf-8')
        .splitlines()
    )
    return [
        line.split('|')[1].strip().strip('`')
        for line in lines
        if line.startswith('| `')
    ]


class TestCaseSetIssueFromBranchContract:
    """O contrato publicado precisa permitir a execucao do comando."""

    def test_id_publicado(self) -> None:
        """O id segue o padrao kebab-case e aponta para o entry certo."""
        assert _public_hook(HOOK_ID)['entry'] == ENTRY

    def test_pass_filenames_verdadeiro(self) -> None:
        """O CLI exige COMMIT_MSG_FILEPATH; sem filename ele aborta."""
        assert _public_hook(HOOK_ID)['pass_filenames'] is True

    def test_docs_usam_o_mesmo_id(self) -> None:
        """`docs/hooks.md` lista o mesmo id do contrato publico."""
        assert HOOK_ID in _docs_hook_ids()

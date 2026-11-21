"""Trava o contrato publico do detect-key (issue #436)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pytest
import yaml

REPO_ROOT = Path(__file__).parents[4]
HOOK_ID = 'detect-key'


def _load(name: str) -> Any:
    """Carrega um YAML da raiz do repositorio."""
    return yaml.safe_load((REPO_ROOT / name).read_text(encoding='utf-8'))


def _public_hook() -> dict[str, Any]:
    """Retorna o bloco do detect-key no .pre-commit-hooks.yaml."""
    for hook in _load('.pre-commit-hooks.yaml'):
        if hook.get('id') == HOOK_ID:
            return cast('dict[str, Any]', hook)
    pytest.fail(f'{HOOK_ID} ausente do .pre-commit-hooks.yaml')
    raise AssertionError  # pragma: no cover


def _config_hook() -> dict[str, Any]:
    """Retorna o bloco do detect-key no .pre-commit-config.yaml."""
    for repo in _load('.pre-commit-config.yaml')['repos']:
        for hook in repo.get('hooks', []):
            if hook.get('id') == HOOK_ID:
                return cast('dict[str, Any]', hook)
    pytest.fail(f'{HOOK_ID} ausente do .pre-commit-config.yaml')
    raise AssertionError  # pragma: no cover


class TestCaseDetectKeyContract:
    """detect-key publico varre texto, em paridade com o config local."""

    def test_publico_types_text(self) -> None:
        """Types publico e [text]; AND com python restringiria a .py."""
        assert _public_hook()['types'] == ['text']

    def test_paridade_types(self) -> None:
        """Contrato publico e config local declaram os mesmos types."""
        assert _public_hook()['types'] == _config_hook()['types']

    def test_paridade_exclude(self) -> None:
        """A auto-exclusao do modulo scanner vale nos dois contratos."""
        assert _public_hook()['exclude'] == _config_hook()['exclude']

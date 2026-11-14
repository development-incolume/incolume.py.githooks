"""Gate - hooks listados em ordem alfabetica na documentacao.

Porta de aceite do issue #383.

Este teste DEVE REPROVAR (vermelho TDD) enquanto qualquer um dos quatro
documentos listar os hooks fora de ordem alfabetica e DEVE PASSAR (verde)
quando todos estiverem ordenados por `id`.
"""

from __future__ import annotations

import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]


def _public_hook_ids() -> list[str]:
    """Ids dos hooks no contrato publico `.pre-commit-hooks.yaml`."""
    hooks = yaml.safe_load(
        (REPO_ROOT / '.pre-commit-hooks.yaml').read_text(encoding='utf-8')
    )
    return [str(hook['id']) for hook in hooks]


def _table_ids(path: pathlib.Path) -> list[str]:
    """Primeira coluna das linhas de tabela escrita com `` ` ``."""
    ids: list[str] = []
    for line in path.read_text(encoding='utf-8').splitlines():
        match = re.match(r'^\|\s*`([^`]+)`\s*\|', line)
        if match:
            ids.append(match.group(1))
    return ids


def _readme_hook_ids() -> list[str]:
    """Ids do bloco do repositorio incolume.py.githooks no README."""
    ids: list[str] = []
    in_block = False
    for line in (
        (REPO_ROOT / 'README.md').read_text(encoding='utf-8').splitlines()
    ):
        stripped = line.strip()
        if stripped.startswith(
            '- repo: https://github.com/development-incolume/incolume.py.githooks'
        ):
            in_block = True
            continue
        if not in_block:
            continue
        if stripped == '```' or stripped.startswith('- repo:'):
            break
        match = re.match(r'^\s*- id:\s*(\S+)\s*$', line)
        if match:
            ids.append(match.group(1))
    return ids


def _assert_sorted(ids: list[str], origem: str) -> None:
    """Falha com a lista atual quando ela nao esta em ordem alfabetica."""
    assert ids, f'{origem}: nenhum hook encontrado'
    assert ids == sorted(ids), (
        f'{origem}: hooks fora de ordem alfabetica: {ids}'
    )


def test_pre_commit_hooks_alfabetico() -> None:
    """O contrato publico lista os hooks em ordem alfabetica."""
    _assert_sorted(_public_hook_ids(), '.pre-commit-hooks.yaml')


def test_docs_hooks_alfabetico() -> None:
    """A tabela de hooks do docs/hooks.md esta em ordem alfabetica."""
    _assert_sorted(
        _table_ids(REPO_ROOT / 'docs' / 'hooks.md'), 'docs/hooks.md'
    )


def test_docs_cli_alfabetico() -> None:
    """A tabela de comandos do docs/cli.md esta em ordem alfabetica."""
    _assert_sorted(_table_ids(REPO_ROOT / 'docs' / 'cli.md'), 'docs/cli.md')


def test_readme_alfabetico() -> None:
    """A lista de hooks do README esta em ordem alfabetica."""
    _assert_sorted(_readme_hook_ids(), 'README.md')

"""Gate - toda funcao ``*_cli`` traz uma secao ``Examples`` na docstring.

Porta de aceite do issue #385.

Este teste DEVE REPROVAR (vermelho TDD) enquanto qualquer uma das 18
funcoes de entrada dos scripts publicados em ``[project.scripts]`` nao
trazer exemplos de uso na docstring e DEVE PASSAR (verde) quando todas
tiverem a secao ``Examples:``.
"""

from __future__ import annotations

import ast
import pathlib

CLI = (
    pathlib.Path(__file__).resolve().parents[4]
    / 'incolume'
    / 'py'
    / 'githooks'
    / 'cli'
    / 'cli.py'
)

TOTAL_CLI = 18


def _cli_functions() -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    """Funcoes de nivel de modulo cujo nome termina em ``_cli``."""
    tree = ast.parse(CLI.read_text(encoding='utf-8'))
    return [
        node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name.endswith('_cli')
    ]


def test_quantidade_de_funcoes_cli() -> None:
    """As 18 funcoes de entrada dos scripts estao presentes."""
    assert len(_cli_functions()) == TOTAL_CLI


def test_toda_cli_tem_examples() -> None:
    """Cada funcao ``*_cli`` traz uma secao ``Examples`` na docstring."""
    missing = [
        node.name
        for node in _cli_functions()
        if 'Examples:' not in (ast.get_docstring(node) or '')
    ]
    assert not missing, f'funcoes sem secao Examples: {missing}'

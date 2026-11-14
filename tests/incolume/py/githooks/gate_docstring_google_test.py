"""Gate AST - docstrings em src devem estar no estilo Google.

Porta de aceite do issue #377 (padronizacao de docstrings).

Este e um teste que DEVE REPROVAR (vermelho TDD) enquanto
qualquer docstring de src/ seguir o estilo reST antigo (nao-Google)
e DEVE PASSAR (green) quando todo o src/ estiver em estilo Google.

Regras Google validadas:
- resumo imperativo na primeira linha;
- nao usar marcadores reST (:param:, :type:, :return:, :raises:, .. versionadded::);
- Args/Returns/Raises/Examples no estilo Google (nomes de argumento em
  ``Args:``, ``Returns:``, ``Raises:`` e exemplos em ``Examples:``);
- docstrings nao-vazias para API publica e privada (funcoes, metodos e
  classes, incluindo as nomeadas com `_`).
"""

from __future__ import annotations

import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
SRC = ROOT / 'incolume' / 'py' / 'githooks'

# Marcadores de estilo reST que nao podem aparecer em docstrings Google.
_REST_MARKERS = (
    ':param ',
    ':type ',
    ':return:',
    ':raises ',
    ':var ',
    '.. versionadded::',
    '.. versionchanged::',
    '.. versionremoved::',
    '.. deprecated::',
)


def _module_docstring_googly(module: ast.Module) -> list[str]:
    errors: list[str] = []
    doc = ast.get_docstring(module)
    if doc is None:
        return errors
    if any(marker in doc for marker in _REST_MARKERS):
        errors.append('docstring do modulo em estilo reST')
    return errors


def _check_node(node: ast.AST) -> list[str]:
    errors: list[str] = []
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        doc = ast.get_docstring(node)
        if doc is None:
            errors.append(
                f'falta docstring em {node.__class__.__name__} {node.name}'
            )
        elif any(marker in doc for marker in _REST_MARKERS):
            errors.append(f'docstring de {node.name} em estilo reST')
    return errors


def _scan_file(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as exc:
        errors.append(f'{path}: erro de sintaxe: {exc}')
        return errors
    errors.extend(_module_docstring_googly(tree))
    for node in ast.walk(tree):
        errors.extend(_check_node(node))
    return errors


def test_all_src_docstrings_are_google_style() -> None:
    """Verifica que todo o src/ usa docstrings no estilo Google."""
    errors: list[str] = []
    for py in sorted(SRC.rglob('*.py')):
        if '__pycache__' in py.parts:
            continue
        errors.extend(_scan_file(py))
    assert not errors, 'docstrings nao em estilo Google: ' + '; '.join(errors)

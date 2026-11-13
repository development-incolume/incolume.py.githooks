"""Gate AST - toda funcao de teste deve ter docstring 1-liner descritiva.

Porta de aceite do issue #378 (docstrings nos testes). Mesma base AST do
gate de src (``gate_docstring_google_test.py``), rodada separada.

Regras validadas para toda funcao ``test*`` em ``tests/``:
- docstring presente e nao-vazia;
- no minimo 15 caracteres (1-liner descritiva, ex.:
  ``"Valida rodape Closes valido."``);
- nao ser mera repeticao do nome da funcao (ex.: ``"rule_length."``).
"""

from __future__ import annotations

import ast
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
TESTS = ROOT / 'tests'
MIN_LEN = 15


def _is_descriptive(name: str, doc: str) -> bool:
    """Verifica se a docstring e descritiva, nao genérica nem repeticao."""
    text = doc.strip()
    if len(text) < MIN_LEN:
        return False
    base = re.sub(r'[^a-z0-9]', '', name.removeprefix('test_').lower())
    norm = re.sub(r'[^a-z0-9]', '', text.lower())
    return not base or base != norm


def _scan_file(path: pathlib.Path) -> list[str]:
    """Coleta funcoes de teste com docstring ausente ou nao-descritiva."""
    errors: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as exc:
        return [f'{path}: erro de sintaxe: {exc}']
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith('test'):
            continue
        doc = ast.get_docstring(node)
        if doc is None or not doc.strip():
            errors.append(f'falta docstring em {node.name}')
        elif not _is_descriptive(node.name, doc):
            errors.append(
                f'docstring nao-descritiva em {node.name}: {doc.strip()!r}'
            )
    return errors


def test_all_test_functions_have_descriptive_docstring() -> None:
    """Verifica que toda funcao de teste tem docstring 1-liner descritiva."""
    errors: list[str] = []
    for py in sorted(TESTS.rglob('*.py')):
        if '__pycache__' in py.parts:
            continue
        errors.extend(_scan_file(py))
    assert not errors, 'docstrings de teste nao-descritivas: ' + '; '.join(
        errors
    )

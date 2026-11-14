"""Check the commit type against the staged files.

Compara o tipo declarado na mensagem de commit com o tipo deduzido
pelos arquivos stageados (mesma heuristica do set-type-from-status).
Bloqueia apenas divergencia objetiva: tipo declarado em
{build, ci, test, docs} diferente do deduzido, ou tipo ``feat`` diante
de alteracao objetivamente nao-codigo. Entre ``feat``, ``fix`` e
``refactor`` nao ha bloqueio — sao indistinguiveis por caminho.

(c) Copyright 2026 incolume.com.br. All rights reserved.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from incolume.py.githooks.type_from_status import (
    TYPE_BUILD,
    TYPE_CI,
    TYPE_DOCS,
    TYPE_FEAT,
    TYPE_TEST,
    declared_type,
    deduce_type,
    get_staged_files,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

OBJECTIVE_TYPES: frozenset[str] = frozenset({
    TYPE_BUILD,
    TYPE_CI,
    TYPE_TEST,
    TYPE_DOCS,
})


def is_objective_divergence(declared: str, deduced: str) -> bool:
    """Diz se ha divergencia objetiva entre o tipo declarado e o deduzido.

    Args:
        declared (str): tipo declarado na mensagem de commit.
        deduced (str): tipo deduzido pelos arquivos stageados.

    Returns:
        True quando a divergencia e objetiva.

    """
    if declared in OBJECTIVE_TYPES and declared != deduced:
        return True
    return deduced in OBJECTIVE_TYPES and declared == TYPE_FEAT


def check_type_from_status(
    filenames: list[str],
    paths: Sequence[str | Path] | None = None,
) -> int:
    """Valida o tipo do commit contra os arquivos stageados.

    Args:
        filenames (list[str]): arquivos de mensagem de commit.
        paths (Sequence[str | Path] | None): caminhos stageados; quando
            None, lidos do git.

    Returns:
        0 quando o tipo e compativel; 1 caso contrario.

    """
    staged = (
        [str(path) for path in paths]
        if paths is not None
        else get_staged_files()
    )
    deduced = deduce_type(staged)
    if not deduced:
        return 0

    for filename in filenames:
        content = Path(filename).read_text(encoding='utf-8')
        declared = declared_type(content)
        if not declared:
            continue
        if is_objective_divergence(declared, deduced):
            logging.critical(
                'Commit type %s diverges from the deduced type %s.',
                declared,
                deduced,
            )
            return 1

    return 0

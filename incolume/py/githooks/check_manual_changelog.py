"""Check manual changelog edits in the commit message.

Rejeita uma mensagem de commit que nao comece com ``build:`` quando o
indice (staged) altera o ``CHANGELOG.md`` do projeto. A comparacao e
sempre entre o indice e o ``HEAD``, nunca com a working tree.

(c) Copyright 2026 incolume.com.br. All rights reserved.
"""

# ruff: file-ignore[suspicious-subprocess-import, subprocess-without-shell-equals-true, start-process-with-partial-path]

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from incolume.py.githooks.core.utils import find_project_root

BUILD_PREFIX: str = 'build:'
CHANGELOG: str = 'CHANGELOG.md'


def _git(root: Path, *args: str) -> str | None:
    """Executa um comando git de leitura no repositorio.

    Args:
        root (Path): raiz do repositorio.
        args (tuple[str]): argumentos do comando git.

    Returns:
        saida do comando, ou None quando o git falha.

    """
    try:
        return subprocess.check_output(
            ['git', *args],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        return None


def _staged_paths(root: Path) -> list[str]:
    """Lista os caminhos alterados no indice.

    Args:
        root (Path): raiz do repositorio.

    Returns:
        caminhos relativos ao repositorio, um por linha.

    """
    output = _git(root, 'diff', '--cached', '--name-only')
    return [line for line in (output or '').splitlines() if line]


def check_manual_changelog(
    filenames: list[str],
    repo_root: Path | str | None = None,
) -> int:
    """Valida que uma mudanca de changelog e commitada com mensagem build:.

    Args:
        filenames (list[str]): arquivos de mensagem de commit.
        repo_root (Path | str | None): raiz do repositorio; por
            padrao, o projeto atual.

    Returns:
        0 quando a mensagem e ``build:`` ou o changelog nao mudou;
            1 caso contrario.

    """
    root = Path(repo_root) if repo_root else find_project_root(Path.cwd())
    messages = [
        Path(filename).read_text(encoding='utf-8') for filename in filenames
    ]
    if all(message.startswith(BUILD_PREFIX) for message in messages):
        return 0

    for staged in _staged_paths(root):
        if staged.replace('\\', '/') == CHANGELOG:
            logging.critical(
                'CHANGELOG.md changed without a "build:" commit message.',
            )
            return 1

    return 0

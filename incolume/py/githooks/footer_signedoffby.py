"""Module trailers hook."""

# ruff: noqa: S404 S607
from __future__ import annotations

import re
import shutil
import subprocess
from typing import TYPE_CHECKING

from incolume.py.githooks.utils import get_signed_off_by

if TYPE_CHECKING:
    from pathlib import Path


def clean_commit_msg(path: Path) -> bool:
    """Remove linhas do arquivo de commit.

    Entre:

    - A linha que começa com 'Please enter the commit message'
    - Até a linha contendo apenas '#'

    Cria um backup `.bak` antes de sobrescrever.

    Args:
        path (Path): Caminho para o arquivo de mensagem de commit.

    Returns:
        True, se o arquivo foi modificado; caso contrário, False.

    """
    backup: Path = path.with_suffix(path.suffix + '.bak')
    shutil.copy(path, backup)

    result: list[str] = []
    skipping: bool = False
    changed: bool = False

    for line in path.read_text(encoding='utf-8').splitlines(keepends=True):
        if not skipping and line.lstrip().startswith(
            'Please enter the commit message'
        ):
            skipping = True
            changed = True
            continue
        if skipping and line.strip() == '#':
            skipping = False
            continue
        if not skipping:
            result.append(line)

    if changed:
        path.write_text(''.join(result), encoding='utf-8')
    return changed


def add_signed_off_by(path: Path, sob: str | None = None) -> None:
    """Adiciona a linha 'Signed-off-by' ao arquivo de commit.

    Usa `git interpret-trailers` para inserir o trailer corretamente.

    Args:
        path (Path): Caminho para o arquivo de mensagem de commit.
        sob (Optional[str]): Linha de assinatura customizada. Se não informado,
                             será gerada com `get_signed_off_by()`.

    Returns:
        None

    """
    sob = sob or get_signed_off_by()
    subprocess.run(  # noqa: S603
        [
            'git',
            'interpret-trailers',
            '--in-place',
            '--trailer',
            sob,
            path.as_posix(),
        ],
        check=True,
    )


def add_blank_line_if_needed(path: Path, commit_source: str = '') -> None:
    """Insere uma linha em branco no topo do arquivo de commit.

    caso `commit_source` seja vazio e o arquivo não comece
      com linha em branco.

    Args:
        path (Path): Caminho para o arquivo de mensagem de commit.
        commit_source (str): Origem do commit (pode ser vazio).

    Returns:
        None

    """
    if commit_source is not None:
        return

    content: str = path.read_text(encoding='utf-8')
    if re.fullmatch(r'[^\n].+', content):
        path.write_text(f'\n{content}', encoding='utf-8')

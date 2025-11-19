"""Module prepare_commit_msg."""

from __future__ import annotations

from typing import TYPE_CHECKING

from incolume.py.githooks.core import debug_enable

if TYPE_CHECKING:
    from pathlib import Path

debug_enable()


def insert_git_diff(commit_msg_file: Path, diff_output: str) -> None:
    """Insere a saída do git diff.

    na primeira linha que começa com '#'
    dentro do arquivo de mensagem de commit.
    """
    if not diff_output:
        return  # nada a inserir

    lines = commit_msg_file.read_text(encoding='utf-8').splitlines(
        keepends=True
    )
    result = []

    for idx, line in enumerate(lines):
        if line.startswith('#'):
            # insere diff e interrompe após a primeira ocorrência
            result.append('\n' + diff_output + '\n')
            result.extend(lines[idx:])  # adiciona o resto sem perder conteúdo
            break
        result.append(line)
    else:
        # caso não exista linha começando com "#"
        result.extend(lines)

    commit_msg_file.write_text(''.join(result), encoding='utf-8')

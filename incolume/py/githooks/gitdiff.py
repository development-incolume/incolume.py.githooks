"""Module prepare_commit_msg."""

# ruff: noqa: S404 S607

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence


def get_git_diff() -> str:
    """Retorna a saída de `git diff --cached --name-status -r`."""
    try:
        return subprocess.check_output(
            ['git', 'diff', '--cached', '--name-status', '-r'], text=True
        ).strip()
    except subprocess.CalledProcessError as e:  # pragma: no cover
        msg = 'Falha ao executar git diff'
        raise RuntimeError(msg) from e


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


def main(argv: Sequence[str] | None = None) -> int:
    """CLI for module."""
    parser = argparse.ArgumentParser(
        description='Processa mensagens de commit'
        ' como no hook original em Perl.'
    )
    parser.add_argument(
        'commit_msg_file', type=Path, help='Arquivo da mensagem de commit'
    )
    parser.add_argument(
        'commit_source', help='Origem do commit (ex.: template)'
    )
    parser.add_argument('commit_hash', help='SHA1 do commit ou vazio')

    args = parser.parse_args(argv)

    if (args.commit_source, args.commit_hash) in {('', ''), ('template', '')}:
        diff_output = get_git_diff()
        insert_git_diff(args.commit_msg_file, diff_output)


if __name__ == '__main__':
    raise SystemExit(main())

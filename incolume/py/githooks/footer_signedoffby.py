"""Module trailers hook."""

# ruff: noqa: S404 S607
from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

from incolume.py.githooks import SUCCESS

if TYPE_CHECKING:
    from collections.abc import Sequence


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


def get_signed_off_by() -> str:
    """Obtém a linha de assinatura 'Signed-off-by' do committer atual.

    Usa `git var GIT_COMMITTER_IDENT` para extrair o nome e email do committer.

    Returns:
        str: Linha formatada no padrão:
             "Signed-off-by: Nome <email>"

    Raises:
        RuntimeError: Se a execução do comando git falhar.

    """
    try:
        ident: str = subprocess.check_output(
            ['git', 'var', 'GIT_COMMITTER_IDENT'], text=True
        ).strip()
    except (
        subprocess.CalledProcessError
    ) as e:  # pragma: no cover; noqa: S110 todo cover in future
        msg = 'Falha ao obter GIT_COMMITTER_IDENT'
        raise RuntimeError(msg) from e

    return f'Signed-off-by: {ident.split(">", maxsplit=1)[0]}>'


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


def add_blank_line_if_needed(path: Path, commit_source: str) -> None:
    """Insere uma linha em branco no topo do arquivo de commit.

    caso `commit_source` seja vazio e o arquivo não comece
      com linha em branco.

    Args:
        path (Path): Caminho para o arquivo de mensagem de commit.
        commit_source (str): Origem do commit (pode ser vazio).

    Returns:
        None

    """
    if commit_source:
        return

    content: str = path.read_text(encoding='utf-8')
    if not content.startswith('\n'):
        path.write_text('\n' + content, encoding='utf-8')


def main(argv: Sequence[str] | None = None) -> int:
    """Função principal que processa os argumentos.

    E aplica as transformações no arquivo de commit.

    Fluxo:
    1. Remove linhas desnecessárias do template de commit.
    2. Adiciona 'Signed-off-by' do committer atual.
    3. Adiciona linha em branco no topo se necessário.

    Returns:
        None

    """
    parser = argparse.ArgumentParser(
        description=(
            'Hook Git em Python equivalente ao script original em Perl/Shell.'
        )
    )
    parser.add_argument(
        'commit_msg_file', type=Path, help='Arquivo de mensagem de commit'
    )
    parser.add_argument(
        'commit_source', default='', help='Origem do commit (pode ser vazio)'
    )
    parser.add_argument(
        'commit_hash', default='', help='SHA1 do commit (pode ser vazio)'
    )

    args = parser.parse_args(argv)

    clean_commit_msg(args.commit_msg_file)
    add_signed_off_by(args.commit_msg_file)
    add_blank_line_if_needed(args.commit_msg_file, args.commit_source)
    return SUCCESS


if __name__ == '__main__':
    raise SystemExit(main())

"""Module Command Line Inteface."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import rich
from icecream import ic

from incolume.py.githooks.detect_private_key import has_private_key
from incolume.py.githooks.effort_message import effort_msg
from incolume.py.githooks.footer_signedoffby import (
    add_blank_line_if_needed,
    add_signed_off_by,
    clean_commit_msg,
)
from incolume.py.githooks.rules import FAILURE, SUCCESS
from incolume.py.githooks.utils import debug_enable
from incolume.py.githooks.valid_filename import is_valid_filename

debug_enable()

if TYPE_CHECKING:
    from collections.abc import Sequence


def check_valid_filenames_cli(argv: Sequence[str] | None = None) -> int:
    """Maint entry point for the script."""
    parser = argparse.ArgumentParser(
        prog='validate-filename',
    )
    parser.add_argument(
        'filenames',
        nargs='+',
        help='Filenames to process.',
    )
    parser.add_argument(
        '--min-len',
        default=3,
        type=int,
        help='Minimum length for a filename.',
    )
    parser.add_argument(
        '--max-len',
        default=256,
        type=int,
        help='Maximum length for a filename.',
    )

    args = parser.parse_args(argv)

    results = [
        not is_valid_filename(
            filename=filename, min_len=args.min_len, max_len=args.max_len
        )
        for filename in args.filenames
    ]
    return int(any(results))


def detect_private_key_cli(argv: Sequence[str] | None = None) -> int:
    """CLI to check private key.

    Args:
        argv (Sequence[str] | None, optional): _description_. Defaults to None.

    Returns:
        int: _description_

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    ic(args)
    return has_private_key(*args.filenames)


def footer_signedoffby_cli(argv: Sequence[str] | None = None) -> int:
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
    parser.add_argument(
        '--signoff',
        default=True,
        dest='signed',
        action='store_false',
        help='Não adicionar Signed-off-by',
    )

    args = parser.parse_args(argv)

    clean_commit_msg(args.commit_msg_file)
    if args.signed:
        add_signed_off_by(args.commit_msg_file)
    add_blank_line_if_needed(args.commit_msg_file, args.commit_source)
    return SUCCESS


def pre_commit_installed_cli() -> int:
    """Run it."""
    result = SUCCESS
    files = list(Path.cwd().glob('.pre-commit-config.yaml'))
    ic(files)
    if not files:
        rich.print(
            '\n\n[red]`pre-commit` configuration detected,'
            ' but `pre-commit install` was never ran.[/red]\n',
        )
        result |= FAILURE
    return sys.exit(result)


def effort_msg_cli() -> None:
    """Run it."""
    effort_msg()

"""Module to validate commit messages."""

import argparse
import inspect
import pathlib
import sys
from collections.abc import Sequence

from click import secho
from icecream import ic


def run(argv: Sequence[str] | None = None) -> int:
    """Validate commit messages."""
    ic(f'{inspect.currentframe().f_code.co_name}: {sys.argv=}, {argv=}')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'commit_msg_file',
        default='',
        help='Arquivo contendo a mensagem do commit',
    )
    args = parser.parse_args(argv)
    commit_msg_file = args.commit_msg_file

    commit_msg = (
        pathlib.Path(commit_msg_file).read_text(encoding='utf-8').strip()
    )

    if not commit_msg.startswith('feat') and not commit_msg.startswith('fix'):
        secho("Erros: Mensagens devem começar com 'feat' ou 'fix'", fg='red')
        return 1

    secho('Mensagem validada com sucesso.', fg='green')
    return 0


if __name__ == '__main__':
    sys.exit(run(sys.argv[1:]))
